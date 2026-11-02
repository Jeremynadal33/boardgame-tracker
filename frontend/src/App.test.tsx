import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";
import { mockApi } from "./test/mockApi";

const player = { id: "1", pseudo: "toto", email: "toto@example.com" };
const catan = { id: "g1", name: "Catan", description: "Trade and build", min_players: 3, max_players: 4 };

beforeEach(() => window.history.pushState({}, "", "/"));
afterEach(() => vi.unstubAllGlobals());

describe("route guard", () => {
    it("redirects an anonymous visitor to the login page", async () => {
        window.history.pushState({}, "", "/games");
        mockApi({ "GET /api/v1/players/me": () => ({ status: 401, body: { detail: "Not authenticated" } }) });

        render(<App />);

        expect(await screen.findByRole("heading", { name: "Welcome back" })).toBeInTheDocument();
        expect(window.location.pathname).toBe("/login");
    });

    it("shows the games to a logged player", async () => {
        window.history.pushState({}, "", "/games");
        mockApi({
            "GET /api/v1/players/me": () => ({ status: 200, body: player }),
            "GET /api/v1/games/": () => ({ status: 200, body: [catan] }),
        });

        render(<App />);

        expect(await screen.findByRole("heading", { name: "Catan" })).toBeInTheDocument();
        expect(window.location.pathname).toBe("/games");
    });
});

describe("home page", () => {
    it("is public and offers to sign in", async () => {
        mockApi({ "GET /api/v1/players/me": () => ({ status: 401, body: { detail: "Not authenticated" } }) });

        render(<App />);

        expect(await screen.findByRole("heading", { name: "Every game night, remembered." })).toBeInTheDocument();
        expect(screen.getAllByRole("link", { name: "Sign in" })).toHaveLength(2);
        expect(screen.getByRole("link", { name: "Create an account" })).toHaveAttribute("href", "/signup");
        expect(window.location.pathname).toBe("/");
    });

    it("shows the initials of a logged player and a link to the games", async () => {
        mockApi({ "GET /api/v1/players/me": () => ({ status: 200, body: { ...player, pseudo: "Camille Roche" } }) });

        render(<App />);

        expect(await screen.findByRole("button", { name: "Account menu" })).toHaveTextContent("CR");
        expect(screen.getByRole("link", { name: "Browse games" })).toHaveAttribute("href", "/games");
    });
});

describe("login", () => {
    function mockLogin(loginResponse: { status: number; body?: unknown }) {
        window.history.pushState({}, "", "/login");
        let logged = false;
        return mockApi({
            "GET /api/v1/players/me": () =>
                logged ? { status: 200, body: player } : { status: 401, body: { detail: "Not authenticated" } },
            "POST /api/v1/players/login/access-token": () => {
                logged = loginResponse.status === 204;
                return loginResponse;
            },
            "GET /api/v1/games/": () => ({ status: 200, body: [] }),
        });
    }

    it("logs in and lands on the games page", async () => {
        const calls = mockLogin({ status: 204 });
        render(<App />);

        await userEvent.type(await screen.findByLabelText("Email"), "toto@example.com");
        await userEvent.type(screen.getByLabelText("Password"), "securepassword123");
        await userEvent.click(screen.getByRole("button", { name: "Sign in" }));

        expect(await screen.findByRole("heading", { name: "Games" })).toBeInTheDocument();
        const loginCall = calls.find((call) => call.url.endsWith("/login/access-token"));
        expect(String(loginCall?.init?.body)).toBe("username=toto%40example.com&password=securepassword123");
    });

    it("shows the error returned by the API", async () => {
        mockLogin({ status: 400, body: { detail: "Incorrect email or password" } });
        render(<App />);

        await userEvent.type(await screen.findByLabelText("Email"), "toto@example.com");
        await userEvent.type(screen.getByLabelText("Password"), "wrong");
        await userEvent.click(screen.getByRole("button", { name: "Sign in" }));

        expect(await screen.findByRole("alert")).toHaveTextContent("Incorrect email or password");
        expect(window.location.pathname).toBe("/login");
    });
});

describe("signup", () => {
    function mockSignup(signupResponse: { status: number; body?: unknown }) {
        window.history.pushState({}, "", "/signup");
        let logged = false;
        return mockApi({
            "GET /api/v1/players/me": () =>
                logged ? { status: 200, body: player } : { status: 401, body: { detail: "Not authenticated" } },
            "POST /api/v1/players/signup": () => signupResponse,
            "POST /api/v1/players/login/access-token": () => {
                logged = true;
                return { status: 204 };
            },
            "GET /api/v1/games/": () => ({ status: 200, body: [] }),
        });
    }

    async function fillAndSubmit() {
        await userEvent.type(await screen.findByLabelText("Pseudo"), "toto");
        await userEvent.type(screen.getByLabelText("Email"), "toto@example.com");
        await userEvent.type(screen.getByLabelText("Password"), "securepassword123");
        await userEvent.click(screen.getByRole("button", { name: "Create account" }));
    }

    it("creates the account, logs in and lands on the games page", async () => {
        const calls = mockSignup({ status: 201, body: player });
        render(<App />);

        await fillAndSubmit();

        expect(await screen.findByRole("heading", { name: "Games" })).toBeInTheDocument();
        const signupCall = calls.find((call) => call.url.endsWith("/players/signup"));
        expect(JSON.parse(String(signupCall?.init?.body))).toEqual({
            pseudo: "toto",
            email: "toto@example.com",
            password: "securepassword123",
        });
    });

    it("shows the error returned by the API", async () => {
        mockSignup({ status: 409, body: { detail: "A player with the pseudo 'toto' already exists" } });
        render(<App />);

        await fillAndSubmit();

        expect(await screen.findByRole("alert")).toHaveTextContent("already exists");
        expect(window.location.pathname).toBe("/signup");
    });
});

describe("logout", () => {
    it("is in the avatar menu and goes back to the home page", async () => {
        window.history.pushState({}, "", "/games");
        mockApi({
            "GET /api/v1/players/me": () => ({ status: 200, body: player }),
            "GET /api/v1/games/": () => ({ status: 200, body: [] }),
            "POST /api/v1/players/logout": () => ({ status: 204 }),
        });
        render(<App />);

        expect(screen.queryByRole("menuitem", { name: "Logout" })).not.toBeInTheDocument();
        await userEvent.click(await screen.findByRole("button", { name: "Account menu" }));
        await userEvent.click(screen.getByRole("menuitem", { name: "Logout" }));

        expect(await screen.findByRole("heading", { name: "Every game night, remembered." })).toBeInTheDocument();
        expect(window.location.pathname).toBe("/");
    });
});

describe("add a game", () => {
    function mockGames(createResponse: { status: number; body: unknown }) {
        window.history.pushState({}, "", "/games");
        return mockApi({
            "GET /api/v1/players/me": () => ({ status: 200, body: player }),
            "GET /api/v1/games/": () => ({ status: 200, body: [catan] }),
            "POST /api/v1/games/": () => createResponse,
        });
    }

    async function fillAndSubmit(name: string) {
        await userEvent.click(await screen.findByRole("button", { name: "Add a game" }));
        await userEvent.type(screen.getByLabelText("Name"), name);
        await userEvent.click(screen.getByRole("button", { name: "Add game" }));
    }

    it("adds the game to the list and selects it", async () => {
        const azul = { id: "g2", name: "Azul", description: null, min_players: 2, max_players: 4 };
        const calls = mockGames({ status: 201, body: azul });
        render(<App />);

        await fillAndSubmit("Azul");

        expect(await screen.findByRole("heading", { name: "Azul" })).toBeInTheDocument();
        expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
        const createCall = calls.find((call) => call.init?.method === "POST");
        expect(JSON.parse(String(createCall?.init?.body))).toEqual({
            name: "Azul",
            description: null,
            min_players: 2,
            max_players: 4,
        });
    });

    it("shows a name conflict and keeps the modal open", async () => {
        mockGames({ status: 409, body: { detail: "A game with the name 'Catan' already exists" } });
        render(<App />);

        await fillAndSubmit("Catan");

        await waitFor(() => expect(screen.getByRole("alert")).toHaveTextContent("already exists"));
        expect(screen.getByRole("dialog")).toBeInTheDocument();
    });
});

function deferred<T>() {
    let resolve!: (value: T) => void;
    const promise = new Promise<T>((r) => (resolve = r));
    return { promise, resolve };
}

describe("races on first load", () => {
    it("a late 401 from the initial session check does not undo a login", async () => {
        window.history.pushState({}, "", "/login");
        const initialCheck = deferred<{ status: number; body: unknown }>();
        let meCalls = 0;
        mockApi({
            "GET /api/v1/players/me": () =>
                ++meCalls === 1 ? initialCheck.promise : { status: 200, body: player },
            "POST /api/v1/players/login/access-token": () => ({ status: 204 }),
            "GET /api/v1/games/": () => ({ status: 200, body: [] }),
        });
        render(<App />);

        await userEvent.type(await screen.findByLabelText("Email"), "toto@example.com");
        await userEvent.type(screen.getByLabelText("Password"), "securepassword123");
        await userEvent.click(screen.getByRole("button", { name: "Sign in" }));
        expect(await screen.findByRole("heading", { name: "Games" })).toBeInTheDocument();

        initialCheck.resolve({ status: 401, body: { detail: "Not authenticated" } });

        await waitFor(() => expect(meCalls).toBe(2));
        expect(screen.getByRole("heading", { name: "Games" })).toBeInTheDocument();
        expect(window.location.pathname).toBe("/games");
    });

    it("keeps a game created while the list was still loading", async () => {
        window.history.pushState({}, "", "/games");
        const azul = { id: "g2", name: "Azul", description: null, min_players: 2, max_players: 4 };
        const initialList = deferred<{ status: number; body: unknown }>();
        mockApi({
            "GET /api/v1/players/me": () => ({ status: 200, body: player }),
            "GET /api/v1/games/": () => initialList.promise,
            "POST /api/v1/games/": () => ({ status: 201, body: azul }),
        });
        render(<App />);

        await userEvent.click(await screen.findByRole("button", { name: "Add a game" }));
        await userEvent.type(screen.getByLabelText("Name"), "Azul");
        await userEvent.click(screen.getByRole("button", { name: "Add game" }));
        expect(await screen.findByRole("heading", { name: "Azul" })).toBeInTheDocument();

        initialList.resolve({ status: 200, body: [catan] });

        expect(await screen.findByRole("button", { name: /Catan/ })).toBeInTheDocument();
        expect(screen.getByRole("heading", { name: "Azul" })).toBeInTheDocument();
    });
});

describe("games search", () => {
    const azul = { id: "g2", name: "Azul", description: "Tiles", min_players: 2, max_players: 4 };

    beforeEach(() => {
        window.history.pushState({}, "", "/games");
        mockApi({
            "GET /api/v1/players/me": () => ({ status: 200, body: player }),
            "GET /api/v1/games/": () => ({ status: 200, body: [catan, azul] }),
        });
    });

    it("shows the details of a game that matches the search, not the previously selected one", async () => {
        render(<App />);

        await userEvent.click(await screen.findByRole("button", { name: /Catan/ }));
        await userEvent.type(screen.getByLabelText("Search a game"), "Azul");

        expect(screen.getByRole("heading", { name: "Azul" })).toBeInTheDocument();
        expect(screen.queryByRole("heading", { name: "Catan" })).not.toBeInTheDocument();
    });

    it("shows no details when nothing matches", async () => {
        render(<App />);

        await userEvent.click(await screen.findByRole("button", { name: /Catan/ }));
        await userEvent.type(screen.getByLabelText("Search a game"), "zzz");

        expect(screen.queryByRole("heading", { name: "Catan" })).not.toBeInTheDocument();
    });
});

describe("add a game modal", () => {
    beforeEach(() => {
        window.history.pushState({}, "", "/games");
    });

    it("closes when clicking outside of it or pressing escape", async () => {
        mockApi({
            "GET /api/v1/players/me": () => ({ status: 200, body: player }),
            "GET /api/v1/games/": () => ({ status: 200, body: [catan] }),
        });
        render(<App />);

        await userEvent.click(await screen.findByRole("button", { name: "Add a game" }));
        await userEvent.click(screen.getByRole("dialog"));
        expect(screen.queryByRole("dialog")).not.toBeInTheDocument();

        await userEvent.click(screen.getByRole("button", { name: "Add a game" }));
        fireEvent(screen.getByRole("dialog"), new Event("cancel", { cancelable: true }));
        expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    });

    it("stays open when clicking inside of it", async () => {
        mockApi({
            "GET /api/v1/players/me": () => ({ status: 200, body: player }),
            "GET /api/v1/games/": () => ({ status: 200, body: [catan] }),
        });
        render(<App />);

        await userEvent.click(await screen.findByRole("button", { name: "Add a game" }));
        await userEvent.click(screen.getByLabelText("Name"));

        expect(screen.getByRole("dialog")).toBeInTheDocument();
    });

    it("refuses a minimum above the maximum without calling the API", async () => {
        const calls = mockApi({
            "GET /api/v1/players/me": () => ({ status: 200, body: player }),
            "GET /api/v1/games/": () => ({ status: 200, body: [catan] }),
        });
        render(<App />);

        await userEvent.click(await screen.findByRole("button", { name: "Add a game" }));
        await userEvent.type(screen.getByLabelText("Name"), "Azul");
        await userEvent.clear(screen.getByLabelText("Min players"));
        await userEvent.type(screen.getByLabelText("Min players"), "5");
        await userEvent.clear(screen.getByLabelText("Max players"));
        await userEvent.type(screen.getByLabelText("Max players"), "2");
        await userEvent.click(screen.getByRole("button", { name: "Add game" }));

        expect(screen.getByRole("alert")).toHaveTextContent("Min players must not exceed max players");
        expect(calls.some((call) => call.init?.method === "POST")).toBe(false);
    });
});

describe("session handling", () => {
    it("sends the player back to the login page when the session expired", async () => {
        window.history.pushState({}, "", "/games");
        mockApi({
            "GET /api/v1/players/me": () => ({ status: 200, body: player }),
            "GET /api/v1/games/": () => ({ status: 200, body: [catan] }),
            "POST /api/v1/games/": () => ({ status: 401, body: { detail: "Token has expired" } }),
        });
        render(<App />);

        await userEvent.click(await screen.findByRole("button", { name: "Add a game" }));
        await userEvent.type(screen.getByLabelText("Name"), "Azul");
        await userEvent.click(screen.getByRole("button", { name: "Add game" }));

        expect(await screen.findByRole("heading", { name: "Welcome back" })).toBeInTheDocument();
        expect(window.location.pathname).toBe("/login");
    });

    it("signs the player out locally even when the logout request fails", async () => {
        window.history.pushState({}, "", "/games");
        mockApi({
            "GET /api/v1/players/me": () => ({ status: 200, body: player }),
            "GET /api/v1/games/": () => ({ status: 200, body: [] }),
            "POST /api/v1/players/logout": () => ({ status: 500, body: { detail: "boom" } }),
        });
        render(<App />);

        await userEvent.click(await screen.findByRole("button", { name: "Account menu" }));
        await userEvent.click(screen.getByRole("menuitem", { name: "Logout" }));

        expect(await screen.findByRole("heading", { name: "Every game night, remembered." })).toBeInTheDocument();
        await waitFor(() => expect(screen.queryByRole("button", { name: "Account menu" })).not.toBeInTheDocument());
    });
});
