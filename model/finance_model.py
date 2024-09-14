
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    amount = Column(Float)
    is_expense = Column(Boolean)

engine = create_engine('sqlite:///finance_manager.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def add_transaction(title, amount, is_expense):
    try:
        with Session() as session:
            transaction = Transaction(title=title, amount=amount, is_expense=is_expense)
            session.add(transaction)
            session.commit()
    except Exception as e:
        print(f"Erro ao editar: {e}")

def get_transactions():
    try:
        with Session() as session:
            return session.query(Transaction).all()
    except Exception as e:
        print(f"erro: {e}")

def delete_transaction(transaction_id):
    try:
        with Session() as session:
            transaction = session.query(Transaction).filter_by(id=transaction_id).first()
            if transaction:
                session.delete(transaction)
                session.commit()
            else:
                print(f"Transaction com o ID {transaction_id} não encontrada")
    except Exception as e:
        print(f"Erro ao deletar: {e}")

def update_transaction(transaction_id, title, amount, is_expense):
    try:
        with Session() as session:
            transaction = session.query(Transaction).filter_by(id=transaction_id).first()
            if transaction:
                transaction.title = title
                transaction.amount = amount
                transaction.is_expense = is_expense
                session.commit()
            else:
                print(f"Transaction com o ID {transaction_id} não encontrada")
    except Exception as e:
        print(f"Erro ao atualizar: {e}")

def get_balance():
    try:
        with Session() as session:
            expenses = session.query(Transaction).filter_by(is_expense=True).all()
            income = session.query(Transaction).filter_by(is_expense=False).all()
            total_expenses = sum(t.amount for t in expenses)
            total_income = sum(t.amount for t in income)
            return total_income - total_expenses, total_expenses, total_income
    except Exception as e:
        print(f"Erro ao calcular o balanço: {e}")
