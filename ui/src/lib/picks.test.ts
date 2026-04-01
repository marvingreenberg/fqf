import { describe, it, expect } from 'vitest';
import {
    MAYBE_PREFIX,
    bareSlug,
    isPicked,
    isMaybe,
    isSelected,
    togglePick,
    toggleMaybe
} from '$lib/picks';

describe('bareSlug', () => {
    it('strips the maybe prefix from a prefixed slug', () => {
        expect(bareSlug('?my-act')).toBe('my-act');
    });

    it('returns bare slug unchanged', () => {
        expect(bareSlug('my-act')).toBe('my-act');
    });

    it('only strips one leading prefix', () => {
        expect(bareSlug('??double')).toBe('?double');
    });

    it('MAYBE_PREFIX is the ? character', () => {
        expect(MAYBE_PREFIX).toBe('?');
    });
});

describe('isPicked', () => {
    it('returns true when bare slug is in the set', () => {
        expect(isPicked('my-act', new Set(['my-act']))).toBe(true);
    });

    it('returns false when only ?-prefixed slug is in the set', () => {
        expect(isPicked('my-act', new Set(['?my-act']))).toBe(false);
    });

    it('returns false when slug is absent from set', () => {
        expect(isPicked('my-act', new Set())).toBe(false);
    });

    it('returns false when other slugs are present but not this one', () => {
        expect(isPicked('my-act', new Set(['other-act']))).toBe(false);
    });
});

describe('isMaybe', () => {
    it('returns true when ?-prefixed slug is in the set', () => {
        expect(isMaybe('my-act', new Set(['?my-act']))).toBe(true);
    });

    it('returns false when only bare slug is in the set', () => {
        expect(isMaybe('my-act', new Set(['my-act']))).toBe(false);
    });

    it('returns false when slug is absent from set', () => {
        expect(isMaybe('my-act', new Set())).toBe(false);
    });
});

describe('isSelected', () => {
    it('returns true when bare slug is in the set', () => {
        expect(isSelected('my-act', new Set(['my-act']))).toBe(true);
    });

    it('returns true when ?-prefixed slug is in the set', () => {
        expect(isSelected('my-act', new Set(['?my-act']))).toBe(true);
    });

    it('returns false when slug is absent from set', () => {
        expect(isSelected('my-act', new Set())).toBe(false);
    });

    it('returns false when other slugs are present but not this one', () => {
        expect(isSelected('my-act', new Set(['other-act', '?other-act']))).toBe(false);
    });
});

describe('togglePick', () => {
    it('transitions unpicked → picked', () => {
        const result = togglePick('my-act', new Set());
        expect(result.has('my-act')).toBe(true);
        expect(result.has('?my-act')).toBe(false);
    });

    it('transitions picked → unpicked', () => {
        const result = togglePick('my-act', new Set(['my-act']));
        expect(result.has('my-act')).toBe(false);
        expect(result.has('?my-act')).toBe(false);
    });

    it('transitions maybe → picked (clears maybe prefix)', () => {
        const result = togglePick('my-act', new Set(['?my-act']));
        expect(result.has('my-act')).toBe(true);
        expect(result.has('?my-act')).toBe(false);
    });

    it('returns a new Set (does not mutate)', () => {
        const original = new Set(['my-act']);
        const result = togglePick('my-act', original);
        expect(result).not.toBe(original);
        expect(original.has('my-act')).toBe(true);
    });

    it('preserves other entries in the set', () => {
        const result = togglePick('my-act', new Set(['other-act', '?another-act']));
        expect(result.has('other-act')).toBe(true);
        expect(result.has('?another-act')).toBe(true);
    });
});

describe('toggleMaybe', () => {
    it('transitions unpicked → maybe', () => {
        const result = toggleMaybe('my-act', new Set());
        expect(result.has('?my-act')).toBe(true);
        expect(result.has('my-act')).toBe(false);
    });

    it('transitions maybe → unpicked', () => {
        const result = toggleMaybe('my-act', new Set(['?my-act']));
        expect(result.has('?my-act')).toBe(false);
        expect(result.has('my-act')).toBe(false);
    });

    it('transitions picked → maybe (clears bare slug)', () => {
        const result = toggleMaybe('my-act', new Set(['my-act']));
        expect(result.has('?my-act')).toBe(true);
        expect(result.has('my-act')).toBe(false);
    });

    it('returns a new Set (does not mutate)', () => {
        const original = new Set<string>();
        const result = toggleMaybe('my-act', original);
        expect(result).not.toBe(original);
        expect(original.has('?my-act')).toBe(false);
    });

    it('preserves other entries in the set', () => {
        const result = toggleMaybe('my-act', new Set(['other-act', '?another-act']));
        expect(result.has('other-act')).toBe(true);
        expect(result.has('?another-act')).toBe(true);
    });
});
