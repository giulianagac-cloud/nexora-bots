import styles from "./StateCard.module.css";

export function EmptyState() {
  return (
    <div className={styles.card}>
      <h3 className={styles.title}>¿En qué podemos ayudarte?</h3>
      <p className={styles.copy}>Contanos tu consulta y te guiamos.</p>
    </div>
  );
}

