import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Gudang from './pages/Gudang'
import Barang from './pages/Barang'
import Stok from './pages/Stok'

function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" toastOptions={{ duration: 3000 }} />
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="gudang" element={<Gudang />} />
          <Route path="barang" element={<Barang />} />
          <Route path="stok" element={<Stok />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
