import pyodbc

DB_CONFIG = {
    "server": "100.89.60.29,1433",
    "database": "inventaris_db",
    "username": "app_user",
    "password": "123456",
    "driver": "ODBC Driver 17 for SQL Server"
}

def get_connection():
    try:
        conn_str = (
            f"DRIVER={{{DB_CONFIG['driver']}}};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['username']};"
            f"PWD={DB_CONFIG['password']};"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print("ERROR CONNECT DB:", e)
        return None
