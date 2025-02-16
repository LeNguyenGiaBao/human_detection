import React from "react";
import styles from "@/styles/Header.module.css";

const Header: React.FC = () => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <h1 className={styles.title}>Human Detection</h1>
      </div>
    </header>
  );
};

export default Header;
