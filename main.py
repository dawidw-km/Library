from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker, relationship, Mapped, mapped_column
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
import validators, security

engine = create_engine("postgresql+psycopg2://postgres@localhost:5432/test_db", echo=True)

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[str] = mapped_column(nullable=False)

    books: Mapped[List["Book"]] = relationship('Book', back_populates='author')

class Book(Base):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    pages: Mapped[int] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))

    author: Mapped["Author"] = relationship('Author', back_populates='books')
    loans: Mapped[List["Loan"]] = relationship('Loan', back_populates='book')

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    postal_code: Mapped[str] = mapped_column(nullable=False)

    loans: Mapped[List['Loan']] = relationship('Loan', back_populates='user')

class Worker(Base):
    __tablename__ = 'workers'
    id: Mapped[int] = mapped_column(primary_key=True)
    login:Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[str] = mapped_column(nullable=False)   
    address: Mapped[str] = mapped_column(nullable=False)
    postal_code: Mapped[str] = mapped_column(nullable=False)

    loans: Mapped[List['Loan']] = relationship('Loan', back_populates='worker')

class Loan(Base):
    __tablename__ = 'loans'
    id: Mapped[int] = mapped_column(primary_key=True)
    loan_date: Mapped[str] = mapped_column(nullable=False)
    return_date: Mapped[str] = mapped_column(nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id'))

    book: Mapped['Book'] = relationship('Book', back_populates='loans')
    user: Mapped['User'] = relationship('User', back_populates='loans')
    worker: Mapped['Worker'] = relationship('Worker', back_populates='loans')

    

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_valid_input(prompt: str, validator_func, existing_user=None) ->str:
    """
    Collects user input and takes validator.
    """
    while True:
        value = input(prompt)
        if existing_user is not None:
            valid = validator_func(value, existing_user)
        else:
            valid = validator_func(value)
        if valid:
            return value
        print("Try again\n")

def get_user_details() -> tuple:
    """
    Collects user inforomation (Name, Birth date, Address, Postal code) and validates input.
    """
    name_i = get_valid_input("Full name: ", validators.validate_user_name)
    birth_date_i = get_valid_input("Birth date format(DD/MM/YYYY): ", validators.validate_birth_date)
    address_i = get_valid_input("Address: ", validators.validate_address)
    postal_code_i = get_valid_input("Postal code 01-234 or 01234 format: ", validators.validate_postal_code)
    
    return name_i, birth_date_i, address_i, postal_code_i

def create_account(model):
    while True:
        login_i = get_valid_input("Login: ", validators.validate_login)
        existing_user = session.execute(select(Worker).where(Worker.login == login_i)).scalar_one_or_none()
        if existing_user:
            print("Login already exists. Try another.\n")
        else:
            break

    password_i = get_valid_input("Password: ", validators.validate_password)
    hashed_pw = security.hashed_password(password_i)

    name_i, birth_date_i, address_i, postal_code_i = get_user_details()
    
    try:
        account = model(
            login=login_i,
            password=hashed_pw,
            name=name_i,
            birth_date=birth_date_i,
            address=address_i,
            postal_code=postal_code_i
        )
        session.add(account)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error, the worker hasn't been added.{e}")

def new_user():
    create_account(User)


def new_worker():
    create_account(Worker)

def login_as(model):
    login_input = input("Login: ")
    password_input = input("Password: ")

    query_check = select(model).where(model.login == login_input)
    result = session.execute(query_check).scalar_one_or_none()

    hashed_pw = result.password

    security.verify_password(password_input, hashed_pw)

    if security.verify_password(password_input, hashed_pw):
        print("Done")
    else:
        print("Invalid login or password.")

def login_user():
    login_as(User)

def login_worker():
    login_as(Worker)

while True:
    #ASK WHAT DO YOU WANT TO DO
    login_register = input("1.Login 2.Register \q Exit: ")

    #LOGIN AS USER OR WORKER
    if login_register == '1':
        worker_user = input("Do you want to login as 1.User or 2.Worker? ")
        if worker_user == '1':
            login_user()
        elif worker_user == '2':
            login_worker()

    #REGISTER AS USER OR WORKER
    elif login_register == '2':
        worker_user = input("1.User or 2.Worker type of account? ")
        if worker_user == '1':
            new_user()
        elif worker_user == '2':
            new_worker()

    #BREAKS THE LOOP
    elif login_register == '\q':
        break

