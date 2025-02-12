import sqlite3

class Database:
    def __init__(self):
        # :memory: 를 사용하여 메모리에 DB 생성
        self.db_path = "app_data.db"
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.initialize_db()
    
    def initialize_db(self):
        # 테이블 생성
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 초기 데이터 설정
        self.cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value) 
            VALUES ('version', '1.0')
        ''')
        
        self.conn.commit()
        self.file_path = None
    
    def save_setting(self, key, value):
        self.cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value) 
            VALUES (?, ?)
        ''', (key, str(value)))
        self.conn.commit()
    
    def get_setting(self, key, default=None):
        self.cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = self.cursor.fetchone()
        return result[0] if result else default
    
    def log_action(self, action):
        self.cursor.execute('INSERT INTO history (action) VALUES (?)', (action,))
        self.conn.commit()
    
    def get_history(self):
        self.cursor.execute('SELECT * FROM history ORDER BY timestamp DESC')
        return self.cursor.fetchall()
    
    def get_file_path(self):
        return self.file_path

# 사용 예시
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = MemoryDatabase()
        
        # 설정 저장
        self.db.save_setting('theme', 'dark')
        self.db.save_setting('font_size', '12')
        
        # 설정 불러오기
        theme = self.db.get_setting('theme', 'light')
        font_size = self.db.get_setting('font_size', '10')
        
        # 작업 기록
        self.db.log_action('Application started')