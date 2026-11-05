type MockResponse = { status: number; body?: unknown };
type Handler = (init?: RequestInit) => MockResponse | Promise<MockResponse>;

export function mockApi(routes: Record<string, Handler>) {
    const calls: { url: string; init?: RequestInit }[] = [];
    vi.stubGlobal(
        "fetch",
        vi.fn(async (url: string, init?: RequestInit) => {
            calls.push({ url, init });
            const key = `${init?.method ?? "GET"} ${url}`;
            const handler = routes[key];
            if (!handler) throw new Error(`Unmocked request: ${key}`);
            const { status, body } = await handler(init);
            return new Response(body === undefined ? null : JSON.stringify(body), { status });
        }),
    );
    return calls;
}
