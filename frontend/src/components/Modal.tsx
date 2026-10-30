import type { ReactNode } from "react";
import styles from "./Modal.module.css";

type Props = { title: string; subtitle?: string; children: ReactNode };

export function Modal({ title, subtitle, children }: Props) {
    return (
        <div className={styles.overlay}>
            <div className={styles.modal} role="dialog" aria-modal="true" aria-label={title}>
                <h2 className={styles.title}>{title}</h2>
                {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
                {children}
            </div>
        </div>
    );
}
