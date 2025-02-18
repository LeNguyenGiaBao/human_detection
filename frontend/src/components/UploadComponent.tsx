'use client'

import { useState } from 'react'
import styles from '../styles/UploadComponent.module.css'
import Image from 'next/image'
import { uploadFile } from '../utils'

export default function UploadComponent() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [number, setNumber] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files?.[0]) {
      setSelectedFile(event.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file.')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const result = await uploadFile(selectedFile)
      setPreview(`data:image/jpeg;base64,${result.image}`)
      setNumber(result.count)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Network error. Try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.uploadSection}>
        <input
          type="file"
          onChange={handleFileChange}
          accept="image/jpeg, image/png"
          className={styles.fileInput}
        />
        <button
          onClick={handleUpload}
          className={styles.submitBtn}
          disabled={loading || !selectedFile}
        >
          {loading ? 'Uploading...' : 'Submit'}
        </button>
      </div>

      {error && <p className={styles.errorText}>{error}</p>}

      {preview && (
        <div className={styles.resultSection}>
          <p className={styles.numberText}>Number of humans: {number}</p>
          <h2>Detected Image:</h2>
          <Image
            src={preview}
            alt="Detected"
            width={800}
            height={800}
            className={styles.detectedImage}
          />
        </div>
      )}
    </div>
  )
}
