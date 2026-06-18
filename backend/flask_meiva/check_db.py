from config import get_connection

conn = get_connection()
if not conn:
    print("Koneksi gagal!")
    exit()

cursor = conn.cursor()

# List semua tabel
print("=== TABEL DI DATABASE ===")
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME")
tables = [row[0] for row in cursor.fetchall()]
for t in tables:
    print(f"  - {t}")

# Preview isi tiap tabel (5 baris pertama)
print()
for table in tables:
    print(f"=== ISI TABEL: {table} ===")
    try:
        cursor.execute(f"SELECT TOP 5 * FROM {table}")
        cols = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        print("  Kolom:", cols)
        for row in rows:
            print("  ", list(row))
    except Exception as e:
        print(f"  Error: {e}")
    print()

cursor.close()
conn.close()
