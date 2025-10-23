from sqlalchemy import create_engine, ForeignKey, select, func
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker, relationship, Mapped, mapped_column
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
import validators, security

engine = create_engine("postgresql+psycopg2://postgres@localhost:5432/test_db")

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


def get_valid_input(prompt: str, validator_func, *args) ->str:
    """
    Collects user input and uses the provided validator.
    """
    while True:
        value = input(prompt)
        is_valid, message = validator_func(value, *args)
        if is_valid:
            return value
        print(message)
        

def get_user_details() -> tuple:
    """
    Collects user information (Name, Birth Date, Address, Postal code) and validates input.
    """
    name_i = get_valid_input("Full name: ", validators.validate_user_name)
    birth_date_i = get_valid_input("Birth date format(DD/MM/YYYY): ", validators.validate_birth_date)
    address_i = get_valid_input("Address: ", validators.validate_address)
    postal_code_i = get_valid_input("Postal code 01-234 or 01234 format: ", validators.validate_postal_code)
    
    return name_i, birth_date_i, address_i, postal_code_i

def add_author():
    """
    Adds new author to the database. Ensure there's no duplicate of the author.
    """
    name_i = get_valid_input("Full name: ", validators.validate_user_name)
    birth_date_i = get_valid_input("Birth date, format DD/MM/YYYY: ", validators.validate_birth_date)
    query = select(Author).where(func.lower(Author.name) == name_i.lower())
    result = session.execute(query).scalar_one_or_none()

    if result:
        print("Name already in the database.")
        return
    
    try:
        author = Author(
            name=name_i,
            birth_date=birth_date_i
        )
        session.add(author)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error, the author hasn't been added.{e}")

def add_book():
    """
    Adds new book to the database. Ensure there's no duplcate and makes sure that author is already in the database.
    """
    title_i = get_valid_input("Title of the book: ", validators.validate_title)
    query_title = select(Book).where(Book.title == title_i)
    title_result = session.execute(query_title).scalars().first()

    if title_result:
        print("Title already in the database.")
        return

    pages_i = get_valid_input("Number of pages: ", validators.validate_pages)
    pages_i_int = int(pages_i)
    author_name_i = input("Author's name: ").strip()

    if not author_name_i:
        print("Author's name cannot be empty.")
        return

    query = select(Author).where(Author.name == author_name_i)
    author = session.execute(query).scalar_one_or_none()

    if author is None:
        print("Author doesn't exist in the database. Add author first.")
        return

    author_id_result = author.id

    try:
        book = Book(
            title=title_i,
            pages=pages_i_int,
            author_id=author_id_result
        )
        session.add(book)
        session.commit()
        print("Book added successfully.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error, the book hasn't been added to the database.{e}")


def create_account(model):
    """
    Model to create an account for a user or a worker.
    Ensure that an account doesn't already exist in the database.
    Secures password with bcrypt.
    """
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
    """
    Model to log in as a worker or a user.
    Ensure that pw and login are correct.
    Decrypts password.
    """
    login_input = input("Login: ")
    password_input = input("Password: ")

    if not login_input or not password_input:
        print("Login and password cannot be empty!")
        return False

    login_query = select(model).where(model.login == login_input)
    result = session.execute(login_query).scalar_one_or_none()

    if result is None:
        print("No account was found with that login.")
        return False

    hashed_pw = result.password

    is_valid = security.verify_password(password_input, hashed_pw)

    if is_valid:
        print(f"Login successful, welcome {result.name}!")
        return True
    else:
        print("Invalid login or password.")
        return False
    

def login_user():
    return login_as(User)

def login_worker():
    return login_as(Worker)

while True:
    #ASK WHAT DO YOU WANT TO DO
    login_register = input("1.Login 2.Register or type 'exit': ")

    #LOGIN AS USER OR WORKER
    if login_register == '1':
        worker_user = input("Do you want to login as 1.User or 2.Worker? ")
        if worker_user == '1':
            login_user()
        elif worker_user == '2':
            logged_in_worker = login_worker()
            if logged_in_worker:
                while True:
                    choice = input("What do you want to do? 1.Add author 2.Add book or type 'exit': ")
                    if choice == '1':
                        add_author()
                    elif choice == '2':
                        add_book()
                    elif choice == "exit":
                        break

    #REGISTER AS USER OR WORKER
    elif login_register == '2':
        worker_user = input("1.User or 2.Worker type of account? ")
        if worker_user == '1':
            new_user()
        elif worker_user == '2':
            new_worker()

    #BREAKS THE LOOP
    elif login_register == 'exit':
        break

