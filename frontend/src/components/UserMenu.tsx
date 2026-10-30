import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router";
import { useAuth } from "@/auth/AuthContext";
import { initialsOf } from "@/auth/initials";
import styles from "./UserMenu.module.css";

export function UserMenu() {
    const { player, logout } = useAuth();
    const navigate = useNavigate();
    const [open, setOpen] = useState(false);
    const container = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!open) return;
        const closeOnOutsideClick = (event: MouseEvent) => {
            if (!container.current?.contains(event.target as Node)) setOpen(false);
        };
        const closeOnEscape = (event: KeyboardEvent) => {
            if (event.key === "Escape") setOpen(false);
        };
        document.addEventListener("mousedown", closeOnOutsideClick);
        document.addEventListener("keydown", closeOnEscape);
        return () => {
            document.removeEventListener("mousedown", closeOnOutsideClick);
            document.removeEventListener("keydown", closeOnEscape);
        };
    }, [open]);

    if (!player) return null;

    async function handleLogout() {
        setOpen(false);
        navigate("/");
        await logout();
    }

    return (
        <div className={styles.container} ref={container}>
            <button
                className={styles.avatar}
                onClick={() => setOpen((current) => !current)}
                aria-label="Account menu"
                aria-haspopup="menu"
                aria-expanded={open}
                title={player.email}
            >
                {initialsOf(player)}
            </button>
            {open && (
                <div className={styles.menu} role="menu">
                    <button className={styles.item} role="menuitem" onClick={() => void handleLogout()}>
                        Logout
                    </button>
                </div>
            )}
        </div>
    );
}
