import sqlite3
import os

# 資料庫存放路徑 (對應到 instance/database.db)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(DB_DIR, 'database.db')

def get_db_connection():
    """建立並回傳 SQLite 資料庫連線"""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # 將回傳的查詢結果轉換成像字典一樣能透過 key 存取的 Row 物件
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫（首次啟動時如果沒有表則會建立）"""
    conn = get_db_connection()
    schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    conn.commit()
    conn.close()

class RecordModel:
    """處理所有的資料庫存取邏輯 (CRUD)"""

    @staticmethod
    def create(type_, category, amount, date, description=""):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO records (type, category, amount, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (type_, category, amount, date, description))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        # 依照日期排序，然後利用 id 作為同日的穩定排序
        cursor.execute('SELECT * FROM records ORDER BY date DESC, id DESC')
        records = cursor.fetchall()
        conn.close()
        return [dict(row) for row in records]

    @staticmethod
    def get_by_id(record_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM records WHERE id = ?', (record_id,))
        record = cursor.fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def update(record_id, type_, category, amount, date, description=""):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE records 
            SET type = ?, category = ?, amount = ?, date = ?, description = ?
            WHERE id = ?
        ''', (type_, category, amount, date, description, record_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
