import re
from datetime import datetime

def validate_login(login: str, existing_user=None) ->bool:
    """
    Validate user's login. Ensure it is not empty, it contains only letters, numbers or _ and - signs. It has to be at least 6 and 20 characters.
    """
    if not login:
        print('Login cannot be empty.')
        return False
    if existing_user:
        print('Username already in use.')
        return False
    if len(login) < 6 or len(login) > 20:
        print('Login must be between 6 do 20 characters.')
        return False
    if not re.match(r"^[a-zA-Z0-9_-]+$", login):
        print("Login can contain only letters, numbers, - or _.")
        return False
    return True


def validate_password(password: str) ->bool:
    """
    Validate user's password. Ensures it contains lowercase and uppercase letter, special character and a number. It must be between 8 and 18 characters.
    """
    if not password:
        print("Password cannot be empty!")
        return False
    if len(password) <8 or len(password) >18:
        print("Password must be between 8 to 18 characters.")
        return False
    if not re.search(r"[a-z]", password):
        print("Password must contain lowercase letter.")
        return False
    if not re.search(r"[A-Z]", password):
        print("Password must contain uppercase letter.")
        return False
    if not re.search(r"\d", password):
        print("Password must contain a number.")
        return False
    if not re.search(r"[@$!%*#?&]", password):
        print("Password must contain a special character.")
        return False
    return True


def validate_title(title: str) ->bool:
    """
    Validate title. Ensures it's not empty, doesn't contain special characters. Makes sure it is at least 2 and 150 characters.
    """
    if not title.strip():
        print("Title cannot be empty, please type correct title.")
        return False
    if len(title) < 2 or len(title) > 150:
        print("Title must be between 2 and 150 characters.")
        return False
    if re.search(r"[@$!%*#?&]", title):
        print("Name cannot contain special characters.")
        return False
    return True


def validate_pages(pages: str) ->bool:
    """
    Validate pages in a book. Ensure it's not empty and it contains only numbers and is max 4 characters.
    """
    if not pages.strip():
        print("It cannot be empty, put a number of pages.")
        return False
    if len(pages) > 4:
        print("It cannot be longer than 4 chracters.")
        return False
    if not re.search(r"^\d+$", pages):
        print("Pages can contain only numbers.")
        return False
    return True
    


def validate_user_name(name: str) ->bool:
    """
    Validate user's full name. Ensures it doesn't contain special characters or numbers. Makes sure it is at least 2 and 150 characters.
    """
    if not name.strip():
        print("Name cannot be empty, type your full name")
        return False
    if len(name) <2 or len(name) > 150:
        print("Name must be between 2 or 150 characters.")
        return False
    if re.search(r"\d", name):
        print("Name cannot contain numbers.")
        return False
    if re.search(r"[@$!%*#?&]", name):
        print("Name cannot contain special characters.")
        return False
    return True


def validate_birth_date(birth_date: str) ->bool:
    """
    Validate user's birth date input.
    Accepted formats: DD-MM-YYYY, DD/MM/YYYY, DD MM YYYY, DDMMYYYY.
    Ensures that the date isn't in the future and it's real.
    """
    if not birth_date.strip():
        print("Birth date cannot be empty, please ensure it's DD-MM-YYYY")
        return False
    
    formats = ("%d-%m-%Y", "%d%m%Y", "%d/%m/%Y", "%d %m %Y")
    parsed_date = None
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(birth_date, fmt)
            break
        except ValueError:
            continue
        
    if not parsed_date:
        print("Invalid date time. Use DD-MM-YYYY or DD/MM/YYYY format.")
        return False
    
    if parsed_date > datetime.now():
        print("Birth date cannot be in the future.")
        return False
    return True


def validate_address(address: str) ->bool:
    """
    Validate user's address input. Ensure it's not empty, it contains only letters, spaces, and hyphens, it's between 2 and 150 characters.
    """
    if not address.strip():
        print("Address cannot be empty. Please insert correct address.")
        return False
    if len(address) < 2 or len(address) > 150:
        print("Address cannot be shorter than 2 characters or longer than 150.")
        return False
    if not re.match(r"^[A-Za-zÀ-ÿ\s-]+$", address):
        print("Address can only contain letters, spaces, and hyphens.")
        return False
    return True


def validate_postal_code(postal_code: str) ->bool:
    """
    Validate user's postal code input. Ensures it's not empty, it is between 4 and 10 characters and has valid format 01-234 or 01234.
    """
    if not postal_code.strip():
        print("Postal code cannot be empty.")
        return False
    if len(postal_code) < 4 or len(postal_code) > 10:
        print("Postal code cannot be shorter than 4 characters or longer than 10.")
        return False
    if not re.match(r"^\d{2}-?\d{3}$", postal_code): # PL
        print("Invalid postal code. Use 01-234 or 01234")
        return False
    return True