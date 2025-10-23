import re
from datetime import datetime

def validate_login(login: str, existing_user=None) -> tuple[bool, str | None]:
    """
    Validate user's login. Ensure it is not empty, it contains only letters, numbers or _ and - signs. It has to be at least 6 and 20 characters.
    """
    if not login:
        return False, 'Login cannot be empty.'
    if existing_user:
        return False, 'Username already in use.'
    if len(login) < 6 or len(login) > 20:
        return False, 'Login must be between 6 and 20 characters.'
    if not re.match(r"^[a-zA-Z0-9_-]+$", login):
        return False, 'Login can contain only letters, numbers, - or _.'
    return True, None


def validate_password(password: str) -> tuple[bool, str | None]:
    """
    Validate user's password. Ensures it contains lowercase and uppercase letter, special character and a number. It must be between 8 and 18 characters.
    """
    if not password:
        return False, "Password cannot be empty!"
    if len(password) < 8 or len(password) > 18:
        return False, "Password must be between 8 to 18 characters."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain lowercase letter."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain uppercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain a number."
    if not re.search(r"[@$!%*#?&]", password):
        return False, "Password must contain a special character."
    return True, None


def validate_title(title: str) -> tuple[bool, str | None]:
    """
    Validate title. Ensures it's not empty, doesn't contain special characters. Makes sure it is at least 2 and 150 characters.
    """
    if not title.strip():
        return False, "Title cannot be empty, please type correct title."
    if len(title) < 2 or len(title) > 150:
        return False, "Title must be between 2 and 150 characters."
    if re.search(r"[@$!%*#?&]", title):
        return False, "Name cannot contain special characters."
    return True, None


def validate_pages(pages: str) -> tuple[bool, str | None]:
    """
    Validate pages in a book. Ensure it's not empty and it contains only numbers and is max 4 characters.
    """
    if not pages.strip():
        return False, "It cannot be empty, put a number of pages."
    if not pages.isdigit() or len(pages) > 4:
        return False, "It can be only digits, it cannot be longer than 4 characters."
    return True, None
    

def validate_user_name(name: str) -> tuple[bool, str | None]:
    """
    Validate user's full name. Ensures it doesn't contain special characters or numbers. Makes sure it is at least 2 and 150 characters.
    """
    if not name.strip():
        return False, "Name cannot be empty, type your full name"
    if len(name) <2 or len(name) > 150:
        return False, "Name must be between 2 or 150 characters."
    if re.search(r"\d", name):
        return False, "Name cannot contain numbers."
    if re.search(r"[@$!%*#?&]", name):
        return False, "Name cannot contain special characters."
    return True, None


def validate_birth_date(birth_date: str) -> tuple[bool, str | None]:
    """
    Validate user's birth date input.
    Accepted formats: DD-MM-YYYY, DD/MM/YYYY, DD MM YYYY, DDMMYYYY.
    Ensures that the date isn't in the future and it's real.
    """
    if not birth_date.strip():
        return False, "Birth date cannot be empty, please ensure it's DD-MM-YYYY"
    
    formats = ("%d-%m-%Y", "%d%m%Y", "%d/%m/%Y", "%d %m %Y")
    parsed_date = None
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(birth_date, fmt)
            break
        except ValueError:
            continue
        
    if not parsed_date:
        return False, "Invalid date time. Use DD-MM-YYYY or DD/MM/YYYY format."
    
    if parsed_date > datetime.now():
        return False, "Birth date cannot be in the future."
    return True, None


def validate_address(address: str) -> tuple[bool, str | None]:
    """
    Validate user's address input. Ensure it's not empty, it contains only letters, spaces, and hyphens, it's between 2 and 150 characters.
    """
    if not address.strip():
        return False, "Address cannot be empty. Please insert correct address."
    if len(address) < 2 or len(address) > 150:
        return False, "Address cannot be shorter than 2 characters or longer than 150."
    if not re.match(r"^[A-Za-zÀ-ÿ\s-]+$", address):
        return False, "Address can only contain letters, spaces, and hyphens."
    return True, None


def validate_postal_code(postal_code: str) -> tuple[bool, str | None]:
    """
    Validate user's postal code input. Ensures it's not empty, it is between 4 and 10 characters and has valid format 01-234 or 01234.
    """
    if not postal_code.strip():
        return False, "Postal code cannot be empty."
    if len(postal_code) < 4 or len(postal_code) > 10:
        return False, "Postal code cannot be shorter than 4 characters or longer than 10."
    if not re.match(r"^\d{2}-?\d{3}$", postal_code): # PL
        return False, "Invalid postal code. Use 01-234 or 01234"
    return True, None

def validate_loan_date(loan_date: str) -> tuple[bool, str | None]:
    """
    Validate user's loan_date input.
    Accepted formats: DD-MM-YYYY, DD/MM/YYYY, DD MM YYYY, DDMMYYYY.
    Ensures that the date isn't in the future and it's real.
    """
    if not loan_date.strip():
        return False, "Loan date cannot be empty, please insert correcte date (DD/MM/YYYY)"
    
    formats = ("%d-%m-%Y", "%d%m%Y", "%d/%m/%Y", "%d %m %Y")
    parsed_date = None
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(loan_date, fmt)
            break
        except ValueError:
            continue

    if not parsed_date:
        return False, "Invalid date time. Use DD-MM-YYYY or DD/MM/YYYY format."
    
    if parsed_date > datetime.now():
        return False, "Date cannot be in the future."
    return True, None