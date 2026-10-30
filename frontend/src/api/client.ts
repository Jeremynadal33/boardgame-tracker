const API_PREFIX = "/api/v1";

export class ApiError extends Error {
    constructor(
        public status: number,
        message: string,
    ) {
        super(message);
    }
}

type ValidationIssue = { msg: string };

function toMessage(detail: unknown, fallback: string): string {
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail)) return (detail as ValidationIssue[]).map((issue) => issue.msg).join(", ");
    return fallback;
}

export async function request<T = void>(path: string, init?: RequestInit): Promise<T> {
    const response = await fetch(`${API_PREFIX}${path}`, { credentials: "same-origin", ...init });
    if (!response.ok) {
        const body = await response.json().catch(() => null);
        throw new ApiError(response.status, toMessage(body?.detail, response.statusText));
    }
    if (response.status === 204) return undefined as T;
    return response.json() as Promise<T>;
}
