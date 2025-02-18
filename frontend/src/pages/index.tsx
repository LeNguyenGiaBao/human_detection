import MainLayout from '../components/MainLayout'
import UploadComponent from '../components/UploadComponent'
import Link from 'next/link'

export default function Home() {
  return (
    <MainLayout>
      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <Link href="/records">
          <button
            style={{
              padding: '10px 20px',
              background: '#0070f3',
              color: '#fff',
              border: 'none',
              borderRadius: '5px',
            }}
          >
            View Records
          </button>
        </Link>
      </div>
      <UploadComponent />
    </MainLayout>
  )
}
