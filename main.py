import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Seu menu personalizado de opções
MENU = """Olá! Eu sou o assistente virtual do Erick. 🤖

Como posso te ajudar hoje? Digite o número da opção:
1️⃣ - Saber mais sobre os projetos
2️⃣ - Solicitar um orçamento
3️⃣ - Falar diretamente com ele
4️⃣ - Outros assuntos"""

@app.route("/", methods=["GET"])
def home():
    return "Bot do Erick está Online! 🚀", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.get_json()
    
    # Esta estrutura vai depender do provedor de API de WhatsApp que você conectar
    if dados and "message" in dados:
        texto_cliente = dados["message"].get("text", "").strip()
        chat_id = dados["message"].get("chatId") # Número de telefone do cliente
        
        # Respostas baseadas nas opções do menu
        if texto_cliente == "1":
            enviar_resposta(chat_id, "Excelente! Desenvolvemos automações incríveis com Python. 🐍")
        elif texto_cliente == "2":
            enviar_resposta(chat_id, "Perfeito! Por favor, descreva brevemente o que você precisa automatizar.")
        elif texto_cliente == "3":
            enviar_resposta(chat_id, "Avisado! O Erick já vai te responder assim que estiver disponível.")
        elif texto_cliente == "4":
            enviar_resposta(chat_id, "Por favor, digite sua dúvida detalhadamente.")
        else:
            enviar_resposta(chat_id, MENU)
            
    return jsonify({"status": "success"}), 200

def enviar_resposta(chat_id, texto):
    # Aqui faremos a conexão com o provedor que enviará a mensagem de fato
    print(f"Enviando para {chat_id}: {texto}")
    # Exemplo: requests.post(API_URL, json={"to": chat_id, "body": texto})

if __name__ == "__main__":
    # O Render define a porta automaticamente através da variável de ambiente PORT
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)