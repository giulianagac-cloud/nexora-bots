import styles from "./StateCard.module.css";

export function LoadingState() {
  return (
    <div className={styles.card}>
      <div className={styles.pulse} />
      <h3 className={styles.title}>Preparing response</h3>
      <p className={styles.copy}>The assistant is processing your request.</p>
    </div>
  );
}

