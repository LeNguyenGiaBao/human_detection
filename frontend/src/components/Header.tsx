import Link from 'next/link'
import styles from '@/styles/Header.module.css'

const Header = () => (
  <header className={styles.header}>
    <div className={styles.container}>
      <Link href="/" passHref legacyBehavior>
        <a className={styles.title}>Human Detection</a>
      </Link>
    </div>
  </header>
)

export default Header
