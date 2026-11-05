import { request } from "./client";

export type Game = {
    id: string;
    name: string;
    description: string | null;
    min_players: number;
    max_players: number;
};

export type NewGame = Omit<Game, "id">;

export function listGames(): Promise<Game[]> {
    return request<Game[]>("/games/");
}

export function createGame(game: NewGame): Promise<Game> {
    return request<Game>("/games/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(game),
    });
}
