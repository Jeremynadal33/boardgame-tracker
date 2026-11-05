import { Link, NavLink } from "react-router";
import { useAuth } from "@/auth/AuthContext";
import { ButtonLink } from "./ButtonLink";
import { UserMenu } from "./UserMenu";
import styles from "./NavBar.module.css";

export function NavBar() {
    const { player, loading } = useAuth();

    return (
        <header className={styles.bar}>
            <nav className={styles.inner}>
                <Link to="/" className={styles.brand}>
                    <span className={styles.logo}>S</span>
                    <span className={styles.name}>Scorepad</span>
                </Link>
                {player && (
                    <NavLink to="/games" className={({ isActive }) => `${styles.link} ${isActive ? styles.active : ""}`}>
                        Games
                    </NavLink>
                )}
                <span className={styles.spacer} />
                {!loading && (player ? <UserMenu /> : <ButtonLink variant="secondary" to="/login">Sign in</ButtonLink>)}
            </nav>
        </header>
    );
}
