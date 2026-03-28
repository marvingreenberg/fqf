<script lang="ts">
    import { createSchedule, loadSchedule } from '$lib/api';
    import { appState } from '$lib/stores.svelte';

    type DialogMode = 'choose' | 'create' | 'load';

    interface Props {
        open: boolean;
    }

    let { open = $bindable() }: Props = $props();

    let mode = $state<DialogMode>('choose');
    let tokenInput = $state('');
    let errorMsg = $state('');
    let loading = $state(false);

    function resetState() {
        mode = 'choose';
        tokenInput = '';
        errorMsg = '';
        loading = false;
    }

    function close() {
        open = false;
        resetState();
    }

    function handleOverlayClick(e: MouseEvent) {
        if (e.target === e.currentTarget) close();
    }

    async function handleNewSchedule() {
        loading = true;
        try {
            const resp = await createSchedule();
            appState.token = resp.token;
            appState.clearPicks();
            mode = 'create';
        } finally {
            loading = false;
        }
    }

    async function handleLoadSchedule() {
        const trimmed = tokenInput.trim();
        if (!trimmed) {
            errorMsg = 'Please enter your secret words.';
            return;
        }
        loading = true;
        errorMsg = '';
        try {
            const resp = await loadSchedule(trimmed);
            appState.token = resp.token;
            appState.picks = new Set(resp.picks);
            close();
        } catch {
            errorMsg = 'Could not find that schedule. Check your secret words and try again.';
        } finally {
            loading = false;
        }
    }

    function handleKeydown(e: KeyboardEvent) {
        if (e.key === 'Escape') close();
    }
</script>

{#if open}
    <div
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
        onclick={handleOverlayClick}
        onkeydown={handleKeydown}
        role="dialog"
        tabindex="-1"
        aria-modal="true"
        aria-label="Schedule dialog"
    >
        <div class="bg-surface-50 rounded-xl shadow-xl w-full max-w-sm mx-4 p-6">
            {#if mode === 'choose'}
                <h2 class="text-xl font-bold mb-2">My Schedule</h2>
                <p class="text-sm text-surface-600 mb-6">
                    Save picks across devices with a set of secret words.
                </p>
                <div class="flex flex-col gap-3">
                    <button
                        class="btn preset-filled-primary-500 w-full"
                        onclick={handleNewSchedule}
                        disabled={loading}
                    >
                        {loading ? 'Creating…' : 'New Schedule'}
                    </button>
                    <button
                        class="btn preset-outlined-surface-500 w-full"
                        onclick={() => {
                            mode = 'load';
                        }}
                        disabled={loading}
                    >
                        I Have Secret Words
                    </button>
                    <button class="btn preset-ghost w-full text-sm" onclick={close}>Cancel</button>
                </div>
            {:else if mode === 'create'}
                <h2 class="text-xl font-bold mb-2">Your Secret Words</h2>
                <p class="text-sm text-surface-600 mb-4">
                    Write these down — you'll need them to reload your schedule on another device.
                </p>
                <div
                    class="bg-primary-50 border border-primary-200 rounded-lg px-4 py-6 text-center mb-6"
                >
                    <span class="text-2xl font-bold tracking-wide text-primary-700 break-all">
                        {appState.token}
                    </span>
                </div>
                <button class="btn preset-filled-primary-500 w-full" onclick={close}>
                    Got It
                </button>
            {:else if mode === 'load'}
                <h2 class="text-xl font-bold mb-2">Load Schedule</h2>
                <p class="text-sm text-surface-600 mb-4">
                    Enter your secret words to restore picks.
                </p>
                <input
                    class="input mb-2 w-full"
                    type="text"
                    placeholder="Your secret words…"
                    bind:value={tokenInput}
                    onkeydown={(e) => e.key === 'Enter' && handleLoadSchedule()}
                />
                {#if errorMsg}
                    <p class="text-error-600 text-sm mb-3">{errorMsg}</p>
                {/if}
                <div class="flex flex-col gap-2 mt-3">
                    <button
                        class="btn preset-filled-primary-500 w-full"
                        onclick={handleLoadSchedule}
                        disabled={loading}
                    >
                        {loading ? 'Loading…' : 'Load Schedule'}
                    </button>
                    <button
                        class="btn preset-outlined-surface-500 w-full"
                        onclick={() => {
                            mode = 'choose';
                            errorMsg = '';
                        }}
                        disabled={loading}
                    >
                        Back
                    </button>
                </div>
            {/if}
        </div>
    </div>
{/if}
