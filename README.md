# Sistem Inventaris Terdistribusi

**Tugas Database Terdistribusi — Kelompok 3**

Aplikasi inventaris barang multi-gudang dengan arsitektur **database terdistribusi** menggunakan **PostgreSQL** dan **SQL Server** yang terhubung melalui jaringan **Tailscale**.

---

## Arsitektur

```
┌──────────────────────────────────────────────────────┐
│                   Frontend React                     │
│               (Vite + Tailwind CSS)                  │
│                    localhost:5173                    │
└──────────┬─────────────────────────────┬─────────────┘
           │ /api/rambat                 │ /api/meiva
           ▼                             ▼
┌──────────────────┐        ┌──────────────────────┐
│ Backend Flask    │        │ Backend Flask        │
│ (flask_rambat)   │        │ (flask_meiva)        │
│ port 5000        │        │ port 5000            │
│ psycopg → PG     │        │ pyodbc → SQL Server  │
└────────┬─────────┘        └─────────┬────────────┘
         │                            │
         ▼                            ▼
┌──────────────────┐        ┌──────────────────────┐
│   PostgreSQL     │        │     SQL Server       │
│  inventaris_db   │        │    inventaris_db     │
│   100.99.218.78  │        │   100.89.60.29       │
└──────────────────┘        └──────────────────────┘
```

### Komponen

| Komponen | Teknologi | Port | Database |
|----------|-----------|------|----------|
| **Frontend** | React 19 + Vite 8 + Tailwind CSS 4 | 5173 | — |
| **Backend Rambat** | Flask 3 + psycopg | 5000 | PostgreSQL |
| **Backend Meiva** | Flask 3 + pyodbc | 5000 | SQL Server |
| **Database PG** | PostgreSQL | 5432 | `inventaris_db` |
| **Database MSSQL** | SQL Server | 1433 | `inventaris_db` |

---

## Tech Stack

- **Frontend:** React 19, Vite 8, Tailwind CSS 4, React Router 7, Axios, react-hot-toast, lucide-react
- **Backend:** Python Flask 3, Flask-CORS
- **Database:** PostgreSQL, SQL Server
- **Networking:** Tailscale (koneksi antar perangkat via IP `100.x.x.x`)

---

## Fitur

- CRUD **Gudang** — kelola data gudang (nama, lokasi)
- CRUD **Barang** — kelola data barang (nama, kategori, satuan)
- CRUD **Stok** — kelola stok barang di gudang (dengan relasi)
- **Dashboard** — ringkasan statistik (total gudang, barang, stok, kuantitas)
- **Multi-backend** — data diambil dari dua node database berbeda

---

## Prasyarat

1. **Node.js** >= 18
2. **Python** >= 3.9
3. **PostgreSQL** (dengan database `inventaris_db`)
4. **SQL Server** (dengan database `inventaris_db`)
5. **Tailscale** (terinstall dan terkoneksi ke jaringan kelompok)

---

## Cara Menjalankan

### 1. Setup Database

Jalankan script SQL sesuai database masing-masing:

**PostgreSQL:**
```bash
psql -h localhost -U postgres -d inventaris_db -f database/sql_server_lois/postgresql_dhea.sql
```

**SQL Server:**
```bash
sqlcmd -S localhost -U sa -d inventaris_db -i database/postgresql_dhea/KOMTER_KELOMPOK.sql
```

### 2. Jalankan Backend Flask

Buka **dua terminal** terpisah:

**Terminal 1 — Backend PostgreSQL (Rambat):**
```bash
cd backend/flask_rambat
pip install -r requirements.txt
python app.py
```

**Terminal 2 — Backend SQL Server (Meiva):**
```bash
cd backend/flask_meiva
pip install -r requirements.txt
python app.py
```

> Jika ingin menjalankan satu backend saja yang mencakup semua CRUD + template HTML, jalankan `backend/app.py`.

### 3. Jalankan Frontend React

```bash
cd frontend
npm install
npm run dev
```

---

## Akses Aplikasi

| Halaman | URL |
|---------|-----|
| Frontend (React SPA) | `http://localhost:5173` |
| Backend API Rambat | `http://localhost:5000` |
| Backend API Meiva | `http://localhost:5000` |
| Dashboard | `http://localhost:5173/` |
| Kelola Gudang | `http://localhost:5173/gudang` |
| Kelola Barang | `http://localhost:5173/barang` |
| Kelola Stok | `http://localhost:5173/stok` |

---

## Catatan

- Semua backend berjalan di **port 5000** — pastikan tidak ada konflik port saat menjalankan keduanya di mesin yang sama.
- IP database (`100.99.218.78` dan `100.89.60.29`) adalah IP **Tailscale** — pastikan perangkat terhubung ke jaringan Tailscale yang sama.
- Konfigurasi koneksi database dapat diubah di `backend/app.py`, `backend/flask_rambat/app.py`, dan `backend/flask_meiva/config/__init__.py`.
- Nama file SQL **terbalik**: folder `postgresql_dhea/` berisi script **SQL Server**, folder `sql_server_lois/` berisi script **PostgreSQL**.
