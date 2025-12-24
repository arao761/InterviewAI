'use client'

import { ThemeProvider } from '@/components/theme-context'
import { AuthProvider } from '@/context/AuthContext'
import { ReactNode } from 'react'

export function Providers({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      <AuthProvider>
        {children}
      </AuthProvider>
    </ThemeProvider>
  )
}
