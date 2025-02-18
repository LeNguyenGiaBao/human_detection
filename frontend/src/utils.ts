import { API_BASE_URL, SECRET_KEY } from './constants'

export async function fetchRecords() {
  try {
    const response = await fetch(`${API_BASE_URL}/records?secret=${SECRET_KEY}`)
    const data = await response.json()
    if (response.ok) {
      return data.data
    }
  } catch (error) {
    console.error('Error fetching records:', error)
  }
  return []
}

export async function fetchRecordById(id: string) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/records/${id}?secret=${SECRET_KEY}`
    )
    const data = await response.json()
    if (response.ok) {
      return data.data
    }
  } catch (error) {
    console.error('Error fetching record:', error)
  }
  return null
}

export async function uploadFile(file: File) {
  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()

    if (response.ok) {
      return data.data
    } else {
      throw new Error(data.message || 'Upload failed')
    }
  } catch (error) {
    console.error('Upload error:', error)
    throw error
  }
}
