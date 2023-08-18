import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout, QGridLayout, QDialog, QInputDialog, QMessageBox
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from database_login_handler import DatabaseLoginHandler

class App(QWidget):
    def __init__(self, username: str):
        super().__init__()
        self.initUI(username)
        self.db_handler = DatabaseLoginHandler("database_login.db")


    def initUI(self, username: str):
        self.setGeometry(600, 200, 600, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("border: 3px solid white; border-radius: 15px;")

        main_layout = QVBoxLayout(self)
        main_widget = QWidget(self)
        widget_layout = QVBoxLayout(main_widget)
        widget_layout.setAlignment(Qt.AlignCenter)  # Alignement au centre
        main_widget.setLayout(widget_layout)
        main_layout.addWidget(main_widget)

        name_label = QLabel(f"Welcome, {username}!")  # Ajout du texte statique
        name_label.setStyleSheet("border: none;")
        name_label_font = QFont("Arial", 20)
        name_label.setFont(name_label_font)
        widget_layout.addWidget(name_label)
        
        # Ajoutez trois boutons côte à côte
        buttons_layout = QHBoxLayout()

        param_button = QPushButton("Paramètres")
        param_button.setStyleSheet("background-color: green; color: white; border: none; border-radius: 5px; padding: 2px;")
        param_button.clicked.connect(lambda: self.open_settings(username))
        buttons_layout.addWidget(param_button)

        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("background-color: gray; color: white; border: none; border-radius: 5px; padding: 2px;")
        exit_button.clicked.connect(self.exit)
        buttons_layout.addWidget(exit_button)
    
        
        widget_layout.addLayout(buttons_layout)

        self.setLayout(widget_layout)

    def change_password(self, username: str):
        dialog = QDialog(self)
        dialog.setWindowTitle("Change Password")
        layout = QVBoxLayout()

        new_password_label = QLabel("Enter new password:")
        new_password_input = QLineEdit()
        new_password_label.setStyleSheet("border: none;")
        new_password_input.setStyleSheet("border: none;")
        layout.addWidget(new_password_label)
        layout.addWidget(new_password_input)

        verify_new_password_label = QLabel("Verify new password:")
        verify_new_password_input = QLineEdit()
        verify_new_password_label.setStyleSheet("border: none;")
        verify_new_password_input.setStyleSheet("border: none;")
        layout.addWidget(verify_new_password_label)
        layout.addWidget(verify_new_password_input)

        current_password_label = QLabel("Enter your current password:")
        current_password_input = QLineEdit()
        current_password_label.setStyleSheet("border: none;")
        current_password_input.setStyleSheet("border: none;")
        layout.addWidget(current_password_label)
        layout.addWidget(current_password_input)

        confirm_button = QPushButton("Confirm")
        layout.addWidget(confirm_button)

        dialog.setLayout(layout)

        def confirm_change():
            new_password = new_password_input.text()
            verify_password = verify_new_password_input.text()
            current_password = current_password_input.text()

            if new_password == verify_password:
                if current_password == self.db_handler.password_for(username):
                    self.db_handler.change_password(username, new_password)
                    QMessageBox.information(self, "Success", "Password changed successfully.")
                    dialog.close()
                else:
                    QMessageBox.critical(self, "Error", "Incorrect current password.")
            else:
                QMessageBox.critical(self, "Error", "Passwords do not match.")

        confirm_button.clicked.connect(confirm_change)

        dialog.exec_()




    def delete_account(self, username: str):
        confirm_delete = QMessageBox.question(self, "Delete Account", "Are you sure you want to delete your account?",
                                              QMessageBox.Yes | QMessageBox.No)
        if confirm_delete == QMessageBox.Yes:
            self.db_handler.delete_account(username)
            print("Account deleted")
            self.exit()


    def exit(self):
        # Fermez l'application
        self.close()

    def open_settings(self, username: str):
        # Ouvrez la fenêtre des paramètres
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle("Paramètres")
        settings_dialog.setGeometry(700, 300, 300, 200)
        settings_dialog_layout = QVBoxLayout()
        change_password_button = QPushButton("Change Password")
        change_password_button.setStyleSheet("background-color: blue; color: white; border: none; border-radius: 5px; padding: 2px;")
        change_password_button.clicked.connect(lambda: self.change_password(username))
        settings_dialog_layout.addWidget(change_password_button)
        delete_account_button = QPushButton("Delete Account")
        delete_account_button.setStyleSheet("background-color: red; color: white; border: none; border-radius: 5px; padding: 2px;")
        delete_account_button.clicked.connect(lambda: self.delete_account(username))
        settings_dialog_layout.addWidget(delete_account_button)
        settings_dialog.setLayout(settings_dialog_layout)
        settings_dialog.exec_()

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
    app_window = App("username")
    app_window.show()
    sys.exit(app.exec())
