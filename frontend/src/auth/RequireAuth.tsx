import { Navigate, Outlet } from "react-router";
import { useAuth } from "./AuthContext";

export function RequireAuth() {
    const { player, loading } = useAuth();
    if (loading) return null;
    return player ? <Outlet /> : <Navigate to="/login" replace />;
}
