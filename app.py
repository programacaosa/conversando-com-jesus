import os
import streamlit as st
import unicodedata

# Define o caminho para o arquivo de dados
DATA_DIR = "dados"
QUESTION_RESPONSE_FILE = os.path.join(DATA_DIR, "perguntas_respostas.txt")

# Certifique-se de que o diretório de dados existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Função para normalizar o texto (ignorando acentos e case)
def normalize_text(text):
    # Normaliza o texto removendo acentos e transformando em minúsculas
    text = unicodedata.normalize('NFD', text)  # Decomposição de caracteres Unicode
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])  # Remove os acentos
    return text.lower()

# Função para carregar perguntas e respostas do arquivo
def load_questions_and_responses():
    if not os.path.exists(QUESTION_RESPONSE_FILE):
        return []  # Se o arquivo não existir, retorna uma lista vazia
    
    with open(QUESTION_RESPONSE_FILE, "r", encoding="utf-8") as file:
        # Carrega perguntas e respostas separadas por ":", e retorna como lista de pares (pergunta, resposta)
        return [line.strip().split(":", 1) for line in file.readlines() if line.strip()]

# Função para salvar a pergunta no arquivo
def save_question(question):
    with open(QUESTION_RESPONSE_FILE, "a", encoding="utf-8") as file:
        file.write(f"{question}:\n")  # Salva a pergunta com ":" e uma linha em branco para a resposta

# Função para buscar a resposta para a pergunta no arquivo
def get_response(question, questions_and_responses):
    question_normalized = normalize_text(question)  # Normaliza a pergunta antes de comparar
    for line in questions_and_responses:
        stored_question = line[0].strip()  # Pergunta registrada
        if normalize_text(stored_question) == question_normalized:
            return line[1].strip() if len(line) > 1 else None  # Retorna a resposta, se existir
    return None

# Carregar perguntas e respostas do arquivo
questions_and_responses = load_questions_and_responses()

# Configuração da interface Streamlit
st.title("Conversando com DEUS ...")

# Campo de texto para entrada da pergunta
question = st.text_input("Digite sua pergunta:")

# Função para exibir as perguntas e respostas com balões, um ao lado do outro
def display_conversation(question, response):
    col1, col2 = st.columns([3, 6])  # Colunas para pergunta à esquerda e resposta à direita
    
    # Exibe a pergunta com estilo de balão à esquerda
    with col1:
        if question:
            st.markdown(f'<div style="background-color: #DCF8C6; padding: 15px 20px; border-radius: 20px; max-width: 70%; word-wrap: break-word; margin-bottom: 15px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">'
                        f'<strong>Você:</strong><br>{question}</div>', unsafe_allow_html=True)
    
    # Exibe a resposta com estilo de balão à direita e deslocando um pouco para baixo
    with col2:
        if response:
            st.markdown(f'<div style="background-color: #FFFFFF; padding: 15px 20px; border-radius: 20px; max-width: 70%; word-wrap: break-word; border: 1px solid #ECE5DD; margin-top: 25px; margin-bottom: 15px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">'
                        f'<strong>Jesus:</strong><br>{response}</div>', unsafe_allow_html=True)

# Botão para enviar a pergunta
if st.button("Enviar"):
    if question:
        # Salvar a pergunta no arquivo
        save_question(question)

        # Atualizar a lista de perguntas e respostas após salvar
        questions_and_responses = load_questions_and_responses()

        # Buscar a resposta para a pergunta
        response = get_response(question, questions_and_responses)

        # Exibir a pergunta e a resposta no formato de balões
        display_conversation(question, response)
    else:
        st.warning("Por favor, insira uma pergunta.")
