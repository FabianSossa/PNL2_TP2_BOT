import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Cargar variables
load_dotenv()

# Cargar documentos TXT y PDF
loaders = [
    DirectoryLoader("docs", glob="**/*.txt", loader_cls=TextLoader),
    DirectoryLoader("docs", glob="**/*.pdf", loader_cls=PyPDFLoader)
]

docs = []
for loader in loaders:
    docs.extend(loader.load())

# Dividir documentos
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Crear embeddings locales
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Guardar en Chroma
vectorstore = Chroma.from_documents(splits, embedding=embeddings, persist_directory="vectorstore")
vectorstore.persist()

print("✅ Ingesta completada. Documentos TXT y PDF almacenados en 'vectorstore'.")
