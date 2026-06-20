-- Buat database
CREATE DATABASE inventaris_db;
GO

USE inventaris_db;
GO

SELECT * FROM ms_gudang
SELECT * FROM ms_barang
SELECT * FROM tr_stok

SELECT 
    g.nama_gudang,
    g.lokasi,
    b.nama_barang,
    b.kategori,
    b.satuan,
    s.jumlah
FROM tr_stok s
INNER JOIN ms_gudang g 
    ON s.id_gudang = g.id_gudang
INNER JOIN ms_barang b 
    ON s.id_barang = b.id_barang;


-- Tabel Gudang
CREATE TABLE ms_gudang (
    id_gudang INT IDENTITY(1,1) PRIMARY KEY,
    nama_gudang VARCHAR(100) NOT NULL,
    lokasi VARCHAR(100) NOT NULL
);

-- Tabel Barang
CREATE TABLE ms_barang (
    id_barang INT IDENTITY(1,1) PRIMARY KEY,
    nama_barang VARCHAR(100) NOT NULL,
    kategori VARCHAR(50),
    satuan VARCHAR(20)
);

-- Tabel Stok
CREATE TABLE tr_stok (
    id_stok INT IDENTITY(1,1) PRIMARY KEY,
    id_gudang INT,
    id_barang INT,
    jumlah INT NOT NULL,
    CONSTRAINT fk_gudang FOREIGN KEY (id_gudang) REFERENCES ms_gudang(id_gudang),
    CONSTRAINT fk_barang FOREIGN KEY (id_barang) REFERENCES ms_barang(id_barang)
);

-- =========================
-- INSERT DATA BARU 
-- =========================

-- Gudang (data baru)
INSERT INTO ms_gudang (nama_gudang, lokasi) VALUES
('Gudang Utama', 'Bekasi'),
('Gudang Barat', 'Tangerang'),
('Gudang Timur', 'Bekasi Timur'),
('Gudang Selatan', 'Depok'),
('Gudang Utara', 'Kelapa Gading');

-- Barang (data baru)
INSERT INTO ms_barang (nama_barang, kategori, satuan) VALUES
('Laptop', 'Elektronik', 'Unit'),
('Mouse', 'Elektronik', 'Unit'),
('Keyboard', 'Elektronik', 'Unit'),
('Meja', 'Furniture', 'Unit'),
('Kursi', 'Furniture', 'Unit'),
('Printer', 'Elektronik', 'Unit'),
('Kertas A4', 'ATK', 'Rim');

-- Stok (data baru)
INSERT INTO tr_stok (id_gudang, id_barang, jumlah) VALUES
(1, 1, 25),
(1, 2, 100),
(2, 3, 75),
(3, 4, 40),
(4, 5, 60),
(5, 6, 15),
(2, 7, 200);