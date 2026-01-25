import os
import streamlit as st
import openai
from dotenv import load_dotenv

# API KEY
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4o-mini"

# LLM CALL
def continue_conversation(messages, temperature=0.2):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

# SYSTEM PROMPT
SYSTEM_PROMPT = """
You work collecting orders in a delivery IceCream shop called "I'm Freezed".

Your behavior:
1. Greet warmly
2. Collect the full order (flavor or mixed flavors, size, toppings)
3. Summarize the order
4. Provide total price
5. Ask for final confirmation

Rules:
- Ice cream can have ONE flavor or a MIX of TWO flavors
- Only allow items from the menu
- If user asks for something not on menu, politely refuse and show valid options
- Keep responses short and friendly

MENU

Flavors: Vanilla, Chocolate, Lemon, Strawberry, Coffee
Sizes:
- Big: $3
- Medium: $2

Toppings ($0.5 each):
- Caramel sausage
- White chocolate
- Melted peanut butter
"""

# UI Configuration
st.set_page_config(page_title="🍦 I'm Freezed", page_icon="🍨", layout="centered")

st.title("🍦 I'm Freezed – Ice Cream Order Bot")
st.caption("Mix flavors, add toppings, and chat to customize your treat!")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if "order" not in st.session_state:
    st.session_state.order = {}

with st.sidebar:
    st.header("🍨 Build Your Ice Cream")

    flavors = st.multiselect(
        "Choose up to TWO flavors",
        ["Vanilla", "Chocolate", "Lemon", "Strawberry", "Coffee"],
        max_selections=2
    )

    size = st.radio("Size", ["Medium ($2)", "Big ($3)"])

    toppings = st.multiselect(
        "Toppings ($0.5 each)",
        ["Caramel sausage", "White chocolate", "Melted peanut butter"]
    )

    if st.button("➕ Add This Ice Cream"):
        if not flavors:
            st.warning("Please select at least one flavor.")
        else:
            flavor_text = " and ".join(flavors)
            structured_prompt = f"I want a {size} ice cream with {flavor_text} flavor and toppings: {', '.join(toppings) if toppings else 'no toppings'}."

            st.session_state.messages.append({"role": "user", "content": structured_prompt})
            st.session_state.order = {
                "flavors": flavors,
                "size": size,
                "toppings": toppings
            }
            st.rerun()

    st.divider()

    if st.button("🔄 Start New Order"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.session_state.order = {}
        st.rerun()

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# CHAT INPUT
user_input = st.chat_input("Tell me if you'd like to change anything or confirm your order...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    response = continue_conversation(st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

# ORDER SUMMARY UI
if st.session_state.order:
    st.divider()
    st.subheader("🧾 Your Ice Cream")

    flavors = st.session_state.order.get("flavors", [])
    size = st.session_state.order.get("size")
    toppings = st.session_state.order.get("toppings", [])

    base_price = 3 if "Big" in size else 2
    topping_cost = 0.5 * len(toppings)
    total = base_price + topping_cost

    with st.container(border=True):
        st.markdown(f"**Flavors:** {' + '.join(flavors)}")
        st.markdown(f"**Size:** {size}")
        st.markdown(f"**Toppings:** {', '.join(toppings) if toppings else 'None'}")

    with st.expander("💰 Price Details"):
        st.write(f"Ice Cream ({size.split()[0]}): ${base_price}")
        st.write(f"Toppings ({len(toppings)} × $0.5): ${topping_cost:.2f}")
        st.write(f"### Total: ${total:.2f}")

    st.info("📝 Your order is being prepared.")
