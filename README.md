# Desafio de Estágio b2bflow ⚡

Projeto em Python para ler contatos do **Supabase** e enviar mensagens automáticas via **Z-API**.

## 1. Setup da Tabela (Supabase)

No **SQL Editor** do Supabase, crie a tabela e insira os contatos de teste (máximo de 3 para o escopo deste desafio):

```sql
create table contacts (
  id serial primary key,
  name text not null,
  phone text not null
);

insert into contacts (name, phone) values 
  ('Marcelo Baldi (CEO da b2bflow)', '5511994084809');
```

## 2. Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto (use o `.env.example` como base) e preencha com as suas credenciais:

```env
# Configurações do Supabase
SUPABASE_URL=https://<SUA-URL>.supabase.co
SUPABASE_KEY=<SUA-CHAVE-ANON-PUBLICA>

# Configurações da Z-API
ZAPI_INSTANCE_ID=<SEU-ID-DE-INSTANCIA>
ZAPI_TOKEN=<SEU-TOKEN-ZAPI>
ZAPI_CLIENT_TOKEN=
```

## 3. Como Rodar

1. Crie o ambiente virtual e instale as dependências:
```bash
python -m venv venv
venv\Scripts\activate   # No Windows (use "source venv/bin/activate" no Mac/Linux)
pip install -r requirements.txt
```

2. Execute o script principal:
```bash
python main.py
```

O script buscará os contatos na tabela e registrará no console o envio bem-sucedido das mensagens pelo WhatsApp!
