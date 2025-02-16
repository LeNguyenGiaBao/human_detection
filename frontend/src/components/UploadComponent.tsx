"use client";

import { useState } from "react";
import styles from "../styles/UploadComponent.module.css";


export default function UploadComponent() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [number, setNumber] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("API Response:", data);

      if (response.ok) {
        setPreview(`data:image/jpeg;base64,${data.data.image}`);
        setNumber(data.data.count);
      } else {
        setError(data.message || "Upload failed.");
      }
    } catch (err) {
      setError("Network error. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.uploadSection}>
        <input
          type="file"
          onChange={handleFileChange}
          accept="image/jpeg, image/png"
          className={styles.fileInput}
        />
        <button onClick={handleUpload} className={styles.submitBtn}>
          Submit
        </button>
      </div>

      {error && <p className={styles.errorText}>{error}</p>}

      {preview && (
        <div className={styles.resultSection}>
          <p className={styles.numberText}>Number of human: {number}</p>
          <h2>Detected Image:</h2>
          <img src={preview} alt="Detected" className={styles.detectedImage} />
        </div>
      )}
    </div>
  );
}
