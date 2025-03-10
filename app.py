import streamlit as st
import re
from datetime import datetime

# Carrega dados existentes
def load_data(file_name):
    data = []
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and ":" in line:
                    keys, resp = line.split(":", 1)
                    keywords = [k.strip().lower() for k in keys.split(",")]
                    data.append({
                        "keywords": keywords,
                        "response": resp.strip()
                    })
        data.sort(key=lambda x: max(len(k) for k in x["keywords"]), reverse=True)
        return data
    except FileNotFoundError:
        return []

# Salva novos dados
def save_data(file_name, new_entry):
    with open(file_name, "a", encoding='utf-8') as f:
        keywords = ", ".join(new_entry["keywords"])
        f.write(f"\n{keywords}: {new_entry['response']}")

# Inicialização do session state
if 'data' not in st.session_state:
    st.session_state.data = load_data("data.txt")

if 'teach_mode' not in st.session_state:
    st.session_state.teach_mode = False

if 'current_question' not in st.session_state:
    st.session_state.current_question = ""

# Interface principal
st.title("ChatBot com Aprendizado Contínuo 🤖📚")

# Campo de pergunta
user_input = st.text_input("Digite sua pergunta:", key="user_input")

if st.button("Enviar"):
    if user_input.strip():
        st.session_state.current_question = user_input
        cleaned = re.sub(r'[^\w\s]', '', user_input.lower())
        response = None

        # Busca resposta
        for entry in st.session_state.data:
            if any(keyword in cleaned for keyword in entry["keywords"]):
                response = entry["response"]
                break
        
        if response:
            st.session_state.teach_mode = False
            st.success(f"**Resposta:** {response}")
        else:
            st.session_state.teach_mode = True
    else:
        st.warning("⚠️ Digite uma pergunta válida!")

# Modo de aprendizado
if st.session_state.teach_mode:
    st.warning("❓ Desculpe, não sei a resposta. Gostaria de me ensinar?")
    
    with st.form(key='teach_form'):
        new_keywords = st.text_input("Digite palavras-chave (separadas por vírgula)")
        new_response = st.text_area("Digite a resposta correta")
        submit_button = st.form_submit_button("Salvar novo conhecimento")
    
    if submit_button:
        if new_keywords.strip() and new_response.strip():
            # Formata nova entrada
            keywords_list = [k.strip().lower() for k in new_keywords.split(",")]
            new_entry = {
                "keywords": keywords_list,
                "response": new_response.strip()
            }
            
            # Salva no arquivo e atualiza sessão
            save_data("data.txt", new_entry)
            st.session_state.data = load_data("data.txt")  # Recarrega dados atualizados
            st.session_state.teach_mode = False
            st.success("✅ Aprendizado concluído com sucesso!")
            st.rerun()  # ✅ Recarrega a interface atualizado
        else:
            st.error("⚠️ Preencha todos os campos para ensinar uma nova resposta!")
