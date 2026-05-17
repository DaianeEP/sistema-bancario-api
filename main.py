from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import models, schemas, crud, security
from database import engine, Base, get_db
app = FastAPI(
    title="API Bancaria Assincrona",
    description="API RESTful para depositos, saques e extratos bancarios.",
    version="1.0.0"
)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
@app.post("/auth/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["Autenticacao"])
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, user)
@app.post("/auth/token", response_model=schemas.Token, tags=["Autenticacao"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    from sqlalchemy.future import select
    result = await db.execute(select(models.User).where(models.User.username == form_data.username))
    user = result.scalars().first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuario ou senha incorretos")
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
@app.post("/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED, tags=["Operacoes Bancarias"])
async def financial_operation(
    tx: schemas.TransactionCreate,
    current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_transaction(db, current_user, tx)
@app.get("/transactions/statement", response_model=schemas.StatementResponse, tags=["Operacoes Bancarias"])
async def get_bank_statement(
    current_user: Annotated[models.User, Depends(security.get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    user_data = await crud.get_statement(db, current_user.id)
    return {
        "balance": user_data.balance,
        "transactions": user_data.transactions
    }
