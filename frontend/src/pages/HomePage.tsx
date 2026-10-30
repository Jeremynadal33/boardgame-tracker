import { useAuth } from "@/auth/AuthContext";
import { ButtonLink } from "@/components/ButtonLink";
import { Card } from "@/components/Card";
import styles from "./HomePage.module.css";

const ideas = [
    { title: "Your games", text: "Keep the list of the board games your group owns and plays." },
    { title: "Your sessions", text: "Log who played, who won and the scores, in a few seconds." },
    { title: "Your stats", text: "See win rates and rivalries build up over the months." },
];

export function HomePage() {
    const { player } = useAuth();

    return (
        <>
            <section className={styles.hero}>
                <div className="eyebrow">Board game score tracker</div>
                <h1 className={styles.title}>Every game night, remembered.</h1>
                <p className={styles.lead}>
                    Scorepad is a small place for your group to keep track of the board games you play, and
                    eventually of who actually won.
                </p>
                <div className={styles.actions}>
                    {player ? (
                        <ButtonLink to="/games">Browse games</ButtonLink>
                    ) : (
                        <>
                            <ButtonLink to="/signup">Create an account</ButtonLink>
                            <ButtonLink variant="secondary" to="/login">
                                Sign in
                            </ButtonLink>
                        </>
                    )}
                </div>
            </section>
            <div className={styles.ideas}>
                {ideas.map((idea) => (
                    <Card key={idea.title}>
                        <h2 className={styles.ideaTitle}>{idea.title}</h2>
                        <p className={styles.ideaText}>{idea.text}</p>
                    </Card>
                ))}
            </div>
        </>
    );
}
