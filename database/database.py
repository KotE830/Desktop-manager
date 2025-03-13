import os
import sqlite3
import threading

from config import PATHS
from objects.buttons import Button
from utils import *

class Database:
    def __init__(self, parent=None):
        self.parent = parent

        try:
            # Set database path
            self.base_dir = PATHS['ROOT']
            self.db_dir = os.path.join(self.base_dir, PATHS['DATABASE_DIR'])
            self.db_path = os.path.join(self.db_dir, PATHS['DATABASE_PATH'])
            
            # Create directory
            if not os.path.exists(self.db_dir):
                try:
                    os.makedirs(self.db_dir)
                except PermissionError as e:
                    show_error("Database folder creation permission denied.", str(e))
                except OSError as e:
                    show_error(f"Database folder creation failed: {str(e)}")

            # Connect to database
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.initialize_DB()
            
        except Exception as e:
            show_error("Database initialization error", str(e))
    
    def initialize_DB(self):
        # Button table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS buttons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                button_name TEXT NOT NULL
            )
        ''')

        # Initialize button sequence
        self.cursor.execute('''
            INSERT OR IGNORE INTO sqlite_sequence (name, seq) 
            VALUES ('buttons', 1)
        ''')    # ID 1 : Run button

        # File table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                button_id INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                FOREIGN KEY (button_id) REFERENCES buttons (id) ON DELETE CASCADE
            )
        ''')

        # URL table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                button_id INTEGER NOT NULL,
                name TEXT,
                url TEXT,
                FOREIGN KEY (button_id) REFERENCES buttons (id) ON DELETE CASCADE
            )
        ''')
        
        self.connection.commit()

    def get_buttons(self):
        self.cursor.execute('SELECT * FROM buttons')
        buttons = []
        for row in self.cursor.fetchall():
            button = Button(self.parent, row[1])  # button_name
            button.set_id(row[0])  # button_id
            buttons.append(button)
        return buttons

    def get_files(self, button_id):
        self.cursor.execute('SELECT * FROM files WHERE button_id = ?', (button_id,))
        files = []
        for row in self.cursor.fetchall():
            files.append({
                'id': row[0],
                'file_path': row[2],
                'file_name': row[2].split('/')[-1]
            })
        return files
    
    def get_urls(self, button_id):
        self.cursor.execute('SELECT * FROM urls WHERE button_id = ?', (button_id,))
        urls = []
        for row in self.cursor.fetchall():
            urls.append({
                'id': row[0],
                'name': row[2],
                'url': row[3]
            })
        return urls
    
    def add_button(self, button):
        self.cursor.execute('''
            INSERT INTO buttons (button_name) VALUES (?)
        ''', (button.get_title(),))
        self.connection.commit()
        button.set_id(self.cursor.lastrowid)

    def add_file(self, button_id, file_path):
        self.cursor.execute('''
            INSERT INTO files (button_id, file_path) VALUES (?, ?)
        ''', (button_id, file_path))
        self.connection.commit()

    def add_url(self, button_id, name, url):
        self.cursor.execute('''
            INSERT INTO urls (button_id, name, url) VALUES (?, ?, ?)
        ''', (button_id, name, url))
        self.connection.commit()
    
    def delete_button(self, button):
        self.cursor.execute('DELETE FROM buttons WHERE id = ?', (button.get_id(),))
        self.connection.commit()

    def delete_file(self, file_id):
        self.cursor.execute('DELETE FROM files WHERE id = ?', (file_id,))
        self.connection.commit()

    def delete_url(self, url_id):
        self.cursor.execute('DELETE FROM urls WHERE id = ?', (url_id,))
        self.connection.commit()

    def update_url(self, url_id, name, url):
        self.cursor.execute('''
            UPDATE urls 
            WHERE id = ?
            SET name = ?, url = ? 
        ''', (url_id, name, url))
        self.connection.commit()

    def execute_button(self, button_id):
        """Open files and URLs for button_id"""
        try:
            # Get files and URLs
            self.cursor.execute('SELECT file_path FROM files WHERE button_id = ?', (button_id,))
            files = [row[0] for row in self.cursor.fetchall()]  # file_path
        
            self.cursor.execute('SELECT url FROM urls WHERE button_id = ?', (button_id,))
            urls = [row[0] for row in self.cursor.fetchall()]  # url
            
            # Execute files
            for file_path in files:
                threading.Thread(target=open_file, args=(file_path,)).start()
            
            # Open URLs in a new window
            if urls:
                open_urls(urls)
                
        except Exception as e:
            show_error("Error executing button", str(e))

    def close(self):
        self.connection.close()
