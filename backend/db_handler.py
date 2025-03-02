import sqlite3
from logging_handler import logger
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS csv_files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT UNIQUE NOT NULL,
                        filepath TEXT NOT NULL,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )''')
    conn.commit()
    conn.close()


def save_csv_metadata(filename, filepath):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO csv_files (filename, filepath) VALUES (?, ?)", (filename, filepath))
        conn.commit()
        conn.close()
        logger.info(f"Saved metadata for file: {filename}")
    except sqlite3.IntegrityError:
        logger.warning(f"File {filename} already exists in the database")
    except Exception as e:
        logger.error(f"Database error: {str(e)}")


def get_csv_file(filename):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT filepath FROM csv_files WHERE filename = ?", (filename,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def get_csv_files():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM csv_files;", ())
    result = cursor.fetchall()
    conn.close()
    return result if result else None


# Initialize the database when the module is imported
init_db()


if __name__ == '__main__':
    pass
