import { useEffect, useState, useCallback } from 'react'
import { Plus } from 'lucide-react'
import toast from 'react-hot-toast'
import { rambatApi, meivaApi, fetchAll, createItem, updateItem, deleteItem } from '../api/axios'
import DataTable from '../components/DataTable'
import FormModal from '../components/FormModal'
import ConfirmModal from '../components/ConfirmModal'
import Loading from '../components/Loading'

const ENDPOINT = '/stok'

export default function Stok() {
  const [data, setData] = useState([])
  const [gudang, setGudang] = useState([])
  const [barang, setBarang] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [deleteTarget, setDeleteTarget] = useState(null)

  const loadData = useCallback(() => {
    setLoading(true)
    Promise.all([
      fetchAll(rambatApi, ENDPOINT),
      fetchAll(meivaApi, '/gudang'),
      fetchAll(meivaApi, '/barang'),
    ]).then(([stokRes, gudangRes, barangRes]) => {
      setData(stokRes.data || [])
      setGudang(gudangRes.data || [])
      setBarang(barangRes.data || [])
    }).finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    loadData()
  }, [loadData])

  const fields = [
    {
      name: 'id_gudang',
      label: 'Gudang',
      type: 'select',
      options: gudang.map((g) => ({
        value: g.id_gudang,
        label: `${g.nama_gudang} (${g.lokasi})`,
      })),
    },
    {
      name: 'id_barang',
      label: 'Barang',
      type: 'select',
      options: barang.map((b) => ({
        value: b.id_barang,
        label: `${b.nama_barang} (${b.kategori})`,
      })),
    },
    { name: 'jumlah', label: 'Jumlah', type: 'number', placeholder: 'Masukkan jumlah' },
  ]

  const columns = [
    { key: 'id_stok', label: 'ID' },
    { key: 'gudang', label: 'Gudang', render: (row) => row.gudang || row.nama_gudang || row.id_gudang },
    { key: 'barang', label: 'Barang', render: (row) => row.barang || row.nama_barang || row.id_barang },
    { key: 'kategori', label: 'Kategori' },
    { key: 'satuan', label: 'Satuan' },
    { key: 'jumlah', label: 'Jumlah' },
  ]

  const handleSave = async (form) => {
    const payload = {
      id_gudang: Number(form.id_gudang),
      id_barang: Number(form.id_barang),
      jumlah: Number(form.jumlah),
    }
    if (editing) {
      await updateItem(rambatApi, ENDPOINT, form.id_stok, payload)
      toast.success('Stok berhasil diperbarui')
    } else {
      await createItem(rambatApi, ENDPOINT, payload)
      toast.success('Stok berhasil ditambahkan')
    }
    setModalOpen(false)
    setEditing(null)
    loadData()
  }

  const handleDelete = async () => {
    if (!deleteTarget) return
    await deleteItem(rambatApi, ENDPOINT, deleteTarget.id_stok)
    toast.success('Stok berhasil dihapus')
    setDeleteTarget(null)
    loadData()
  }

  const openEdit = (row) => {
    setEditing(row)
    setModalOpen(true)
  }

  const openAdd = () => {
    setEditing(null)
    setModalOpen(true)
  }

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-bold text-slate-800">Data Stok</h2>
        <button
          onClick={openAdd}
          className="flex cursor-pointer items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
        >
          <Plus size={18} />
          Tambah Stok
        </button>
      </div>

      {loading ? (
        <Loading />
      ) : (
        <DataTable
          columns={columns}
          data={data}
          onEdit={openEdit}
          onDelete={setDeleteTarget}
          emptyMessage="Belum ada data stok."
        />
      )}

      <FormModal
        open={modalOpen}
        title={editing ? 'Edit Stok' : 'Tambah Stok'}
        fields={fields}
        initial={editing || {}}
        onSave={handleSave}
        onClose={() => {
          setModalOpen(false)
          setEditing(null)
        }}
      />

      <ConfirmModal
        open={!!deleteTarget}
        title="Hapus Stok"
        message="Yakin ingin menghapus catatan stok ini?"
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
