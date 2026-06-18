import { useEffect, useState } from 'react'
import { Warehouse, Package, Layers } from 'lucide-react'
import { rambatApi, meivaApi, fetchAll } from '../api/axios'
import StatCard from '../components/StatCard'
import Loading from '../components/Loading'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetchAll(meivaApi, '/gudang'),
      fetchAll(meivaApi, '/barang'),
      fetchAll(rambatApi, '/stok'),
    ])
      .then(([gudang, barang, stok]) => {
        setStats({
          gudang: gudang.data?.length || 0,
          barang: barang.data?.length || 0,
          stok: stok.data?.length || 0,
          totalItems: stok.data?.reduce((sum, s) => sum + s.jumlah, 0) || 0,
        })
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <Loading />

  return (
    <div>
      <h2 className="mb-6 text-2xl font-bold text-slate-800">Dashboard</h2>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          icon={Warehouse}
          label="Total Gudang"
          value={stats.gudang}
          color="bg-blue-600"
        />
        <StatCard
          icon={Package}
          label="Total Barang"
          value={stats.barang}
          color="bg-emerald-600"
        />
        <StatCard
          icon={Layers}
          label="Total Catatan Stok"
          value={stats.stok}
          color="bg-amber-600"
        />
        <StatCard
          icon={Layers}
          label="Total Kuantitas"
          value={stats.totalItems}
          color="bg-indigo-600"
        />
      </div>
    </div>
  )
}
