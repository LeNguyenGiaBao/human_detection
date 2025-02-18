import { useEffect, useState } from 'react'
import MainLayout from '../components/MainLayout'
import { fetchRecords } from '../utils'
import Link from 'next/link'
import styles from '@/styles/Records.module.css'

interface Record {
  id: string
  timestamp: string
  num_boxes: number
}

export default function Records() {
  const [records, setRecords] = useState<Record[]>([])

  useEffect(() => {
    async function loadRecords() {
      const records = await fetchRecords()
      setRecords(records)
    }
    loadRecords()
  }, [])

  return (
    <MainLayout>
      <h1>Detection Records</h1>
      <div className={styles.container}>
        <table className={styles.table}>
          <thead>
            <tr className={styles.headerRow}>
              <th className={styles.headerCell}>ID</th>
              <th className={styles.headerCell}>Timestamp</th>
              <th className={styles.headerCell}>Number of Boxes</th>
            </tr>
          </thead>
          <tbody>
            {records.length === 0 ? (
              <tr>
                <td colSpan={3} className={styles.emptyState}>
                  No records found
                </td>
              </tr>
            ) : (
              records.map((record) => (
                <tr key={record.id} className={styles.row}>
                  <td className={styles.cell}>
                    <Link
                      href={`/records/${record.id}`}
                      className={styles.link}
                    >
                      {record.id}
                    </Link>
                  </td>
                  <td className={styles.cell}>
                    {new Date(record.timestamp).toLocaleString()}
                  </td>
                  <td className={styles.cell}>{record.num_boxes}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </MainLayout>
  )
}
