from database_login_handler import DatabaseLoginHandler

database_handler = DatabaseLoginHandler("database_login.db")

def sign_in():
    print("---Sign In---")
    username = input("Username: ")
    password = input("Password: ")

    if database_handler.user_exists_with(username) and password == database_handler.password_for(username):
        print("\nSuccessfully connected !\n")
        menu_connected(username)
    else:
        print("\nFailed connection, incorrect identifier(s).\n")

def sign_up():
    print("---Sign Up---")
    username = input("Username: ")
    password = input("Password: ")
    password_check = input("Verify your password: ")

    if password != password_check:
        print("Les mots de passe sont différents.")
    else:
        if database_handler.create_person(username, password):
            print("\nSuccessfully created account!\n")
            menu_connected(username)
        else:
            print(f"\nThe username '{username}' is unavailable. Please choose a different username.\n")

def change_password(username: str):
    new_password = input("New password: ")
    new_password_check = input("Verify your new password: ")
    if new_password != new_password_check:
        print("Les mots de passe sont différents.")
    else:
        database_handler.change_password(username, new_password)
        print("\nYour password has been successfully changed !\n")

def delete_account(username: str):
    print("\nÊtes-vous sûr de vouloir faire ça ?\n")
    print("1. Oui")
    print("2. Non")
    check = input("\n")

    if check == "1":
        database_handler.delete_account(username)
        quit()
    else:
        pass

def menu_connected(username: str):
    while True:
        print("\nBienvenue sur MyLogin ! (connected)\n")
        print("1. Sign Out")
        print("2. Change your password")
        print("3. Delete your account")
        choice = int(input("\n"))

        match choice:
            case 1:
                print("\nDisconnection successful.\n")
                return
            case 2:
                change_password(username)
            case 3:
                delete_account(username)

def menu_not_connected():
    while True:
        print("Bienvenue sur MyLogin ! (not connected)")
        print("Veuillez choisir une option\n")
        print("1. Sign In")
        print("2. Sign Up")
        print("3. Exit")
        choice = int(input("\n"))

        match choice:
            case 1:
                sign_in()
            case 2:
                sign_up()
            case 3:
                break
            case _:
                print("Veuillez choisir une proposition valide.")

menu_not_connected()
