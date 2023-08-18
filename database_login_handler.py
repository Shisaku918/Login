import os
import sqlite3

class DatabaseLoginHandler():
    def __init__(self, database_name: str):
        db_path = os.path.join(os.path.dirname(__file__), database_name)
        self.con = sqlite3.connect(db_path)
        self.con.row_factory = sqlite3.Row

    def role_for(self, username: str) -> str:
        cursor = self.con.cursor()
        query = f"SELECT role FROM Person WHERE username = ?;"
        cursor.execute(query, (username,))
        result = cursor.fetchall()
        cursor.close()
        if result:
            return dict(result[0])["role"]
        else:
            return None
    
    def get_user_list(self):
        cursor = self.con.cursor()
        query = "SELECT username, password, role FROM Person;"
        cursor.execute(query)
        user_list = cursor.fetchall()
        cursor.close()
        return user_list


    def create_person(self, username: str, password: str) -> bool:
        cursor = self.con.cursor()
        try:
            query = "INSERT INTO Person (username, password) VALUES (?, ?);"
            cursor.execute(query, (username, password))
            cursor.close()
            self.con.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def create_admin(self, username: str, password: str) -> bool:
        cursor = self.con.cursor()
        try:
            query = "INSERT INTO Person (username, password, role) VALUES (?, ?, ?);"
            cursor.execute(query, (username, password, "admin"))
            cursor.close()
            self.con.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def password_for(self, username: str) -> str:
        cursor = self.con.cursor()
        query = f"SELECT password FROM Person WHERE username = ?;"
        cursor.execute(query, (username,))
        result = cursor.fetchall()
        cursor.close()
        return dict(result[0]) ["password"]
    
    def user_exists_with(self, username: str) -> bool:
        cursor = self.con.cursor()
        query = f"SELECT * FROM Person WHERE username = ?;"
        cursor.execute(query, (username,))
        result = cursor.fetchall()
        cursor.close()
        return len(result) == 1
    
    def change_password(self, username: str, new_password: str):
        cursor = self.con.cursor()
        query = f"UPDATE Person SET password = ?, nbPasswordChange = nbPasswordChange + 1 WHERE username = ?;"
        cursor.execute(query, (new_password, username))
        cursor.close()
        self.con.commit()

    def delete_account(self, username: str):
        cursor = self.con.cursor()
        query = f"DELETE FROM Person WHERE username = ?;"
        cursor.execute(query, (username,))
        cursor.close()
        self.con.commit()
