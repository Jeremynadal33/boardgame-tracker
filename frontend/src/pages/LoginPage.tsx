import { useState, type FormEvent } from "react";
import { Link, Navigate, useNavigate } from "react-router";
import { ApiError } from "@/api/client";
import { useAuth } from "@/auth/AuthContext";
import { AuthLayout } from "@/components/AuthLayout";
import { Button } from "@/components/Button";
import { Field } from "@/components/Field";

export function LoginPage() {
    const { player, login } = useAuth();
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);

    if (player) return <Navigate to="/games" replace />;

    async function handleSubmit(event: FormEvent) {
        event.preventDefault();
        setError(null);
        setSubmitting(true);
        try {
            await login(email, password);
            navigate("/games", { replace: true });
        } catch (e) {
            setError(e instanceof ApiError ? e.message : "Something went wrong, please try again");
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <AuthLayout
            title="Welcome back"
            subtitle="Sign in to log tonight's scores."
            error={error}
            onSubmit={handleSubmit}
            footnote={
                <>
                    New here? <Link to="/signup">Create an account</Link>
                </>
            }
        >
            <Field label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <Field
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <Button type="submit" disabled={submitting}>
                Sign in
            </Button>
        </AuthLayout>
    );
}
