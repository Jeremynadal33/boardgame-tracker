import { useState, type FormEvent } from "react";
import { createGame, type Game } from "@/api/games";
import { ApiError } from "@/api/client";
import { Button } from "@/components/Button";
import { Field, TextAreaField } from "@/components/Field";
import { Modal } from "@/components/Modal";
import styles from "./AddGameModal.module.css";

type Props = { onCreated: (game: Game) => void; onCancel: () => void };

export function AddGameModal({ onCreated, onCancel }: Props) {
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [minPlayers, setMinPlayers] = useState("2");
    const [maxPlayers, setMaxPlayers] = useState("4");
    const [error, setError] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);

    async function handleSubmit(event: FormEvent) {
        event.preventDefault();
        setError(null);
        setSubmitting(true);
        try {
            const game = await createGame({
                name,
                description: description || null,
                min_players: Number(minPlayers),
                max_players: Number(maxPlayers),
            });
            onCreated(game);
        } catch (e) {
            setError(e instanceof ApiError ? e.message : "Something went wrong, please try again");
            setSubmitting(false);
        }
    }

    return (
        <Modal title="Add a game" subtitle="It will be available to everyone in the group.">
            <form className={styles.form} onSubmit={handleSubmit}>
                <Field label="Name" value={name} onChange={(e) => setName(e.target.value)} required />
                <TextAreaField label="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
                <div className={styles.row}>
                    <Field
                        label="Min players"
                        type="number"
                        min={1}
                        value={minPlayers}
                        onChange={(e) => setMinPlayers(e.target.value)}
                        required
                    />
                    <Field
                        label="Max players"
                        type="number"
                        min={1}
                        value={maxPlayers}
                        onChange={(e) => setMaxPlayers(e.target.value)}
                        required
                    />
                </div>
                {error && (
                    <p role="alert" className={styles.error}>
                        {error}
                    </p>
                )}
                <div className={styles.actions}>
                    <Button type="button" variant="secondary" onClick={onCancel}>
                        Cancel
                    </Button>
                    <Button type="submit" disabled={submitting}>
                        Add game
                    </Button>
                </div>
            </form>
        </Modal>
    );
}
