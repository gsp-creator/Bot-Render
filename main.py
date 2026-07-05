import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configurações da API que conecta ao seu número real
# (Você vai preencher com os dados do provedor escolhido)
API_URL = "URL_DA_API_AQUI"
API_TOKEN = "SEU_TOKEN_AQUI"

MENU = """Olá! Eu sou o assistente virtual do Erick. 🤖

Como posso te ajudar hoje? Digite o número da opção:
1️⃣ - Saber mais sobre os projetos
2️⃣ - Solicitar um orçamento
3️⃣ - Falar diretamente com ele
4️⃣ - Outros assuntos"""

@app.route("/", methods=["GET"])
def home():
    return "Bot do Erick está Online e Conectado ao número pessoal! 🚀", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.get_json()
    
    # Captura a mensagem que chegou no seu WhatsApp pessoal
    # (A estrutura exata dos campos muda de acordo com o provedor da API)
    if dados:
        try:
            # Exemplo padrão de mercado para APIs de leitura de QR Code
            texto_cliente = dados.get("message", {}).get("text", "").strip()
            remetente = dados.get("sender", {}).get("number") # Número de quem mandou
            
            if texto_cliente and remetente:
                # Respostas baseadas no menu
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
            print(f"Erro ao processar dados do webhook: {e}")
            
    return jsonify({"status": "success"}), 200

def enviar_resposta(numero_cliente, texto):
    # Envia a mensagem de volta usando a API conectada ao seu celular
    url_envio = f"{API_URL}/send-text"
    payload = {
        "number": numero_cliente,
        "text": texto
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        requests.post(url_envio, json=payload, headers=headers)
    except Exception as e:
        print(f"Erro ao enviar mensagem via API: {e}")

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)