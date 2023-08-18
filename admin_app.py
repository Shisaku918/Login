import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QInputDialog, QListWidget, QTableWidget, QTableWidgetItem, QScrollArea
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from database_login_handler import DatabaseLoginHandler


class UserListDialog(QDialog):
    def __init__(self, username: str):
        super().__init__()
        self.setWindowTitle("User List")
        self.setGeometry(700, 300, 400, 400)  # Increased the height to accommodate search bar
        self.db_handler = DatabaseLoginHandler("database_login.db")

        main_layout = QVBoxLayout()

        welcome_label = QLabel(f"User Management for {username}")
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)

        # Add a search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search by username")
        search_bar.textChanged.connect(self.filter_user_list)
        main_layout.addWidget(search_bar)

        # Create a scroll area to hold the user list
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        self.user_labels = []  # Store labels to later filter them
        
        user_list = self.db_handler.get_user_list()
        for user_info in user_list:
            user_label = QLabel(f"Username: {user_info['username']}\nPassword: {user_info['password']}\nRole: {user_info['role']}\n\n")
            scroll_layout.addWidget(user_label)
            self.user_labels.append(user_label)
        
        # Set the scroll layout to the scroll widget
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        main_layout.addWidget(scroll_area)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("background-color: blue; color: white; border: none; border-radius: 5px; padding: 2px;")
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button)

        self.setLayout(main_layout)

    def filter_user_list(self, search_text):
        for user_label in self.user_labels:
            if search_text.lower() in user_label.text().lower():
                user_label.setVisible(True)
            else:
                user_label.setVisible(False)




class UserManagementDialog(QDialog):
    def __init__(self, username: str):
        super().__init__()
        self.setWindowTitle("User Management")
        self.setGeometry(700, 300, 300, 200)
        self.db_handler = DatabaseLoginHandler("database_login.db")  # Initialisez votre gestionnaire de base de données

        layout = QVBoxLayout()

        add_button = QPushButton("Add Admin")
        add_button.setStyleSheet("background-color: black; color: white; border: none; border-radius: 5px; padding: 2px;")
        add_button.clicked.connect(self.add_admin)
        layout.addWidget(add_button)

        add_button = QPushButton("Add User")
        add_button.setStyleSheet("background-color: blue; color: white; border: none; border-radius: 5px; padding: 2px;")
        add_button.clicked.connect(self.add_user)
        layout.addWidget(add_button)

        modify_button = QPushButton("Modify User")
        modify_button.setStyleSheet("background-color: #039dfc; color: white; border: none; border-radius: 5px; padding: 2px;")
        modify_button.clicked.connect(self.modify_user)
        layout.addWidget(modify_button)

        delete_button = QPushButton("Delete User")
        delete_button.setStyleSheet("background-color: red; color: white; border: none; border-radius: 5px; padding: 2px;")
        delete_button.clicked.connect(self.delete_user)
        layout.addWidget(delete_button)

        close_button = QPushButton("Close")
        close_button.setStyleSheet("background-color: gray; color: white; border: none; border-radius: 5px; padding: 2px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def add_admin(self):
        username, ok = QInputDialog.getText(self, "Add User", "Enter username:")
        if ok and username:
            password, ok = QInputDialog.getText(self, "Add User", "Enter password:")
            if ok and password:
                if self.db_handler.create_admin(username, password):
                    QMessageBox.information(self, "Success", "User added successfully.")
                else:
                    QMessageBox.critical(self, "Error", f"Username '{username}' is already taken.")

    def add_user(self):
        username, ok = QInputDialog.getText(self, "Add User", "Enter username:")
        if ok and username:
            password, ok = QInputDialog.getText(self, "Add User", "Enter password:")
            if ok and password:
                if self.db_handler.create_person(username, password):
                    QMessageBox.information(self, "Success", "User added successfully.")
                else:
                    QMessageBox.critical(self, "Error", f"Username '{username}' is already taken.")

    def delete_user(self):
        username, ok = QInputDialog.getText(self, "Delete User", "Enter username:")
        if ok and username:
            confirm_delete = QMessageBox.question(self, "Delete User", f"Are you sure you want to delete the user '{username}'?",
                                                  QMessageBox.Yes | QMessageBox.No)
            if confirm_delete == QMessageBox.Yes:
                if self.db_handler.user_exists_with(username):
                    self.db_handler.delete_account(username)
                    QMessageBox.information(self, "Success", f"User '{username}' deleted successfully.")
                else:
                    QMessageBox.critical(self, "Error", f"User '{username}' does not exist.")

    def modify_user(self):
        username, ok = QInputDialog.getText(self, "Modify User", "Enter username:")
        if ok and username:
            new_password, ok = QInputDialog.getText(self, "Modify User", "Enter new password:")
            if ok and new_password:
                if self.db_handler.user_exists_with(username):
                    self.db_handler.change_password(username, new_password)
                    QMessageBox.information(self, "Success", f"Password for user '{username}' modified successfully.")
                else:
                    QMessageBox.critical(self, "Error", f"User '{username}' does not exist.")



class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.background_label = QLabel(self)
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), "background-admin.png"))  # Chemin de votre image de fond
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)  # Redimensionner automatiquement l'image pour qu'elle s'adapte au QLabel

    def resizeEvent(self, event):
        # Redimensionner automatiquement le QLabel (et donc l'image) lorsque le widget est redimensionné
        self.background_label.setGeometry(self.rect())



class AppAdmin(QWidget):
    def __init__(self, username: str):
        super().__init__()
        self.initUI(username)

    def initUI(self, username: str):
        self.setGeometry(600, 200, 600, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("border: 3px solid white;")

        main_layout = QVBoxLayout(self)
        main_widget = BackgroundWidget(self)
        widget_layout = QVBoxLayout(main_widget)
        widget_layout.setAlignment(Qt.AlignCenter)  # Alignement au centre
        main_widget.setLayout(widget_layout)
        main_layout.addWidget(main_widget)

        name_label = QLabel(f"Welcome {username}")  # Ajout du texte statique avec la balise <font>
        name_label.setStyleSheet("border: none; color: white; margin-bottom: 50px;")  # Supprimez la couleur blanche ici, car nous l'avons spécifiée dans la balise <font>
        name_label_font = QFont("Arial", 20)
        name_label.setFont(name_label_font)
        widget_layout.addWidget(name_label)


        list_users_button = QPushButton("Users List")
        list_users_button.setStyleSheet("background-color: #039dfc; color: white; border: none; border-radius: 5px; padding: 5px; margin-top: 85px;")
        list_users_button.clicked.connect(lambda: self.users_list(username))
        widget_layout.addWidget(list_users_button)

        manage_users_button = QPushButton("Manage Users")
        manage_users_button.setStyleSheet("background-color: blue; color: white; border: none; border-radius: 5px; padding: 5px;")
        manage_users_button.clicked.connect(lambda: self.open_user_management(username))
        widget_layout.addWidget(manage_users_button)

        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("background-color: gray; color: white; border: none; border-radius: 5px; padding: 5px;")
        exit_button.clicked.connect(self.exit)
        widget_layout.addWidget(exit_button)

        self.setLayout(widget_layout)

    def open_user_management(self, username: str):
        user_management_dialog = UserManagementDialog(username)
        user_management_dialog.exec()

    def users_list(self, username: str):
        user_list_dialog = UserListDialog(username)
        user_list_dialog.exec()


    def exit(self):
        # Fermez l'application
        self.close()

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
    app_window = AppAdmin("ADMIN")
    app_window.show()
    sys.exit(app.exec())
