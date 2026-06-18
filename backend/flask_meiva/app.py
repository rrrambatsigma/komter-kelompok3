from flask import Flask, jsonify, request
from flask_cors import CORS
from config import get_connection

app = Flask(__name__)

# Izinkan akses dari semua origin (termasuk frontend teman via Tailscale)
CORS(app)


# Health check — untuk verifikasi backend bisa diakses via Tailscale
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Backend flask_meiva berjalan"})

@app.route("/gudang", methods=["GET"])
def get_gudang():
    try:
        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("SELECT id_gudang, nama_gudang, lokasi FROM ms_gudang")
        rows = cursor.fetchall()

        result = [{"id_gudang": row[0], "nama_gudang": row[1], "lokasi": row[2]} for row in rows]
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "data": result})

    except Exception as e:
        print("ERROR QUERY:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/gudang", methods=["POST"])
def create_gudang():
    try:
        data = request.get_json()
        nama_gudang = data.get("nama_gudang")
        lokasi = data.get("lokasi")

        if not nama_gudang or not lokasi:
            return jsonify({"error": "Nama gudang dan lokasi harus diisi"}), 400

        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("INSERT INTO ms_gudang (nama_gudang, lokasi) VALUES (?, ?)", (nama_gudang, lokasi))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Gudang added successfully"}), 201

    except Exception as e:
        print("ERROR CREATE:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/gudang/<int:id_gudang>", methods=["PUT"])
def update_gudang(id_gudang):
    try:
        data = request.get_json()
        nama_gudang = data.get("nama_gudang")
        lokasi = data.get("lokasi")

        if not nama_gudang or not lokasi:
            return jsonify({"error": "Nama gudang dan lokasi harus diisi"}), 400

        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("UPDATE ms_gudang SET nama_gudang = ?, lokasi = ? WHERE id_gudang = ?", 
                       (nama_gudang, lokasi, id_gudang))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Gudang updated successfully"}), 200

    except Exception as e:
        print("ERROR UPDATE:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/gudang/<int:id_gudang>", methods=["DELETE"])
def delete_gudang(id_gudang):
    try:
        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("DELETE FROM ms_gudang WHERE id_gudang = ?", (id_gudang,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Gudang deleted successfully"}), 200

    except Exception as e:
        print("ERROR DELETE:", e)
        return jsonify({"error": str(e)}), 500
    
@app.route("/barang", methods=["GET"])
def get_barang():
    try:
        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("SELECT id_barang, nama_barang, kategori, satuan FROM ms_barang")
        rows = cursor.fetchall()

        result = [{"id_barang": row[0], "nama_barang": row[1], "kategori": row[2], "satuan": row[3]} for row in rows]
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "data": result})

    except Exception as e:
        print("ERROR QUERY:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/barang", methods=["POST"])
def create_barang():
    try:
        data = request.get_json()
        nama_barang = data.get("nama_barang")
        kategori = data.get("kategori")
        satuan = data.get("satuan")

        if not nama_barang or not kategori or not satuan:
            return jsonify({"error": "Nama barang, kategori, dan satuan harus diisi"}), 400

        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("INSERT INTO ms_barang (nama_barang, kategori, satuan) VALUES (?, ?, ?)", 
                       (nama_barang, kategori, satuan))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Barang added successfully"}), 201

    except Exception as e:
        print("ERROR CREATE:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/barang/<int:id_barang>", methods=["PUT"])
def update_barang(id_barang):
    try:
        data = request.get_json()
        nama_barang = data.get("nama_barang")
        kategori = data.get("kategori")
        satuan = data.get("satuan")

        if not nama_barang or not kategori or not satuan:
            return jsonify({"error": "Nama barang, kategori, dan satuan harus diisi"}), 400

        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("UPDATE ms_barang SET nama_barang = ?, kategori = ?, satuan = ? WHERE id_barang = ?", 
                       (nama_barang, kategori, satuan, id_barang))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Barang updated successfully"}), 200

    except Exception as e:
        print("ERROR UPDATE:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/barang/<int:id_barang>", methods=["DELETE"])
def delete_barang(id_barang):
    try:
        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("DELETE FROM ms_barang WHERE id_barang = ?", (id_barang,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Barang deleted successfully"}), 200

    except Exception as e:
        print("ERROR DELETE:", e)
        return jsonify({"error": str(e)}), 500


# ===================== STOK =====================

@app.route("/stok", methods=["GET"])
def get_stok():
    try:
        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        query = """
            SELECT s.id_stok, g.nama_gudang, g.lokasi, b.nama_barang, b.kategori, b.satuan, s.jumlah
            FROM tr_stok s
            JOIN ms_gudang g ON s.id_gudang = g.id_gudang
            JOIN ms_barang b ON s.id_barang = b.id_barang
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        result = [{"id_stok": row[0], "gudang": row[1], "lokasi": row[2], 
                   "barang": row[3], "kategori": row[4], "satuan": row[5], 
                   "jumlah": row[6]} for row in rows]
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "data": result})

    except Exception as e:
        print("ERROR QUERY:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/stok", methods=["POST"])
def create_stok():
    try:
        data = request.get_json()
        id_gudang = data.get("id_gudang")
        id_barang = data.get("id_barang")
        jumlah = data.get("jumlah")

        if not id_gudang or not id_barang or not jumlah:
            return jsonify({"error": "ID Gudang, ID Barang, dan Jumlah harus diisi"}), 400

        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("INSERT INTO tr_stok (id_gudang, id_barang, jumlah) VALUES (?, ?, ?)", 
                       (id_gudang, id_barang, jumlah))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Stok added successfully"}), 201

    except Exception as e:
        print("ERROR CREATE:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/stok/<int:id_stok>", methods=["PUT"])
def update_stok(id_stok):
    try:
        data = request.get_json()
        id_gudang = data.get("id_gudang")
        id_barang = data.get("id_barang")
        jumlah = data.get("jumlah")

        if not id_gudang or not id_barang or not jumlah:
            return jsonify({"error": "ID Gudang, ID Barang, dan Jumlah harus diisi"}), 400

        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("UPDATE tr_stok SET id_gudang = ?, id_barang = ?, jumlah = ? WHERE id_stok = ?", 
                       (id_gudang, id_barang, jumlah, id_stok))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Stok updated successfully"}), 200

    except Exception as e:
        print("ERROR UPDATE:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/stok/<int:id_stok>", methods=["DELETE"])
def delete_stok(id_stok):
    try:
        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("DELETE FROM tr_stok WHERE id_stok = ?", (id_stok,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Stok deleted successfully"}), 200

    except Exception as e:
        print("ERROR DELETE:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)