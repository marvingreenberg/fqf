import { describe, it, expect } from 'vitest';
import { displayName } from '$lib/display';

describe('displayName', () => {
    it('strips a leading "The " with capital T', () => {
        expect(displayName('The Quickening')).toBe('Quickening');
    });

    it('strips a leading "the " lowercase', () => {
        expect(displayName('the soul rebels')).toBe('soul rebels');
    });

    it('strips when followed by a tab or multiple spaces', () => {
        expect(displayName('The   Lilli White Band')).toBe('Lilli White Band');
    });

    it('does not strip "The" in the middle of a name', () => {
        expect(displayName('Bon Bon Vivant The Band')).toBe('Bon Bon Vivant The Band');
    });

    it('does not strip a name beginning with "Then"', () => {
        // The regex requires whitespace after "the", so "Then" stays put.
        expect(displayName('Then Came The Last Days of May')).toBe(
            'Then Came The Last Days of May'
        );
    });

    it('returns an empty string unchanged', () => {
        expect(displayName('')).toBe('');
    });

    it('returns a one-word name unchanged when the word is not "The"', () => {
        expect(displayName('Juice')).toBe('Juice');
    });

    it('strips only the first occurrence', () => {
        expect(displayName('The The Band')).toBe('The Band');
    });
});
