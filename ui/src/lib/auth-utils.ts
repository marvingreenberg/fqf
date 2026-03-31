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
