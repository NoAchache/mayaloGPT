import streamlit as st
from openai import OpenAI
import os

st.set_page_config(
    page_title="MayaloGPT", page_icon=":penguin:", layout="wide"
)

st.title(":penguin: MayaloGPT")
client = OpenAI()
model = "ft:gpt-3.5-turbo-1106:personal::8RdTmood"

mayaliens = ["Sade", "Clara", "Baptiste", "Romain", "Fanny", "Léopoldine", "Noé", "Benjamin"]


with st.sidebar:
    temperature = st.slider(
        "Taux de créativité",
        min_value=0.0,
        max_value=2.0,
        value=0.,
    )

    max_tokens = st.slider(
        "Nombre maximum de tokens (1 mot ~ 2 tokens)",
        min_value=0,
        max_value=1000,
        value=150,
    )

    asker = st.selectbox("Quel Mayalien pose la question? (Choisi 'Tous' pour tester tout les Mayaliens)", mayaliens + ["Tous"])
    answerer = st.selectbox("Quel Mayalien répond à la question? (Choisi 'Tous' pour tester tout les Mayaliens)", mayaliens + ["Tous"])


if asker == "Tous" and answerer == "Tous":
    st.warning("Choisis pas 'Tous' pour les deux options, le rendu va être moche, ça sert à rien bb")
    st.stop()

question = st.text_input("Quelle est la question?")

if question == "":
    st.stop()

def get_answer(question, asker, answerer, max_tokens):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": asker + ": " + question + "\n\n" + answerer + ": "}
            , ], temperature=temperature, max_tokens=max_tokens
    )
    return response.choices[0].message.content

if asker == "Tous":
    mayaliens_filtered = [mayalien for mayalien in mayaliens if mayalien != answerer]
    for mayalien in mayaliens_filtered:
        with st.chat_message(mayalien, avatar=f"{mayalien}.jpg"):
            st.markdown(question)
        with st.chat_message(answerer, avatar=f"{answerer}.jpg"):
            st.text(get_answer(question, mayalien, answerer, max_tokens))

        st.write("--------")

elif answerer == "Tous":
    mayaliens_filtered = [mayalien for mayalien in mayaliens if mayalien != asker]
    for mayalien in mayaliens_filtered:
        with st.chat_message(asker, avatar=f"{asker}.jpg"):
            st.markdown(question)
        with st.chat_message(mayalien, avatar=f"{mayalien}.jpg"):
            st.text(get_answer(question, asker, mayalien, max_tokens))

        st.write("--------")

else:
    with st.chat_message(asker, avatar=f"{asker}.jpg"):
        st.markdown(question)
    with st.chat_message(answerer, avatar=f"{answerer}.jpg"):
        st.text(get_answer(question, asker, answerer, max_tokens))




