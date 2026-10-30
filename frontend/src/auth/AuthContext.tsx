import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import * as authApi from "@/api/auth";
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

    useEffect(() => {
        authApi
            .fetchCurrentPlayer()
            .then(setPlayer)
            .catch(() => setPlayer(null))
            .finally(() => setLoading(false));
    }, []);

    const login = useCallback(async (email: string, password: string) => {
        await authApi.login(email, password);
        setPlayer(await authApi.fetchCurrentPlayer());
    }, []);

    const signup = useCallback(
        async (pseudo: string, email: string, password: string) => {
            await authApi.signup(pseudo, email, password);
            await login(email, password);
        },
        [login],
    );

    const logout = useCallback(async () => {
        await authApi.logout();
        setPlayer(null);
    }, []);

    const value = useMemo(() => ({ player, loading, login, signup, logout }), [player, loading, login, signup, logout]);
    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
    const context = useContext(AuthContext);
    if (!context) throw new Error("useAuth must be used inside AuthProvider");
    return context;
}
