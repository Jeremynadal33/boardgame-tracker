import type { InputHTMLAttributes, TextareaHTMLAttributes } from "react";
import styles from "./Field.module.css";

type InputProps = InputHTMLAttributes<HTMLInputElement> & { label: string };

export function Field({ label, ...props }: InputProps) {
    return (
        <label className={styles.field}>
            <span className="eyebrow">{label}</span>
            <input className={styles.control} {...props} />
        </label>
    );
}

type TextAreaProps = TextareaHTMLAttributes<HTMLTextAreaElement> & { label: string };

export function TextAreaField({ label, ...props }: TextAreaProps) {
    return (
        <label className={styles.field}>
            <span className="eyebrow">{label}</span>
            <textarea className={`${styles.control} ${styles.textarea}`} {...props} />
        </label>
    );
}
