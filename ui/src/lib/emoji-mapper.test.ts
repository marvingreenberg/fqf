import { describe, it, expect } from 'vitest';
import { assignEmojis } from '$lib/emoji-mapper';

describe('assignEmojis', () => {
    it('assigns unique emojis to each token', () => {
        const result = assignEmojis(['token-a', 'token-b']);
        const emojis = Object.values(result);
        expect(new Set(emojis).size).toBe(2);
    });

    it('is deterministic for same set of tokens', () => {
        const a = assignEmojis(['token-a', 'token-b']);
        const b = assignEmojis(['token-a', 'token-b']);
        expect(a).toEqual(b);
    });

    it('is deterministic regardless of input order', () => {
        const a = assignEmojis(['token-a', 'token-b']);
        const b = assignEmojis(['token-b', 'token-a']);
        expect(a).toEqual(b);
    });

    it('handles up to 5 tokens', () => {
        const tokens = ['a', 'b', 'c', 'd', 'e'];
        const result = assignEmojis(tokens);
        expect(Object.keys(result).length).toBe(5);
        expect(new Set(Object.values(result)).size).toBe(5);
    });
});
