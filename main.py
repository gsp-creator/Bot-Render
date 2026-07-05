import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ZAPI_INSTANCE_ID = "3F5AE01ACEDCB2DA1789FA3326EF075C"
ZAPI_TOKEN = "D05638613CB7A218C222D392"
ZAPI_CLIENT_TOKEN = ""

API_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"

MENU = """Olá! Eu sou o assistente virtual do Erick. 🤖

Como posso te ajudar hoje? Digite o número da opção:
1️⃣ - Saber mais sobre os projetos
2️⃣ - Solicitar um orçamento
3️⃣ - Falar diretamente com ele
4️⃣ - Outros assuntos"""

@app.route("/", methods=["GET"])
def home():
    return "Bot do Erick está Online e Conectado à Z-API! 🚀", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.get_json()
    
    # Isso vai printar no painel do Render tudo o que a Z-API está enviando!
    print("DADOS RECEBIDOS DO WEBHOOK:", dados)
    
    if dados:
        try:
            # Garante a captura do texto tanto se for enviado por você quanto por terceiros
            texto_cliente = dados.get("text", "")
            if not texto_cliente and dados.get("message"):
                texto_cliente = dados.get("message", {}).get("text", "")
                
            texto_cliente = str(texto_cliente).strip()
            remetente = dados.get("phone")
            
            if texto_cliente and remetente:
                if texto_cliente == "1":
                    enviar_resposta(remetente, "Excelente! Desenvolvemos automações incríveis com Python. 🐍")
                elif texto_cliente == "2":
                    enviar_resposta(remetente, "Perfeito! Por favor, descreva brevemente o que você precisa automatizar.")
                elif texto_cliente == "3":
                    enviar_resposta(remetente, "Avisado! O Erick já vai te responder assim que estiver disponível.")
                elif texto_cliente == "4":
                    enviar_resposta(remetente, "Por favor, digite sua dúvida detalhadamente.")
                else:
                    enviar_resposta(remetente, MENU)
        except Exception as e:
            print(f"Erro ao processar o webhook: {e}")
            
    return jsonify({"status": "success"}), 200

def enviar_resposta(numero_cliente, texto):
    payload = {
        "phone": numero_cliente,
        "message": texto
    }
    headers = {
        "Content-Type": "application/json"
    }
    if ZAPI_CLIENT_TOKEN:
        headers["Client-Token"] = ZAPI_CLIENT_TOKEN
        
    try:
        res = requests.post(API_URL, json=payload, headers=headers)
        print("Resposta do envio da Z-API:", res.status_code, res.text)
    except Exception as e:
        print(f"Erro ao enviar mensagem via API: {e}")

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)