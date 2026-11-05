import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import * as authApi from "@/api/auth";
import { setUnauthorizedHandler } from "@/api/client";
import type { Player } from "@/api/auth";

type AuthState = {
    player: Player | null;
    loading: boolean;
    login: (email: string, password: string) => Promise<void>;
    signup: (pseudo: string, email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [player, setPlayer] = useState<Player | null>(null);
    const [loading, setLoading] = useState(true);

    // Bumped by every login/logout so that a slower, older response never overwrites a newer state
    const generation = useRef(0);

    useEffect(() => {
        const startedAt = generation.current;
        const isStale = () => generation.current !== startedAt;
        authApi
            .fetchCurrentPlayer()
            .then((current) => {
                if (!isStale()) setPlayer(current);
            })
            .catch(() => {
                if (!isStale()) setPlayer(null);
            })
            .finally(() => setLoading(false));
    }, []);

    useEffect(() => {
        setUnauthorizedHandler(() => {
            generation.current += 1;
            setPlayer(null);
            setLoading(false);
        });
        return () => setUnauthorizedHandler(null);
    }, []);

    const login = useCallback(async (email: string, password: string) => {
        generation.current += 1;
        await authApi.login(email, password);
        setPlayer(await authApi.fetchCurrentPlayer());
        setLoading(false);
    }, []);

    const signup = useCallback(
        async (pseudo: string, email: string, password: string) => {
            await authApi.signup(pseudo, email, password);
            await login(email, password);
        },
        [login],
    );

    const logout = useCallback(async () => {
        generation.current += 1;
        try {
            await authApi.logout();
        } finally {
            setPlayer(null);
            setLoading(false);
        }
    }, []);

    const value = useMemo(() => ({ player, loading, login, signup, logout }), [player, loading, login, signup, logout]);
    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
    const context = useContext(AuthContext);
    if (!context) throw new Error("useAuth must be used inside AuthProvider");
    return context;
}
