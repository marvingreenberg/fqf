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
        <div class="fqf-dialog-card w-full max-w-sm mx-4">
            {#if mode === 'choose'}
                <div class="fqf-dialog-header">
                    <h2>My Schedule</h2>
                    <p>Save picks across devices with a set of secret words.</p>
                </div>
                <div class="fqf-dialog-body flex flex-col gap-3">
                    <button class="fqf-btn-gold" onclick={handleNewSchedule} disabled={loading}>
                        {loading ? 'Creating…' : 'New Schedule'}
                    </button>
                    <button
                        class="fqf-btn-outline"
                        onclick={() => {
                            mode = 'load';
                        }}
                        disabled={loading}
                    >
                        I Have Secret Words
                    </button>
                    <button class="fqf-btn-ghost" onclick={close}>Cancel</button>
                </div>
            {:else if mode === 'create'}
                <div class="fqf-dialog-header">
                    <h2>Your Secret Words</h2>
                    <p>
                        Write these down — you'll need them to reload your schedule on another
                        device.
                    </p>
                </div>
                <div class="fqf-dialog-body">
                    <div class="fqf-token-box">
                        <span class="fqf-token-text">{appState.token}</span>
                    </div>
                    <button class="fqf-btn-primary" onclick={close}>Got It</button>
                </div>
            {:else if mode === 'load'}
                <div class="fqf-dialog-header">
                    <h2>Load Schedule</h2>
                    <p>Enter your secret words to restore picks.</p>
                </div>
                <div class="fqf-dialog-body">
                    <input
                        class="input mb-2 w-full"
                        type="text"
                        placeholder="Your secret words…"
                        bind:value={tokenInput}
                        onkeydown={(e) => e.key === 'Enter' && handleLoadSchedule()}
                    />
                    {#if errorMsg}
                        <p class="text-sm mb-3" style="color: #dc2626;">{errorMsg}</p>
                    {/if}
                    <div class="flex flex-col gap-2 mt-3">
                        <button
                            class="fqf-btn-primary"
                            onclick={handleLoadSchedule}
                            disabled={loading}
                        >
                            {loading ? 'Loading…' : 'Load Schedule'}
                        </button>
                        <button
                            class="fqf-btn-outline"
                            onclick={() => {
                                mode = 'choose';
                                errorMsg = '';
                            }}
                            disabled={loading}
                        >
                            Back
                        </button>
                    </div>
                </div>
            {/if}
        </div>
    </div>
{/if}
