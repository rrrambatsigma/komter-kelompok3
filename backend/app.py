from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)
CORS(app)  # supaya frontend temanmu bisa akses API ini

# =====================
# CONFIG DATABASE
# =====================
DB_CONFIG = {
    "host": "100.99.218.78",   # IP Tailscale laptop server database
    "port": 5432,
    "dbname": "inventaris_db",
    "user": "postgres",        # ganti kalau nanti pakai app_user
    "password": "031205"
}

# =====================
# CONNECT DB
# =====================
def get_connection():
    try:
        conn = psycopg.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            row_factory=dict_row
        )
        return conn
    except Exception as e:
        print("ERROR CONNECT DB:", e)
        return None
    
def db_error_response(message, code=500):
    return jsonify({
        "status": "error",
        "message": message
    }), code


def success_response(message, data=None, code=200):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    }), code

# =====================
# HOME
# =====================
@app.route("/")
def home():
    return render_template("index.html")

# =====================
# TEST CONNECTION
# =====================
@app.route("/test")
def test_db():
    try:
        conn = get_connection()
        if not conn:
            return jsonify({
                "status": "error",
                "message": "Gagal konek ke PostgreSQL"
            }), 500

        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 AS test")
            result = cursor.fetchone()

        conn.close()

        return jsonify({
            "status": "success",
            "message": "Koneksi PostgreSQL BERHASIL!",
            "data": result
        })
    except Exception as e:
        print("ERROR /test:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# =====================
# CRUD GUDANG
# =====================

@app.route("/gudang", methods=["GET"])
def get_gudang():
    try:
        conn = get_connection()
        if not conn:
            return db_error_response("Koneksi database gagal")

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_gudang, nama_gudang, lokasi
                FROM ms_gudang
                ORDER BY id_gudang
            """)
            rows = cursor.fetchall()

        conn.close()
        return success_response("Data gudang berhasil diambil", rows)

    except Exception as e:
        print("ERROR GET /gudang:", e)
        return db_error_response(str(e))


@app.route("/gudang", methods=["POST"])
def create_gudang():
    try:
        data = request.get_json()
        nama_gudang = data.get("nama_gudang")
        lokasi = data.get("lokasi")

        if not nama_gudang or not lokasi:
            return db_error_response("nama_gudang dan lokasi wajib diisi", 400)

        conn = get_connection()
        if not conn:
            return db_error_response("Koneksi database gagal")

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO ms_gudang (nama_gudang, lokasi)
                VALUES (%s, %s)
                RETURNING id_gudang, nama_gudang, lokasi
            """, (nama_gudang, lokasi))
            new_data = cursor.fetchone()
            conn.commit()

        conn.close()
        return success_response("Data gudang berhasil ditambahkan", new_data, 201)

    except Exception as e:
        print("ERROR POST /gudang:", e)
        return db_error_response(str(e))


@app.route("/gudang/<int:id_gudang>", methods=["PUT"])
def update_gudang(id_gudang):
    try:
        data = request.get_json()
        nama_gudang = data.get("nama_gudang")
        lokasi = data.get("lokasi")

        if not nama_gudang or not lokasi:
            return db_error_response("nama_gudang dan lokasi wajib diisi", 400)

        conn = get_connection()
        if not conn:
            return db_error_response("Koneksi database gagal")

        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE ms_gudang
                SET nama_gudang = %s, lokasi = %s
                WHERE id_gudang = %s
                RETURNING id_gudang, nama_gudang, lokasi
            """, (nama_gudang, lokasi, id_gudang))
            updated = cursor.fetchone()
            conn.commit()

        conn.close()

        if not updated:
            return db_error_response("Data gudang tidak ditemukan", 404)

        return success_response("Data gudang berhasil diupdate", updated)

    except Exception as e:
        print("ERROR PUT /gudang:", e)
        return db_error_response(str(e))


@app.route("/gudang/<int:id_gudang>", methods=["DELETE"])
def delete_gudang(id_gudang):
    try:
        conn = get_connection()
        if not conn:
            return db_error_response("Koneksi database gagal")

        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM ms_gudang
                WHERE id_gudang = %s
                RETURNING id_gudang, nama_gudang, lokasi
            """, (id_gudang,))
            deleted = cursor.fetchone()
            conn.commit()

        conn.close()

        if not deleted:
            return db_error_response("Data gudang tidak ditemukan", 404)

        return success_response("Data gudang berhasil dihapus", deleted)

    except Exception as e:
        print("ERROR DELETE /gudang:", e)
        return db_error_response(str(e))
    
# =====================
# CRUD BARANG
# =====================

@app.route("/barang", methods=["GET"])
def get_barang():
    try:
        conn = get_connection()
        if not conn:
            return db_error_response("Koneksi database gagal")

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_barang, nama_barang, kategori, satuan
                FROM ms_barang
                ORDER BY id_barang
            """)
            rows = cursor.fetchall()

        conn.close()
        return success_response("Data barang berhasil diambil", rows)

    except Exception as e:
        print("ERROR GET /barang:", e)
        return db_error_response(str(e))


@app.route("/barang", methods=["POST"])
def create_barang():
    try:
        data = request.get_json()
        nama_barang = data.get("nama_barang")
        kategori = data.get("kategori")
        satuan = data.get("satuan")

        if not nama_barang or not kategori or not satuan:
            return db_error_response("nama_barang, kategori, dan satuan wajib diisi", 400)

        conn = get_connection()
        if not conn:
            return db_error_response("Koneksi database gagal")

        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO ms_barang (nama_barang, kategori, satuan)
                VALUES (%s, %s, %s)
                RETURNING id_barang, nama_barang, kategori, satuan
            """, (nama_barang, kategori, satuan))
            new_data = cursor.fetchone()
            conn.commit()

        conn.close()
        return success_response("Data barang berhasil ditambahkan", new_data, 201)

    except Exception as e:
        print("ERROR POST /barang:", e)
        return db_error_response(str(e))


@app.route("/barang/<int:id_barang>", methods=["PUT"])
def update_barang(id_barang):
    try:
        data = request.get_json()
        nama_barang = data.get("nama_barang")
        kategori = data.get("kategori")
        satuan = data.get("satuan")

        if not nama_barang or not kategori or not satuan:
            return db_error_response("nama_barang, kategori, dan satuan wajib diisi", 400)

        conn = get_connection()
        if not conn:
            return db_error_response("Koneksi database gagal")

        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE ms_barang
                SET nama_barang = %s, kategori = %s, satuan = %s
                WHERE id_barang = %s
                RETURNING id_barang, nama_barang, kategori, satuan
            """, (nama_barang, kategori, satuan, id_barang))
            updated = cursor.fetchone()
            conn.commit()

        conn.close()

        if not updated:
            return db_error_response("Data barang tidak ditemukan", 404)

        return success_response("Data barang berhasil diupdate", updated)

    except Exception as e:
        print("ERROR PUT /barang:", e)
        return db_error_response(str(e))


@app.route("/barang/<int:id_barang>", methods=["DELETE"])
def delete_barang(id_barang):
    try:
        conn = get_connection()
        if not conn:
            return db_error_response("Koneksi database gagal")

        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM ms_barang
                WHERE id_barang = %s
                RETURNING id_barang, nama_barang, kategori, satuan
            """, (id_barang,))
            deleted = cursor.fetchone()
            conn.commit()

        conn.close()

        if not deleted:
            return db_error_response("Data barang tidak ditemukan", 404)

        return success_response("Data barang berhasil dihapus", deleted)

    except Exception as e:
        print("ERROR DELETE /barang:", e)
        return db_error_response(str(e))
    

    
# =====================
# API STOK
# =====================
@app.route("/stok", methods=["GET"])
def get_stok():
    try:
        conn = get_connection()
        if not conn:
            return jsonify({
                "status": "error",
                "message": "Koneksi database gagal"
            }), 500

        query = """
            SELECT 
            s.id_stok,
            s.id_gudang,
            s.id_barang,
            g.nama_gudang AS gudang,
            g.lokasi AS lokasi,
            b.nama_barang AS barang,
            b.kategori AS kategori,
            b.satuan AS satuan,
            s.jumlah AS jumlah
            FROM tr_stok s
            JOIN ms_gudang g ON s.id_gudang = g.id_gudang
            JOIN ms_barang b ON s.id_barang = b.id_barang
            ORDER BY s.id_stok
        """

        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        conn.close()

        return jsonify({
            "status": "success",
            "message": "Data stok berhasil diambil",
            "data": rows
        })

    except Exception as e:
        print("ERROR QUERY /stok:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
@app.route("/stok", methods=["POST"])
def create_stok():
    try:
        data = request.get_json()
        id_gudang = data.get("id_gudang")
        id_barang = data.get("id_barang")
        jumlah = data.get("jumlah")

        if id_gudang is None or id_barang is None or jumlah is None:
            return db_error_response("id_gudang, id_barang, dan jumlah wajib diisi", 400)

        conn = get_connection()
        if not conn:
            return db_error_response("Koneksi database gagal")

        with conn.cursor() as cursor:
            cursor.execute("SELECT id_gudang FROM ms_gudang WHERE id_gudang = %s", (id_gudang,))
            gudang = cursor.fetchone()
            if not gudang:
                conn.close()
                return db_error_response("id_gudang tidak ditemukan", 404)

            cursor.execute("SELECT id_barang FROM ms_barang WHERE id_barang = %s", (id_barang,))
            barang = cursor.fetchone()
            if not barang:
                conn.close()
                return db_error_response("id_barang tidak ditemukan", 404)

            cursor.execute("""
                INSERT INTO tr_stok (id_gudang, id_barang, jumlah)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (id_gudang, id_barang, jumlah))
            new_data = cursor.fetchone()
            conn.commit()

        conn.close()
        return success_response("Data stok berhasil ditambahkan", new_data, 201)

    except Exception as e:
        print("ERROR POST /stok:", e)
        return db_error_response(str(e))


@app.route("/stok/<int:id_stok>", methods=["PUT"])
def update_stok(id_stok):
    try:
        data = request.get_json()
        id_gudang = data.get("id_gudang")
        id_barang = data.get("id_barang")
        jumlah = data.get("jumlah")

        if id_gudang is None or id_barang is None or jumlah is None:
            return db_error_response("id_gudang, id_barang, dan jumlah wajib diisi", 400)

        conn = get_connection()
        if not conn:
            return db_error_response("Koneksi database gagal")

        with conn.cursor() as cursor:
            cursor.execute("SELECT id_gudang FROM ms_gudang WHERE id_gudang = %s", (id_gudang,))
            gudang = cursor.fetchone()
            if not gudang:
                conn.close()
                return db_error_response("id_gudang tidak ditemukan", 404)

            cursor.execute("SELECT id_barang FROM ms_barang WHERE id_barang = %s", (id_barang,))
            barang = cursor.fetchone()
            if not barang:
                conn.close()
                return db_error_response("id_barang tidak ditemukan", 404)

            cursor.execute("""
                UPDATE tr_stok
                SET id_gudang = %s, id_barang = %s, jumlah = %s
                WHERE id_stok = %s
                RETURNING *
            """, (id_gudang, id_barang, jumlah, id_stok))
            updated = cursor.fetchone()
            conn.commit()

        conn.close()

        if not updated:
            return db_error_response("Data stok tidak ditemukan", 404)

        return success_response("Data stok berhasil diupdate", updated)

    except Exception as e:
        print("ERROR PUT /stok:", e)
        return db_error_response(str(e))


@app.route("/stok/<int:id_stok>", methods=["DELETE"])
def delete_stok(id_stok):
    try:
        conn = get_connection()
        if not conn:
            return db_error_response("Koneksi database gagal")

        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM tr_stok
                WHERE id_stok = %s
                RETURNING *
            """, (id_stok,))
            deleted = cursor.fetchone()
            conn.commit()

        conn.close()

        if not deleted:
            return db_error_response("Data stok tidak ditemukan", 404)

        return success_response("Data stok berhasil dihapus", deleted)

    except Exception as e:
        print("ERROR DELETE /stok:", e)
        return db_error_response(str(e))

# =====================
# RUN APP
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)