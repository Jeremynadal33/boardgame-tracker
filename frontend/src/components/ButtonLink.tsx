import { Link, type LinkProps } from "react-router";
import styles from "./Button.module.css";

type Props = LinkProps & { variant?: "primary" | "secondary" };

export function ButtonLink({ variant = "primary", className = "", ...props }: Props) {
    return <Link className={`${styles.button} ${styles[variant]} ${styles.link} ${className}`} {...props} />;
}
