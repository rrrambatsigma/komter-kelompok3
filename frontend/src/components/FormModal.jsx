import { X } from 'lucide-react'
import { useState } from 'react'

export default function FormModal({ open, title, fields, initial, onSave, onClose }) {
  const [form, setForm] = useState(initial || {})
  const [errors, setErrors] = useState({})

  if (!open) return null

  const handleChange = (name, value) => {
    setForm((prev) => ({ ...prev, [name]: value }))
    setErrors((prev) => ({ ...prev, [name]: '' }))
  }

  const validate = () => {
    const errs = {}
    fields.forEach((f) => {
      if (!form[f.name] && f.name !== 'id') {
        errs[f.name] = `${f.label} wajib diisi`
      }
    })
    setErrors(errs)
    return Object.keys(errs).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!validate()) return
    onSave(form)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="mx-4 w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-800">{title}</h3>
          <button
            onClick={onClose}
            className="cursor-pointer rounded p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
          >
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {fields.map((f) => (
            <div key={f.name}>
              <label className="mb-1 block text-sm font-medium text-slate-700">
                {f.label}
              </label>
              {f.type === 'select' ? (
                <select
                  value={form[f.name] || ''}
                  onChange={(e) => handleChange(f.name, e.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                >
                  <option value="">-- Pilih --</option>
                  {f.options?.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  type={f.type || 'text'}
                  value={form[f.name] || ''}
                  onChange={(e) =>
                    handleChange(
                      f.name,
                      f.type === 'number'
                        ? Number(e.target.value)
                        : e.target.value,
                    )
                  }
                  placeholder={f.placeholder}
                  className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              )}
              {errors[f.name] && (
                <p className="mt-1 text-xs text-red-500">{errors[f.name]}</p>
              )}
            </div>
          ))}

          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="cursor-pointer rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              Batal
            </button>
            <button
              type="submit"
              className="cursor-pointer rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
            >
              Simpan
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
