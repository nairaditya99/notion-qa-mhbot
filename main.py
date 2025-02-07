"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
import faiss
from langchain import OpenAI
from langchain.chains import VectorDBQA
import pickle
import ingest

# Load the LangChain.
index = faiss.read_index("docs.index")

with open("faiss_store.pkl", "rb") as f:
    store = pickle.load(f)

store.index = index
chain = VectorDBQA.from_llm(llm=OpenAI(), vectorstore=store)

# From here down is all the StreamLit UI.
st.set_page_config(page_title="AURA the mental health bot", page_icon=":robot:")
st.header("AURA")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text


user_input = get_text()

if user_input:
    result = chain({"question": user_input})
    output = f"{result['answer']}"

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
