import type { Player } from "@/api/auth";

export function initialsOf(player: Pick<Player, "pseudo" | "email">): string {
    const words = player.pseudo.trim().split(/[\s_.-]+/).filter(Boolean);
    if (words.length >= 2) return (words[0][0] + words[1][0]).toUpperCase();
    const source = words[0] ?? player.email.split("@")[0];
    return source.slice(0, 2).toUpperCase();
}
