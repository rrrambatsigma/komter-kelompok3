import { Loader2 } from 'lucide-react'

export default function Loading() {
  return (
    <div className="flex items-center justify-center py-16">
      <Loader2 size={32} className="animate-spin text-indigo-600" />
    </div>
  )
}
