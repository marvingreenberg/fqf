/**
 * Shared identity/auth utilities used by IdentityGate and ShareLoginPane.
 */

import { createSchedule } from '$lib/api';
import { getFingerprint } from '$lib/fingerprint';
import { appState } from '$lib/stores.svelte';
import { FINGERPRINT_COUNTER_KEY } from '$lib/types';

export interface NewScheduleResult {
    token: string;
}

/**
 * Create a new schedule using the browser fingerprint and persisted counter.
 * Increments and persists the counter, then calls appState.confirm.
 */
/**
 * Display-only token rewrites. The real token (used for API calls and storage)
 * is unchanged; only the string shown to the user is remapped. Add entries here
 * when a user wants a friendlier-looking token without migrating backend data.
 */
const TOKEN_DISPLAY_ALIASES: Record<string, string> = {
    'brisk-crisp-mortician': 'wonderful-ray-sunshine'
};

const TOKEN_REVERSE_ALIASES: Record<string, string> = Object.fromEntries(
    Object.entries(TOKEN_DISPLAY_ALIASES).map(([real, alias]) => [alias, real])
);

/** Return the user-facing rendering of a token (may equal the input). */
export function displayToken(token: string | null | undefined): string {
    if (!token) return '';
    return TOKEN_DISPLAY_ALIASES[token] ?? token;
}

/**
 * Translate a user-entered alias back to its real token before hitting the
 * backend. Accepts whitespace/hyphen-normalized input; returns the real token
 * if the input matches a known alias, otherwise returns the input unchanged.
 */
export function reverseDisplayToken(input: string): string {
    const normalized = input.trim().toLowerCase().replace(/\s+/g, '-');
    return TOKEN_REVERSE_ALIASES[normalized] ?? input;
}

export async function createNewSchedule(name: string): Promise<NewScheduleResult> {
    const fingerprintHash = await getFingerprint();
    const rawCounter = localStorage.getItem(FINGERPRINT_COUNTER_KEY);
    const counter = rawCounter !== null ? parseInt(rawCounter, 10) || 0 : 0;

    const resp =
        fingerprintHash !== null
            ? await createSchedule(name, fingerprintHash, counter)
            : await createSchedule(name);

    const nextCounter = counter + 1;
    localStorage.setItem(FINGERPRINT_COUNTER_KEY, String(nextCounter));
    await appState.confirm(resp.token, name, nextCounter);
    return { token: resp.token };
}
