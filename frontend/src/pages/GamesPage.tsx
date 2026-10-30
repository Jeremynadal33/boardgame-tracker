import { useEffect, useState } from "react";
import { listGames, type Game } from "@/api/games";
import { Button } from "@/components/Button";
import { Card } from "@/components/Card";
import { AddGameModal } from "./AddGameModal";
import styles from "./GamesPage.module.css";

function playersLabel(game: Game): string {
    return game.min_players === game.max_players
        ? `${game.min_players}`
        : `${game.min_players}–${game.max_players}`;
}

export function GamesPage() {
    const [games, setGames] = useState<Game[]>([]);
    const [selectedId, setSelectedId] = useState<string | null>(null);
    const [query, setQuery] = useState("");
    const [adding, setAdding] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        listGames()
            .then(setGames)
            .catch(() => setError("Could not load the games"));
    }, []);

    const normalizedQuery = query.trim().toLowerCase();
    const filtered = games.filter((game) => game.name.toLowerCase().includes(normalizedQuery));
    const selected = games.find((game) => game.id === selectedId) ?? filtered[0] ?? null;

    function handleCreated(game: Game) {
        setGames((current) => [...current, game]);
        setSelectedId(game.id);
        setAdding(false);
    }

    return (
        <>
            <div className={styles.header}>
                <div>
                    <h1 className={styles.title}>Games</h1>
                    <p className={styles.count}>
                        {filtered.length} of {games.length} games
                    </p>
                </div>
                <div className={styles.tools}>
                    <input
                        className={styles.search}
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Search a game…"
                        aria-label="Search a game"
                    />
                    <Button onClick={() => setAdding(true)}>Add a game</Button>
                </div>
            </div>

            {error && <p role="alert">{error}</p>}

            <div className={styles.layout}>
                <ul className={styles.list}>
                    {filtered.map((game) => (
                        <li key={game.id}>
                            <button
                                className={`${styles.item} ${game.id === selected?.id ? styles.itemSelected : ""}`}
                                onClick={() => setSelectedId(game.id)}
                            >
                                <span>{game.name}</span>
                                <span className={styles.itemMeta}>{playersLabel(game)} players</span>
                            </button>
                        </li>
                    ))}
                </ul>

                {selected && (
                    <Card>
                        <h2 className={styles.detailTitle}>{selected.name}</h2>
                        <div className={styles.detailMeta}>{playersLabel(selected)} players</div>
                        {selected.description && <p className={styles.description}>{selected.description}</p>}
                    </Card>
                )}
            </div>

            {adding && <AddGameModal onCreated={handleCreated} onCancel={() => setAdding(false)} />}
        </>
    );
}
