import {
  Warehouse,
  Package,
  ClipboardList,
  LayoutDashboard,
  ChevronLeft,
  ChevronRight,
  Server,
} from 'lucide-react'
import { NavLink } from 'react-router-dom'
import { useState } from 'react'

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/gudang', icon: Warehouse, label: 'Gudang' },
  { to: '/barang', icon: Package, label: 'Barang' },
  { to: '/stok', icon: ClipboardList, label: 'Stok' },
]

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <aside
      className={`flex flex-col bg-slate-900 text-white transition-all duration-300 ${
        collapsed ? 'w-16' : 'w-56'
      }`}
    >
      <div className="flex h-14 items-center justify-between border-b border-slate-700 px-4">
        {!collapsed && (
          <h1 className="text-lg font-bold tracking-tight">Inventaris</h1>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="cursor-pointer rounded p-1 hover:bg-slate-700"
          title={collapsed ? 'Buka sidebar' : 'Tutup sidebar'}
        >
          {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </div>

      <nav className="mt-2 flex flex-col gap-1 px-2">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              }`
            }
          >
            <Icon size={20} className="shrink-0" />
            {!collapsed && <span>{label}</span>}
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto border-t border-slate-700 px-3 py-3">
        {!collapsed && (
          <p className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
            Tailscale Backend
          </p>
        )}
        <div className="flex flex-col gap-1.5">
          <div
            className="flex items-center gap-2 text-xs text-slate-400"
            title="100.87.168.12:5000"
          >
            <Server size={14} className="shrink-0 text-emerald-400" />
            {!collapsed && <span>Rambat</span>}
          </div>
          <div
            className="flex items-center gap-2 text-xs text-slate-400"
            title="100.78.200.58:5000"
          >
            <Server size={14} className="shrink-0 text-sky-400" />
            {!collapsed && <span>Meiva</span>}
          </div>
        </div>
      </div>
    </aside>
  )
}
