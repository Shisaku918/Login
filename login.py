import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from database_login_handler import DatabaseLoginHandler
from app import App
from admin_app import AppAdmin

class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_label = QLabel(self)
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "background-dark.png"))
        self.background_label.setStyleSheet("border: 3px solid black;")
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)

    def resizeEvent(self, event):
        self.background_label.setGeometry(self.rect())

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.db_handler = DatabaseLoginHandler("database_login.db")
        self.app_window = None  # Ajoutez cet attribut
        self.app_admin_window = None

    def initUI(self):
        self.setGeometry(600, 200, 400, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        main_layout = QVBoxLayout(self)
        main_widget = BackgroundWidget(self)
        widget_layout = QVBoxLayout(main_widget)
        main_widget.setLayout(widget_layout)
        main_layout.addWidget(main_widget)

        user_layout = QVBoxLayout()
        self.user_label = QLabel(self)
        self.user_label.setStyleSheet("margin-top: 50px; margin-bottom: 50px;")
        user_layout.addWidget(self.user_label, alignment=Qt.AlignCenter)
        self.user_image()
        widget_layout.addLayout(user_layout)

        fields_layout = QVBoxLayout()

        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("  Your Username...")
        self.username_field.setStyleSheet("background-color: #757875; color: white; border: 2px solid blue; border-radius: 30px;")
        self.username_field.setFixedHeight(60)
        self.username_field.setFixedWidth(250)
        fields_layout.addWidget(self.username_field, alignment=Qt.AlignCenter)

        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("  Your Password...")
        self.password_field.setStyleSheet("background-color: #757875; color: white; border: 2px solid blue; border-radius: 30px;")
        self.password_field.setFixedHeight(60)
        self.password_field.setFixedWidth(250)
        fields_layout.addWidget(self.password_field, alignment=Qt.AlignCenter)

        self.password_check_field = QLineEdit(self)
        self.password_check_field.setPlaceholderText("  Verify Password...")
        self.password_check_field.setStyleSheet("background-color: #757875; color: white; border: 2px solid blue; border-radius: 30px;")
        self.password_check_field.setFixedHeight(60)
        self.password_check_field.setFixedWidth(250)
        self.password_check_field.setVisible(False)
        fields_layout.addWidget(self.password_check_field, alignment=Qt.AlignCenter)

        widget_layout.addLayout(fields_layout)

        # Créer le layout pour les boutons "Se connecter" et "Sign Up"
        connect_signup_layout = QVBoxLayout()
        self.connect_button = QPushButton("Se connecter")
        self.connect_button.setStyleSheet("padding-left: 30px; padding-right: 30px; border: 1px solid black; border-radius: 7px; background-color: blue;")
        self.connect_button.clicked.connect(self.validate_and_login)
        connect_signup_layout.addWidget(self.connect_button, alignment=Qt.AlignCenter)

        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("color: #09e8dd; border: none; text-decoration: underline;")
        signup_button.clicked.connect(self.toggle_signup)
        connect_signup_layout.addWidget(signup_button, alignment=Qt.AlignCenter)
        self.signup_button = signup_button

        # Ajoutez le layout des boutons "Se connecter" et "Sign Up" à la mise en page principale
        widget_layout.addLayout(connect_signup_layout)

        # Ajoutez le bouton "Sign Up" à la mise en page principale
        widget_layout.addWidget(signup_button, alignment=Qt.AlignCenter)

        # Créer le layout pour les boutons "Back" et "Create Account"
        back_create_layout = QVBoxLayout()

        # Ajoutez le layout des boutons "Back" et "Create Account" à la mise en page principale
        widget_layout.addLayout(back_create_layout)


        # Créer le layout pour les boutons "Back" et "Create Account"
        back_create_layout = QVBoxLayout()
        self.create_button = QPushButton("Create Account")
        self.create_button.setStyleSheet("padding-left: 30px; padding-right: 30px; border: 1px solid black; border-radius: 7px; background-color: blue;")
        self.create_button.setVisible(False)
        self.create_button.clicked.connect(self.sign_up)
        back_create_layout.addWidget(self.create_button, alignment=Qt.AlignCenter)

        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("padding-left: 30px; padding-right: 30px; border: 1px solid black; border-radius: 7px; background-color: blue;")
        self.back_button.setVisible(False)
        self.back_button.clicked.connect(self.cancel_account_creation)
        back_create_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        # Ajoutez le layout des boutons "Back" et "Create Account" à la mise en page principale
        widget_layout.addLayout(back_create_layout)

    def validate_and_login(self):
        # Obtenez le contenu des champs de texte
        username = self.username_field.text()
        password = self.password_field.text()

        if username and password:
            if self.db_handler.user_exists_with(username):
                stored_password = self.db_handler.password_for(username)
                stored_role = self.db_handler.role_for(username)
                if stored_password == password:
                    if stored_role == "admin":
                        print("Connecté avec succès en tant qu'administrateur !")

                        if self.app_admin_window is None:
                            self.app_admin_window = AppAdmin(username)
                        self.app_admin_window.show()
                        self.hide()
                    else:
                        print("Connecté avec succès !")

                        if self.app_window is None:
                            self.app_window = App(username)
                        self.app_window.show()
                        self.hide()
                else:
                    # Mot de passe incorrect
                    print("Mot de passe incorrect.")
            else:
                # Compte inexistant
                print("Compte inexistant.")
            

    def user_image(self):
        self.user_path = os.path.join(os.path.dirname(__file__), "user.png")
        pixmap = QPixmap(self.user_path)
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
        self.user_label.setPixmap(pixmap)

    def toggle_signup(self):
        self.password_check_field.setVisible(not self.password_check_field.isVisible())
        if self.password_check_field.isVisible():
            self.signup_button.setVisible(False)
            self.connect_button.setVisible(False)  # Masquer le bouton "Se connecter"
            self.create_button.setVisible(True)
            self.back_button.setVisible(True)
        else:
            self.signup_button.setVisible(True)
            self.connect_button.setVisible(True)  # Rendre le bouton "Se connecter" visible
            self.create_button.setVisible(False)
            self.back_button.setVisible(False)

    def sign_up(self):
        # Obtenez le contenu des champs de texte
        username = self.username_field.text()
        password = self.password_field.text()
        password_check = self.password_check_field.text()

        if self.password_check_field.isVisible():
            if not password_check:
                print("Veuillez remplir le champ de vérification de mot de passe.")
                return
            elif password != password_check:
                print("Les mots de passe ne correspondent pas.")
                return

        if username and password:
            if self.db_handler.user_exists_with(username):
                print("Le nom d'utilisateur existe déjà.")
            else:
                if self.db_handler.create_person(username, password):
                    print("\nCompte créé avec succès !\n")
                    self.password_field.clear()
                    self.username_field.clear()
                    self.password_check_field.clear()
                else:
                    print(f"\nLe nom d'utilisateur '{username}' est indisponible. Veuillez choisir un nom d'utilisateur différent.\n")
        else:
            print("Veuillez remplir tous les champs.")

    def cancel_account_creation(self):
        self.connect_button.setVisible(True)
        self.signup_button.setVisible(True)
        self.create_button.setVisible(False)
        self.back_button.setVisible(False)

        self.password_check_field.setVisible(False)


    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
        else:
            self.dragPos = None

    def mouseMoveEvent(self, event):
        if self.dragPos:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())


