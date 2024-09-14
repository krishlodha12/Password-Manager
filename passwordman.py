import hashlib 
import getpass
import random
import string

password_manager = {}

def generate_password(length: int = 12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(alphabet) for _ in range(length))
    return password

def create_account():
    while True:
        username = input("Enter your desired username: ")
        if username in password_manager:
            print("This username already exists. Please choose a different one.")
        else:
            break
    
    use_generated = input("Would you like to use a randomly generated password? (y/n): ").lower()
    
    if use_generated == 'y':
        password = generate_password()
        print(f"Your generated password is: {password}")
        print("Please make sure to save this password securely.")
    else:
        password = getpass.getpass("Enter your desired password: ")
    
    security_question = input("Enter a security question: ")
    security_answer = input("Enter the answer to your security question: ")
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    hashed_answer = hashlib.sha256(security_answer.lower().encode()).hexdigest()
    
    password_manager[username] = {
        'password': hashed_password,
        'security_question': security_question,
        'security_answer': hashed_answer
    }
    print("Account created successfully!")

def login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    if username in password_manager and password_manager[username]['password'] == hashed_password:
        print("Login successful!")
        return username
    else:
        print("Invalid username or password.")
        return None

def update_password(username):
    print(f"Security Question: {password_manager[username]['security_question']}")
    answer = input("Enter the answer to your security question: ")
    hashed_answer = hashlib.sha256(answer.lower().encode()).hexdigest()
    
    if hashed_answer == password_manager[username]['security_answer']:
        new_password = getpass.getpass("Enter your new password: ")
        hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
        password_manager[username]['password'] = hashed_new_password
        print("Password updated successfully!")
    else:
        print("Incorrect answer to security question. Password not updated.")

def main():
    while True:
        choice = input("Enter 1 to create an account, 2 to login, 3 to update password, or 0 to exit: ")
        if choice == "1":
            create_account()
        elif choice == "2":
            logged_in_user = login()
            if logged_in_user:
                update_choice = input("Would you like to update your password? (y/n): ").lower()
                if update_choice == 'y':
                    update_password(logged_in_user)
        elif choice == "3":
            username = input("Enter your username: ")
            if username in password_manager:
                update_password(username)
            else:
                print("Username not found.")
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()