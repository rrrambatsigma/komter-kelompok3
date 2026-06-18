CREATE DATABASE inventaris_db;

CREATE TABLE ms_gudang (
    id_gudang SERIAL PRIMARY KEY,
    nama_gudang VARCHAR(100) NOT NULL,
    lokasi VARCHAR(100) NOT NULL
);

CREATE TABLE ms_barang (
    id_barang SERIAL PRIMARY KEY,
    nama_barang VARCHAR(100) NOT NULL,
    kategori VARCHAR(50),
    satuan VARCHAR(20)
);

CREATE TABLE tr_stok (
    id_stok SERIAL PRIMARY KEY,
    id_gudang INT REFERENCES ms_gudang(id_gudang),
    id_barang INT REFERENCES ms_barang(id_barang),
    jumlah INT NOT NULL
);

INSERT INTO ms_gudang (nama_gudang, lokasi) VALUES
('Gudang Jakarta', 'Jakarta'),
('Gudang Bandung', 'Bandung'),
('Gudang Surabaya', 'Surabaya'),
('Gudang Semarang', 'Semarang'),
('Gudang Jogja', 'Yogyakarta'),
('Gudang Medan', 'Medan'),
('Gudang Makassar', 'Makassar');

INSERT INTO ms_barang (nama_barang, kategori, satuan) VALUES
('Beras', 'Sembako', 'Kg'),
('Gula', 'Sembako', 'Kg'),
('Minyak Goreng', 'Sembako', 'Liter'),
('Tepung', 'Sembako', 'Kg'),
('Susu', 'Minuman', 'Liter'),
('Kopi', 'Minuman', 'Gram'),
('Teh', 'Minuman', 'Gram');

INSERT INTO tr_stok (id_gudang, id_barang, jumlah) VALUES
(1, 1, 100),
(2, 2, 80),
(3, 3, 60),
(4, 4, 120),
(5, 5, 50),
(6, 6, 70),
(7, 7, 90);


CREATE ROLE app_user WITH LOGIN PASSWORD '123456';

GRANT ALL PRIVILEGES ON DATABASE inventaris_db TO app_user;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO app_user;

DROP USER IF EXISTS app_user;

CREATE USER app_user WITH PASSWORD '123456';

GRANT ALL PRIVILEGES ON DATABASE inventaris_db TO app_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO app_user;
