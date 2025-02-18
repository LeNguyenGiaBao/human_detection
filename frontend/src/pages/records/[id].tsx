import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import MainLayout from '../../components/MainLayout'
import { fetchRecordById } from '../../utils'
import styles from '@/styles/RecordDetail.module.css'

export default function RecordDetail() {
  const router = useRouter()
  const { id } = router.query
  const [record, setRecord] = useState<any>(null)

  useEffect(() => {
    if (id) {
      async function loadRecord() {
        const record = await fetchRecordById(id as string)
        setRecord(record)
      }
      loadRecord()
    }
  }, [id])

  if (!record) return <p>Loading...</p>

  return (
    <MainLayout>
      <div className={styles.container}>
        <button onClick={() => router.back()} className={styles.backButton}>
          Back
        </button>

        <div className={styles.detailItem}>
          <span className={styles.detailLabel}>ID:</span>
          <span className={styles.detailValue}>{record.id}</span>
        </div>

        <div className={styles.detailItem}>
          <span className={styles.detailLabel}>Timestamp:</span>
          <span className={styles.detailValue}>
            {new Date(record.timestamp).toLocaleString()}
          </span>
        </div>

        <div className={styles.detailItem}>
          <span className={styles.detailLabel}>Number of Boxes:</span>
          <span className={styles.detailValue}>{record.num_boxes}</span>
        </div>

        {record.image && (
          <div className={styles.imageContainer}>
            <img
              src={`data:image/jpeg;base64,${record.image}`}
              alt="Detected Image"
              className={styles.detectedImage}
            />
          </div>
        )}
      </div>
    </MainLayout>
  )
}
