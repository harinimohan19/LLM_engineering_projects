import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import openai
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

print("Loading research paper...")
paper_text = load_pdf("Miniature_crane_prototype.pdf")

chunk_size = 300
chunks = [paper_text[i:i+chunk_size] for i in range(0, len(paper_text), chunk_size)]
# print(chunks)

print("Creating embeddings...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embed_model.encode(chunks).tolist()


print("Storing in ChromaDB...")
client = chromadb.PersistentClient(path="./chroma_db", settings=Settings(anonymized_telemetry=False))
collection_name = "research_papers"

existing = [c.name for c in client.list_collections()]
if collection_name in existing:
    client.delete_collection(collection_name)

collection = client.create_collection(name=collection_name)

collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

print("Paper indexed successfully!\n")


while True:
    question = input("Ask a question about the paper (or type 'exit'): ")
    if question.lower() == "exit":
        break

    query_embedding = embed_model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=10
    )

    context = " ".join(results["documents"][0])

    prompt = f"""
    You are answering questions about a research paper.

    Context:
    {context}

    Question: {question}
    Answer:
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    print("\n Answer:\n", response.choices[0].message.content, "\n")
