from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import models, schemas, security
from fastapi import HTTPException, status

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    result = await db.execute(select(models.User).where(models.User.username == user.username))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    
    hashed_pw = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def create_transaction(db: AsyncSession, user: models.User, tx: schemas.TransactionCreate):
    if tx.type == "WITHDRAW" and user.balance < tx.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Saldo insuficiente para a operação")
    
    if tx.type == "DEPOSIT":
        user.balance += tx.amount
    elif tx.type == "WITHDRAW":
        user.balance -= tx.amount
        
    db_tx = models.Transaction(user_id=user.id, type=tx.type, amount=tx.amount)
    db.add(db_tx)
    await db.commit()
    await db.refresh(db_tx)
    return db_tx

async def get_statement(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.User)
        .where(models.User.id == user_id)
        .options(selectinload(models.User.transactions))
    )
    return result.scalars().first()
