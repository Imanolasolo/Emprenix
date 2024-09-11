import streamlit as st
from streamlit_option_menu import option_menu
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI 
from htmlTemplates import css, bot_template, user_template
import os
import base64
from home import home_show
from about import about_show
from contact import contact_show

st.set_page_config(page_title="Emprenix", layout="wide")

# Function to extract text from a PDF file
def get_pdf_text(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text = ""
    # Iterate through each page and extract text
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to split the extracted text into manageable chunks for processing
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to generate a vector store using the text chunks
def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPEN_AI_APIKEY"])
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Function to create a conversational chain using the vector store
def get_conversation_chain(vector_store):
    llm = ChatOpenAI(openai_api_key=st.secrets["OPEN_AI_APIKEY"])
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Function to handle user input and generate responses
def handle_user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    # Display the conversation history
    for i, msg in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64_of_bin_file('fondo.jpg')

st.markdown(
    f"""
    <style>
    .stApp {{
        background: url('data:image/jpeg;base64,{img_base64}') no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Crear una barra de navegación superior CON LOGO
col1,col2 = st.columns ([1,6])
with col1:
    st.image('EMPRENIX_LOGO.jpg', width=150)
with col2:    
    selected = option_menu(
        menu_title='Emprenix, your growing partner',
        options=["Home", "What can we do for you?", "Contact"],  # Opciones del menú
        icons=["house", "info-circle", "envelope"],  # Iconos para las opciones
        menu_icon="cast",  # Icono del menú
        default_index=0,  # Opción seleccionada por defecto
        orientation="horizontal",  # Menú horizontal
    )

# Mostrar contenido según la selección en la barra de navegación
if selected == "Home":
    home_show()
elif selected == "What can we do for you?":
    about_show()
elif selected == "Contact":
    contact_show()
    


# Verificar si el estado de mostrar_chat existe en session_state
if 'mostrar_chat' not in st.session_state:
    st.session_state.mostrar_chat = False

# Botón para mostrar/ocultar el chat
col1, col2 = st.columns([4,1])
with col1:
    pass
with col2:
    if st.button("💬 Talk with our AI"):
        st.session_state.mostrar_chat = not st.session_state.mostrar_chat

# Si el estado mostrar_chat es verdadero, mostrar el chat
if st.session_state.mostrar_chat:
    col1, col2 = st.columns(2)
    with col1:
        pass
    with col2:
        # Section for interacting with the AI chatbot
        st.write("### Chat with Us, know me and let´s contact!")
        st.info("Doesn´t matter the language, ask anything you need!")

        # Process the PDF file to be used as context for the chatbot
        pdf_path = os.path.join(os.getcwd(), "Emprenix.pdf")
        pdf_text = get_pdf_text(pdf_path)
        text_chunks = get_text_chunks(pdf_text)
        vector_store = get_vector_store(text_chunks)
        conversation_chain = get_conversation_chain(vector_store)

        # Store the conversation chain and history in session state
        st.session_state.conversation = conversation_chain
        st.session_state.chat_history = []

        # Input box for user questions
        user_question = st.text_input("Ask us anything about how Emprenix can help you!:")
        if user_question:
            handle_user_input(user_question)
