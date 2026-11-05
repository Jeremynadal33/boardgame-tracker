import { useEffect, useRef, type ReactNode } from "react";
import styles from "./Modal.module.css";

type Props = { title: string; subtitle?: string; onClose: () => void; children: ReactNode };

export function Modal({ title, subtitle, onClose, children }: Props) {
    const dialog = useRef<HTMLDialogElement>(null);
    const pressStartedOnBackdrop = useRef(false);

    // showModal() traps the focus, makes the page inert and restores the focus on close
    useEffect(() => {
        const element = dialog.current;
        element?.showModal();
        return () => element?.close();
    }, []);

    // Clicks on the backdrop target the dialog itself: the content has its own wrapper.
    // The press must also start there, so that selecting text in a field and releasing
    // the mouse outside does not close the dialog.
    return (
        <dialog
            ref={dialog}
            className={styles.modal}
            aria-label={title}
            onCancel={(event) => {
                event.preventDefault();
                onClose();
            }}
            onMouseDown={(event) => {
                pressStartedOnBackdrop.current = event.target === event.currentTarget;
            }}
            onClick={(event) => {
                if (pressStartedOnBackdrop.current && event.target === event.currentTarget) onClose();
            }}
        >
            <div className={styles.content}>
                <h2 className={styles.title}>{title}</h2>
                {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
                {children}
            </div>
        </dialog>
    );
}
