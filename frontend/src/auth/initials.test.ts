import { describe, expect, it } from "vitest";
import { initialsOf } from "./initials";

const email = "jean.dupont@example.com";

describe("initialsOf", () => {
    it("uses the first letters of the first two words of the pseudo", () => {
        expect(initialsOf({ pseudo: "Camille Roche", email })).toBe("CR");
        expect(initialsOf({ pseudo: "camille_roche", email })).toBe("CR");
    });

    it("uses the first two letters of a single-word pseudo", () => {
        expect(initialsOf({ pseudo: "toto", email })).toBe("TO");
    });

    it("falls back on the email when there is no pseudo", () => {
        expect(initialsOf({ pseudo: "  ", email })).toBe("JE");
    });
});
