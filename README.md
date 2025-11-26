# Admin & User Management App

This is a Python desktop application built with **PySide6** for managing users with a secure login system backed by a local SQLite database. The app supports both standard users and admin accounts, providing functionality for password management, account deletion, and user administration.

---

## Features

* **User Login**: Secure login for users with password verification.
* **Password Management**: Users can change their passwords securely.
* **Account Deletion**: Users can delete their own accounts.
* **Admin Panel**: Admins can view the user list, add/modify/delete users.
* **Searchable User List**: Quickly filter users by username.
* **Custom UI**: Frameless and styled windows with drag support.

---

## Installation

1. Clone the repository:

```bash
git clone <your-repository-url>
cd <repository-folder>
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

---

## Project Structure

```
AdminUserApp/
├─ main.py                       # Main application window and logic
├─ database_login_handler.py      # Handles SQLite user database
├─ background_widget.py           # Widget for admin background
├─ user_management_dialog.py      # Admin user management UI
├─ user_list_dialog.py            # Display user list with search
├─ assets/                        # Images and icons (e.g., background-admin.png)
└─ requirements.txt               # Project dependencies
```

---

## License

This project is open source.
