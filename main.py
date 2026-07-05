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
            # Pegando as informações brutas da Z-API
            texto_cliente = dados.get("text", "")
            if not texto_cliente and dados.get("message"):
                texto_cliente = dados.get("message", {}).get("text", "")
            
            texto_cliente = str(texto_cliente).strip()
            remetente = dados.get("phone")
            
            # Se for uma notificação vazia, ignora
            if not texto_cliente or not remetente:
                return jsonify({"status": "empty_message"}), 200

            # 🛡️ TRAVA ANTI-LOOP E FILTRO DE TIE-IN DA CONTA TRIAL
            # Se a mensagem recebida for o próprio bot falando (ou o eco do menu), ignora
            texto_upper = texto_cliente.upper()
            if "COMO POSSO TE AJUDAR" in texto_upper or "AUTOMAÇÕES INCRÍVEIS" in texto_upper or "CONFIRMADO EM MAIÚSCULAS" in texto_upper:
                print("Loop evitado: Mensagem gerada pelo bot ignorada.")
                return jsonify({"status": "ignored_bot_output"}), 200
            
            # Se a mensagem contiver o bloco enorme de JSON gerado pelo loop anterior do Trial, limpa
            if "MESSAGE" in texto_upper and "CONTA EM TRIAL" in texto_upper:
                # Extrai apenas o comando final caso esteja embutido, ou ignora se for eco
                if "'MESSAGE': '1'" in texto_upper or "'1'" in texto_upper: texto_cliente = "1"
                elif "'MESSAGE': '2'" in texto_upper or "'2'" in texto_upper: texto_cliente = "2"
                elif "'MESSAGE': '3'" in texto_upper or "'3'" in texto_upper: texto_cliente = "3"
                elif "'MESSAGE': '4'" in texto_upper or "'4'" in texto_upper: texto_cliente = "4"
                elif "OI" in texto_upper or "OLA" in texto_upper: texto_cliente = "oi"
                else:
                    return jsonify({"status": "ignored_raw_trial_block"}), 200

            # Atualiza o upper pós-limpeza
            texto_upper = texto_cliente.upper()

            # Menu de Opções
            if texto_cliente == "1":
                enviar_resposta(remetente, "Excelente! Desenvolvemos automações incríveis com Python. 🐍")
            elif texto_cliente == "2":
                enviar_resposta(remetente, "Por favor, digite o NOVO ENDEREÇO e confirme com Enter:")
            elif texto_cliente == "3":
                enviar_resposta(remetente, "Avisado! O suporte já vai falar com você.")
            elif texto_cliente == "4":
                enviar_resposta(remetente, "Por favor, digite sua dúvida detalhadamente.")
            
            # 🔠 Trata o envio do endereço de forma limpa
            elif len(texto_cliente) > 5 and not texto_cliente.isdigit() and "{" not in texto_cliente:
                endereco_maiusculo = texto_cliente.upper()
                enviar_resposta(remetente, f"✓ ENDEREÇO CONFIRMADO EM MAIÚSCULAS:\n{endereco_maiusculo}")
            
            # Qualquer palavra de saudação aciona o menu compacto
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