import styles from "./StateCard.module.css";

export function EmptyState() {
  return (
    <div className={styles.card}>
      <h3 className={styles.title}>Start an HR conversation</h3>
      <p className={styles.copy}>
        Ask for help with leave, payroll, employee certificates, or internal administrative
        processes.
      </p>
    </div>
  );
}

