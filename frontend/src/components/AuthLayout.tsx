import type { FormEvent, ReactNode } from "react";
import { Link } from "react-router";
import styles from "./AuthLayout.module.css";

type Props = {
    title: string;
    subtitle: string;
    error: string | null;
    onSubmit: (event: FormEvent) => void;
    footnote: ReactNode;
    children: ReactNode;
};

export function AuthLayout({ title, subtitle, error, onSubmit, footnote, children }: Props) {
    return (
        <div className={styles.split}>
            <aside className={styles.aside}>
                <Link to="/" className={styles.brand}>
                    <span className={styles.logo}>S</span>
                    <span className={styles.name}>Scorepad</span>
                </Link>
                <div>
                    <div className={styles.pitch}>Every game night, remembered.</div>
                    <p className={styles.pitchText}>Track the games your group plays.</p>
                </div>
                <div />
            </aside>
            <section className={styles.formSide}>
                <form className={styles.form} onSubmit={onSubmit}>
                    <h1 className={styles.title}>{title}</h1>
                    <p className={styles.subtitle}>{subtitle}</p>
                    {children}
                    {error && (
                        <p role="alert" className={styles.error}>
                            {error}
                        </p>
                    )}
                    <p className={styles.footnote}>{footnote}</p>
                </form>
            </section>
        </div>
    );
}
