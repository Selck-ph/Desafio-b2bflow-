# Desafio de Estágio Desenvolvedor Python - b2bflow ⚡

Este projeto é a solução para o desafio da primeira etapa do processo seletivo para Estágio em Desenvolvimento Python na b2bflow. O objetivo principal é ler contatos previamente cadastrados no Supabase e enviar uma mensagem personalizada via Z-API usando Python.

## Tecnologias e Bibliotecas

- Python 3.10+
- `supabase` (Cliente Python para integração com Supabase)
- `requests` (Requisições HTTP para a Z-API)
- `python-dotenv` (Gerenciamento de variáveis de ambiente)
- `logging` nativo do Python para rastreio de atividades e erros.

## Pré-requisitos e Setup

### 1. Setup da Tabela no Supabase
1. Crie um projeto gratuito no [Supabase](https://supabase.com/).
2. Vá ao **SQL Editor** ou use a interface visual para criar uma tabela chamada `contacts`.
3. A tabela deve conter no mínimo as seguintes colunas:
   - `id` (int8 ou uuid, chave primária)
   - `name` (text, nome do contato)
   - `phone` (text, número do telefone no formato internacional, ex: `5511999999999`)
4. Insira de 1 a 3 linhas com contatos de teste.
5. Pegue a sua `URL` e a `anon public key` em _Project Settings > API_.

### 2. Setup na Z-API
1. Crie uma conta no [Z-API](https://www.z-api.io/).
2. Crie uma instância e conecte seu WhatsApp lendo o QR Code.
3. Copie o **ID da Instância** e o **Token**.

### 3. Setup do Ambiente Local

Clone este repositório para o seu computador:
```bash
git clone <url-deste-repositorio>
cd desafio-b2bflow
```

Crie e ative um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
# No Windows
venv\Scripts\activate
# No Mac/Linux
source venv/bin/activate
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

### 4. Configuração das Variáveis de Ambiente (.env)

O projeto usa um arquivo `.env` para proteger chaves e tokens sensíveis.

Copie o arquivo de exemplo para criar o seu próprio:
```bash
cp .env.example .env
```
_(Ou apenas crie um arquivo chamado `.env` e copie o conteúdo de `.env.example`)_

Abra o `.env` criado e preencha com suas chaves:
```env
SUPABASE_URL=https://<SUA-URL>.supabase.co
SUPABASE_KEY=<SUA-CHAVE-ANON-PUBLICA>
ZAPI_INSTANCE_ID=<SEU-ID-DE-INSTANCIA>
ZAPI_TOKEN=<SEU-TOKEN-ZAPI>
# Opcional (deixe em branco se não usar):
ZAPI_CLIENT_TOKEN=
```

## Como Rodar

Com o `.env` preenchido e as dependências instaladas, basta executar:

```bash
python main.py
```

Você verá a saída de logs no seu console indicando a conexão com o Supabase, a busca dos contatos e os status dos envios da Z-API.

## O que foi desenvolvido

- **Fluxo funcionando de ponta a ponta**, lendo os dados do banco e conectando ao Z-API com limite explícito para até 3 números.
- **Tratamento de erro e logging detalhado** utilizando o módulo `logging` nativo do Python, garantindo uma rastreabilidade profissional.
- A mensagem é corretamente formatada via f-string no Python (`"Olá, <nome_contato> tudo bem com você?"`), utilizando dados dinâmicos do banco.
- Segurança reforçada para não expor tokens sensíveis, utilizando `python-dotenv`.
- Código limpo, componentizado em funções de responsabilidade única.
- Uso inteligente de commits diretos e objetivos durante o desenvolvimento.
