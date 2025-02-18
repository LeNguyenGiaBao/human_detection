import React from 'react'
import Header from './Header'
import styles from '@/styles/Layout.module.css'

interface MainLayoutProps {
  children: React.ReactNode
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className={styles.container}>
      <Header />
      <main className={styles.main}>{children}</main>
    </div>
  )
}

export default MainLayout
