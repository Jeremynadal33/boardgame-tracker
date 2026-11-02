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

let unauthorizedHandler: (() => void) | null = null;

export function setUnauthorizedHandler(handler: (() => void) | null): void {
    unauthorizedHandler = handler;
}

type RequestOptions = {
    // False for the session probe, whose 401 only means "nobody is logged in"
    notifyUnauthorized?: boolean;
};

export async function request<T = void>(
    path: string,
    init?: RequestInit,
    { notifyUnauthorized = true }: RequestOptions = {},
): Promise<T> {
    const response = await fetch(`${API_PREFIX}${path}`, { credentials: "same-origin", ...init });
    if (!response.ok) {
        if (response.status === 401 && notifyUnauthorized) unauthorizedHandler?.();
        const body = await response.json().catch(() => null);
        throw new ApiError(response.status, toMessage(body?.detail, response.statusText));
    }
    if (response.status === 204) return undefined as T;
    return response.json() as Promise<T>;
}
