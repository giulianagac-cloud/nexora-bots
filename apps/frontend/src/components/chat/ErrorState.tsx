import styles from "./StateCard.module.css";

export function ErrorState() {
  return (
    <div className={styles.card}>
      <h3 className={styles.title}>Service unavailable</h3>
      <p className={styles.copy}>
        The chat service could not complete the request. Please retry or switch to a mocked
        environment during development.
      </p>
    </div>
  );
}

