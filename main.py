import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Insira suas credenciais da Z-API aqui
ZAPI_INSTANCE_ID = "3F5AE01ACEDCB2DA1789FA3326EF075C"
ZAPI_TOKEN = "D05638613CB7A218C222D392"
ZAPI_CLIENT_TOKEN = "" 

API_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"

# Menu compacto e direto para evitar qualquer necessidade de barra de rolagem
MENU = """Olá, Erick! Bot em modo de desenvolvimento. 🤖

Escolha uma opção:
1 - Saber mais sobre os projetos
2 - Alterar endereço de transferência
3 - Falar com o suporte
4 - Outros assuntos"""

@app.route("/", methods=["GET"])
def home():
    return "Bot de Desenvolvimento do Erick está Online! 🚀", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.get_json()
    
    if dados:
        try:
            # 🛑 BLOQUEIO DO LOOP INFERNAL:
            # Se a mensagem recebida contiver exatamente o texto do menu, 
            # significa que foi o próprio bot que enviou. Nós ignoramos para quebrar o loop!
            texto_cliente = dados.get("text", "")
            if not texto_cliente and dados.get("message"):
                texto_cliente = dados.get("message", {}).get("text", "")
            
            texto_cliente = str(texto_cliente).strip()
            
            if "Olá, Erick! Bot em modo de desenvolvimento." in texto_cliente:
                print("Loop bloqueado com sucesso! (Mensagem enviada pelo próprio bot)")
                return jsonify({"status": "loop_prevented"}), 200

            remetente = dados.get("phone")
            
            if texto_cliente and remetente:
                # Menu de Opções
                if texto_cliente == "1":
                    enviar_resposta(remetente, "Excelente! Desenvolvemos automações incríveis com Python. 🐍")
                elif texto_cliente == "2":
                    enviar_resposta(remetente, "Por favor, digite o NOVO ENDEREÇO e aperte Enter para confirmar:")
                elif texto_cliente == "3":
                    enviar_resposta(remetente, "Avisado! O suporte já vai falar com você.")
                elif texto_cliente == "4":
                    enviar_resposta(remetente, "Por favor, digite sua dúvida detalhadamente.")
                
                # Se o usuário estiver respondendo o endereço (independente de maiúscula/minúscula)
                # O sistema vai processar e exibir o texto transformado todo em MAIÚSCULA
                elif len(texto_cliente) > 5 and not texto_cliente.isdigit():
                    endereco_maiusculo = texto_cliente.upper()
                    enviar_resposta(remetente, f"✓ ENDEREÇO CONFIRMADO EM MAIÚSCULAS:\n{endereco_maiusculo}")
                
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