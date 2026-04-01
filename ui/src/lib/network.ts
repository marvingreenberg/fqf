import type { AppState } from '$lib/stores.svelte';

/**
 * Initialises browser network-status watching and ties it to AppState.
 *
 * Call once from the main layout's onMount. The returned cleanup function
 * removes the event listeners (useful for SSR / test teardown).
 */
export function initNetworkWatcher(appState: AppState): () => void {
    if (typeof window === 'undefined') return () => {};

    function handleOnline() {
        appState.isOnline = true;
        // Flush any queued / failed saves now that connectivity is back.
        appState.flushSaveIfPending();
    }

    function handleOffline() {
        appState.isOnline = false;
    }

    // Sync immediately with the current browser state.
    appState.isOnline = navigator.onLine;

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
        window.removeEventListener('online', handleOnline);
        window.removeEventListener('offline', handleOffline);
    };
}
