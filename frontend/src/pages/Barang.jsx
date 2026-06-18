import { useEffect, useState, useCallback } from 'react'
import { Plus } from 'lucide-react'
import toast from 'react-hot-toast'
import { rambatApi, fetchAll, createItem, updateItem, deleteItem } from '../api/axios'
import DataTable from '../components/DataTable'
import FormModal from '../components/FormModal'
import ConfirmModal from '../components/ConfirmModal'
import Loading from '../components/Loading'

const ENDPOINT = '/barang'

const fields = [
  { name: 'nama_barang', label: 'Nama Barang', placeholder: 'Masukkan nama barang' },
  { name: 'kategori', label: 'Kategori', placeholder: 'Masukkan kategori' },
  { name: 'satuan', label: 'Satuan', placeholder: 'contoh: pcs, kg, box' },
]

const columns = [
  { key: 'id_barang', label: 'ID' },
  { key: 'nama_barang', label: 'Nama Barang' },
  { key: 'kategori', label: 'Kategori' },
  { key: 'satuan', label: 'Satuan' },
]

export default function Barang() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [deleteTarget, setDeleteTarget] = useState(null)

  const loadData = useCallback(() => {
    setLoading(true)
    fetchAll(rambatApi, ENDPOINT)
      .then((res) => setData(res.data || []))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    loadData()
  }, [loadData])

  const handleSave = async (form) => {
    if (editing) {
      await updateItem(rambatApi, ENDPOINT, form.id_barang, form)
      toast.success('Barang berhasil diperbarui')
    } else {
      await createItem(rambatApi, ENDPOINT, form)
      toast.success('Barang berhasil ditambahkan')
    }
    setModalOpen(false)
    setEditing(null)
    loadData()
  }

  const handleDelete = async () => {
    if (!deleteTarget) return
    await deleteItem(rambatApi, ENDPOINT, deleteTarget.id_barang)
    toast.success('Barang berhasil dihapus')
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
        <h2 className="text-2xl font-bold text-slate-800">Data Barang</h2>
        <button
          onClick={openAdd}
          className="flex cursor-pointer items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
        >
          <Plus size={18} />
          Tambah Barang
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
          emptyMessage="Belum ada data barang."
        />
      )}

      <FormModal
        open={modalOpen}
        title={editing ? 'Edit Barang' : 'Tambah Barang'}
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
        title="Hapus Barang"
        message={`Yakin ingin menghapus "${deleteTarget?.nama_barang}"?`}
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  )
}
