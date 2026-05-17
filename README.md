# Sistema Bancario API ??
API RESTful assincrona desenvolvida com **FastAPI** para gerenciamento de operacoes bancarias de depositos e saques vinculados a contas correntes.
## ??? Tecnologias Utilizadas
- **FastAPI**: Framework web moderno e assincrono.
- **SQLAlchemy & AIOSQLite**: ORM e banco de dados rodando em modo assincrono.
- **Pydantic v2**: Validacao de dados estruturados.
- **Passlib & Python-Jose**: Criptografia de senhas e geracao de tokens JWT.
## ?? Como Executar o Projeto
1. Instale as dependencias:
\\\ash
pip install fastapi uvicorn sqlalchemy aiosqlite pydantic passlib[bcrypt] python-jose[cryptography] python-multipart
\\\
2. Inicie o servidor Uvicorn:
\\\ash
python -m uvicorn main:app --reload
\\\
3. Acesse a documentacao interativa do Swagger em: [http://127.0.0](http://127.0.0)
