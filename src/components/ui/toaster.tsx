'use client'

import { Toaster as SonnerToaster } from 'sonner'

// Единая точка для уведомлений: layout.tsx импортирует Toaster из этого модуля,
// поэтому конкретная реализация (sonner) скрыта за этим компонентом.
export function Toaster() {
  return <SonnerToaster position="top-center" richColors />
}
