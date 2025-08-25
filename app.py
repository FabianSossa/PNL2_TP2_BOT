import os
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Cargar variables de entorno
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

# Inicializar Flask
app = Flask(__name__)

# Inicializar embeddings locales
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Cargar base de conocimiento
vectorstore = Chroma(persist_directory="vectorstore", embedding_function=embeddings)

# Configurar LLM con Groq
llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0)

# Memoria de conversación
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# RAG Chain
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=memory
)

# Interfaz mínima
html_template = '''
<!DOCTYPE html>
<html>
<head>
  <title>Chatbot RAG con Groq</title>
</head>
<body>
  <h2>Chatbot RAG con Groq</h2>
  <form id="chat-form">
    <input type="text" id="user-input" placeholder="Escribe tu pregunta..." size="50">
    <button type="submit">Enviar</button>
  </form>
  <div id="chat-box"></div>

  <script>
    const form = document.getElementById("chat-form");
    const chatBox = document.getElementById("chat-box");

    form.onsubmit = async (e) => {
      e.preventDefault();
      const userInput = document.getElementById("user-input").value;
      chatBox.innerHTML += "<p><b>Tú:</b> " + userInput + "</p>";
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userInput })
      });
      const data = await response.json();
      chatBox.innerHTML += "<p><b>Bot:</b> " + data.answer + "</p>";
      document.getElementById("user-input").value = "";
    };
  </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(html_template)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question", "")
    result = qa({"question": question})
    return jsonify({"answer": result["answer"]})

if __name__ == "__main__":
    app.run(debug=True)
