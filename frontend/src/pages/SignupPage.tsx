import { useState, type FormEvent } from "react";
import { Link, Navigate, useNavigate } from "react-router";
import { ApiError } from "@/api/client";
import { useAuth } from "@/auth/AuthContext";
import { AuthLayout } from "@/components/AuthLayout";
import { Button } from "@/components/Button";
import { Field } from "@/components/Field";

export function SignupPage() {
    const { player, signup } = useAuth();
    const navigate = useNavigate();
    const [pseudo, setPseudo] = useState("");
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
            await signup(pseudo, email, password);
            navigate("/games", { replace: true });
        } catch (e) {
            setError(e instanceof ApiError ? e.message : "Something went wrong, please try again");
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <AuthLayout
            title="Create an account"
            subtitle="Join your group on Scorepad."
            error={error}
            onSubmit={handleSubmit}
            footnote={
                <>
                    Already have an account? <Link to="/login">Sign in</Link>
                </>
            }
        >
            <Field label="Pseudo" value={pseudo} maxLength={30} onChange={(e) => setPseudo(e.target.value)} required />
            <Field label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <Field
                label="Password"
                type="password"
                value={password}
                minLength={8}
                maxLength={72}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <Button type="submit" disabled={submitting}>
                Create account
            </Button>
        </AuthLayout>
    );
}
