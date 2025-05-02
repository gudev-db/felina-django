# Felina Django

Aplicação de chat com IA integrada à base de dados AstraDB para busca de informações baseada em vetores.

## Características

- Interface de chat estilizada com Tailwind CSS
- Integração com OpenAI para embeddings e geração de respostas
- Integração com AstraDB para busca vetorial
- Aplicação Django para gerenciamento de usuários e histórico de chats

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/gudev-db/felina-django.git
cd felina-django
```

2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

4. Instale o Tailwind CSS:
```bash
python manage.py tailwind install
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

7. Em outro terminal, inicie o servidor Tailwind (para desenvolvimento):
```bash
python manage.py tailwind start
```

## Uso

Acesse a aplicação em `http://127.0.0.1:8000/` e comece a conversar com o assistente para obter informações sobre o LASID (Laboratório de Sistemas Dinâmicos).
