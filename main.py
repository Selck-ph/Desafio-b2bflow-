import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client
import requests

# Configuração de Logging (boas práticas)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

def carregar_variaveis():
    """Carrega variáveis de ambiente do arquivo .env"""
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    zapi_instance_id = os.getenv("ZAPI_INSTANCE_ID")
    zapi_token = os.getenv("ZAPI_TOKEN")
    zapi_client_token = os.getenv("ZAPI_CLIENT_TOKEN", "") # Opcional dependendo da config

    if not supabase_url or not supabase_key or not zapi_instance_id or not zapi_token:
        logging.error("Faltam variáveis de ambiente obrigatórias. Verifique seu arquivo .env.")
        exit(1)
        
    return supabase_url, supabase_key, zapi_instance_id, zapi_token, zapi_client_token or ""

def buscar_contatos(supabase: Client):
    """Busca contatos na tabela 'contacts' do Supabase"""
    try:
        # Busca até 3 contatos conforme a regra do desafio
        response = supabase.table("contacts").select("name, phone").limit(3).execute()
        contatos = response.data
        if not contatos:
            logging.warning("Nenhum contato encontrado na tabela 'contacts'.")
            return []
        
        logging.info(f"Foram encontrados {len(contatos)} contatos para envio.")
        return contatos
    except Exception as e:
        logging.error(f"Erro ao buscar contatos no Supabase: {e}")
        return []

def enviar_mensagem_zapi(instancia_id, token, client_token, telefone, mensagem):
    """Envia mensagem de texto usando a Z-API"""
    url = f"https://api.z-api.io/instances/{instancia_id}/token/{token}/send-text"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    if client_token:
        headers["Client-Token"] = client_token

    payload = {
        "phone": telefone,
        "message": mensagem
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Lança erro se o status HTTP não for 200
        
        data = response.json()
        logging.info(f"Mensagem enviada com sucesso para o número {telefone}. Resposta Z-API: {data.get('message', 'OK')}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar mensagem para {telefone}: {e}")
        if e.response is not None:
            logging.error(f"Detalhes do erro: {e.response.text}")
        return False

def main():
    logging.info("Iniciando o script de envio de mensagens.")
    
    # 1. Carregar configuração
    supabase_url, supabase_key, zapi_instance_id, zapi_token, zapi_client_token = carregar_variaveis()

    # 2. Inicializar cliente do Supabase
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        logging.info("Cliente do Supabase inicializado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao inicializar cliente do Supabase: {e}")
        exit(1)

    # 3. Buscar os contatos no banco de dados
    contatos = buscar_contatos(supabase)

    if not contatos:
        logging.info("Encerrando script pois não há contatos para envio.")
        exit(0)

    # 4. Enviar mensagem para cada contato
    for contato in contatos:
        nome_contato = contato.get("name")
        telefone = contato.get("phone")
        
        if not nome_contato or not telefone:
            logging.warning(f"Contato inválido ou com dados faltando: {contato}. Pulando...")
            continue
            
        # Personaliza a mensagem com o nome_contato do banco de dados
        mensagem = f"Olá, {nome_contato} tudo bem com você?"
        logging.info(f"Preparando envio para {nome_contato} ({telefone})...")
        
        sucesso = enviar_mensagem_zapi(
            zapi_instance_id, 
            zapi_token, 
            zapi_client_token, 
            telefone, 
            mensagem
        )
        
        if sucesso:
            logging.info(f"Envio para {nome_contato} concluído.")
        else:
            logging.error(f"Falha ao processar o envio para {nome_contato}.")

    logging.info("Processamento finalizado com sucesso!")

if __name__ == "__main__":
    main()
