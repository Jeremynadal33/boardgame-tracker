import { request } from "./client";

export type Player = { id: string; pseudo: string; email: string };

export function login(email: string, password: string): Promise<void> {
    return request("/players/login/access-token", {
        method: "POST",
        body: new URLSearchParams({ username: email, password }),
    });
}

export function logout(): Promise<void> {
    return request("/players/logout", { method: "POST" });
}

export function fetchCurrentPlayer(): Promise<Player> {
    return request<Player>("/players/me", undefined, { notifyUnauthorized: false });
}

export function signup(pseudo: string, email: string, password: string): Promise<Player> {
    return request<Player>("/players/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pseudo, email, password }),
    });
}
