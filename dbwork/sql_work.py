import sqlite3

def sql_execute(db_path, query = None, data = None):

    if query:
        try:
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                db.commit()
                return True
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return False
        except Exception as e:  # Другие неожиданные ошибки
            print(f"Unexpected error: {e}")
            return False
    else:
        return False

def sql_select(db_path, query, data=None):
    """Функция для выполнения SELECT запросов"""
    if query:
        try:
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                print(results)
                return results
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    else:
        return None

def db_create(db_path):
    query = """
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER NOT NULL CHECK (age > 0 and age < 150),
        grade INTEGER NOT NULL CHECK (grade > 0 and grade < 13))
    """
    return sql_execute(db_path,query)

def db_add(db_path, tabel_name, data):
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    query = f"INSERT INTO {tabel_name} ({columns}) VALUES ({placeholders})"
    return sql_execute(db_path, query, tuple(data.values()))

def db_select(db_path, tabel_name, cond = None,):
    if cond == None:
        query = f"SELECT * FROM {tabel_name}"
        return sql_select(db_path, query)
    condition = " and ".join(f" {k} = {v}" for k, v in cond.items())
    query = f"SELECT * FROM {tabel_name} WHERE {condition} "
    return sql_select(db_path, query)
