import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔑 SUAS CREDENCIAIS DA Z-API CONFIGURADAS:
ZAPI_INSTANCE_ID = "3F5AE01ACEDCB2DA1789FA3326EF075C"
ZAPI_TOKEN = "D05638613CB7A218C222D392"
ZAPI_CLIENT_TOKEN = "" 

API_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"

# Menu limpo e compacto (sem setas de números ou barras de rolagem)
MENU = """Olá! Como posso te ajudar hoje? 🤖

Digite o número da opção:
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
            # Captura o texto puro enviado
            texto_cliente = dados.get("text", "")
            if not texto_cliente and dados.get("message"):
                texto_cliente = dados.get("message", {}).get("text", "")
            
            texto_cliente = str(texto_cliente).strip()
            remetente = dados.get("phone")
            
            # 🛡️ TRAVA ANTI-LOOP: Ignora mensagens geradas pelo próprio fluxo do bot
            texto_upper = texto_cliente.upper()
            if "COMO POSSO TE AJUDAR" in texto_upper or "AUTOMAÇÕES INCRÍVEIS" in texto_upper or "CONFIRMADO EM MAIÚSCULAS" in texto_upper:
                print("Loop evitado: Mensagem do bot ignorada.")
                return jsonify({"status": "ignored_bot_output"}), 200

            if texto_cliente and remetente:
                # Se for o aviso de Trial da Z-API puro, não responde nada
                if "CONTA EM TRIAL" in texto_upper and len(texto_cliente) > 200 and not "OI" in texto_upper and not "OLA" in texto_upper:
                    return jsonify({"status": "ignored_trial_system"}), 200

                # Menu de Opções
                if texto_cliente == "1":
                    enviar_resposta(remetente, "Excelente! Desenvolvemos automações incríveis com Python. 🐍")
                elif texto_cliente == "2":
                    enviar_resposta(remetente, "Por favor, digite o NOVO ENDEREÇO e confirme com Enter:")
                elif texto_cliente == "3":
                    enviar_resposta(remetente, "Avisado! O suporte já vai falar com você.")
                elif texto_cliente == "4":
                    enviar_resposta(remetente, "Por favor, digite sua dúvida detalhadamente.")
                
                # 🔠 Trata o envio do endereço de forma estrita (evita o bug do JSON da imagem)
                elif len(texto_cliente) > 5 and not texto_cliente.isdigit() and "{" not in texto_cliente and "}" not in texto_cliente:
                    endereco_maiusculo = texto_cliente.upper()
                    enviar_resposta(remetente, f"✓ ENDEREÇO CONFIRMADO EM MAIÚSCULAS:\n{endereco_maiusculo}")
                
                # Se for uma mensagem normal (Oi, Olá), exibe o Menu compacto
                elif texto_cliente.lower() in ["oi", "ola", "olá", "menu", "bom dia", "boa tarde"]:
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