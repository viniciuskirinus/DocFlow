from .models import conectar_db
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain_community.callbacks import get_openai_callback


def process_message(user_message, pdf_id):
    load_dotenv()
    # Conectar ao banco de dados
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT location FROM pdf WHERE id_pdf = '{pdf_id}'")
    result = cursor.fetchone()

    if result is None:
        print("PDF não encontrado no banco de dados.")
        return "Não foi encontrado um caminho para este pdf_id."

    pdf_filename = result[0]
    pdf_directory = ".\\app\data"  # Substitua com o caminho real para o seu diretório
    pdf_path = os.path.join(pdf_directory, pdf_filename)
    print(f"PDF encontrado: {pdf_path}")

    if os.path.exists(pdf_path):
        print(f"PDF encontrado: {pdf_path}")
    else:
        print("PDF não encontrado no diretório especificado.")
        return "PDF não encontrado."


    # Processar o PDF
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() if page.extract_text() else ""

    # Dividir o texto em chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Criar embeddings e base de conhecimento
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    # Busca na base de conhecimento e geração de resposta
    if user_message:
        docs = knowledge_base.similarity_search(user_message)
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=user_message)
            print(cb)
        return response

    return "Nenhuma pergunta fornecida."
