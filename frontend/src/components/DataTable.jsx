import { Pencil, Trash2 } from 'lucide-react'

export default function DataTable({ columns, data, onEdit, onDelete, loading, emptyMessage }) {
  if (loading) return null

  if (!data || data.length === 0) {
    return (
      <div className="py-12 text-center text-slate-500">
        <p>{emptyMessage || 'Tidak ada data.'}</p>
      </div>
    )
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white">
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-50 text-xs uppercase text-slate-500">
          <tr>
            {columns.map((col) => (
              <th key={col.key} className="px-4 py-3 font-medium">
                {col.label}
              </th>
            ))}
            <th className="w-24 px-4 py-3 text-center font-medium">Aksi</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {data.map((row, i) => (
            <tr key={row.id || i} className="hover:bg-indigo-50/50">
              {columns.map((col) => (
                <td key={col.key} className="px-4 py-3 text-slate-700">
                  {col.render ? col.render(row) : row[col.key]}
                </td>
              ))}
              <td className="px-4 py-3">
                <div className="flex justify-center gap-1">
                  <button
                    onClick={() => onEdit(row)}
                    className="cursor-pointer rounded p-1.5 text-slate-400 hover:bg-indigo-100 hover:text-indigo-600"
                    title="Edit"
                  >
                    <Pencil size={16} />
                  </button>
                  <button
                    onClick={() => onDelete(row)}
                    className="cursor-pointer rounded p-1.5 text-slate-400 hover:bg-red-100 hover:text-red-600"
                    title="Hapus"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
