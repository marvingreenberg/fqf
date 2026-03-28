<script lang="ts">
    import { createSchedule } from '$lib/api';
    import { appState } from '$lib/stores.svelte';

    type GateMode = 'choose' | 'enter-token' | 'creating';

    interface Props {
        onconfirmed?: () => void;
    }

    let { onconfirmed }: Props = $props();

    let mode = $state<GateMode>('choose');
    let tokenInput = $state('');
    let nameInput = $state('');
    let errorMsg = $state('');
    let loading = $state(false);

    // Pre-fill if a token was found in localStorage
    $effect(() => {
        if (appState.token) {
            tokenInput = appState.token;
            mode = 'enter-token';
        }
    });

    async function handleConfirmToken(): Promise<void> {
        const trimmed = tokenInput.trim().toLowerCase();
        if (!trimmed) {
            errorMsg = 'Please enter your fest schedule identity.';
            return;
        }
        loading = true;
        errorMsg = '';
        try {
            await appState.confirm(trimmed, nameInput.trim() || undefined);
            onconfirmed?.();
        } catch {
            errorMsg = 'Could not find that identity. Check your secret words and try again.';
        } finally {
            loading = false;
        }
    }

    async function handleCreateNew(): Promise<void> {
        loading = true;
        errorMsg = '';
        try {
            const resp = await createSchedule(nameInput.trim() || undefined);
            tokenInput = resp.token;
            await appState.confirm(resp.token, nameInput.trim() || undefined);
            onconfirmed?.();
        } finally {
            loading = false;
        }
    }

    function handleKeydown(e: KeyboardEvent): void {
        if (e.key === 'Enter') handleConfirmToken();
    }
</script>

<div
    class="fixed inset-0 z-50 flex items-center justify-center"
    style="background: rgba(26, 10, 40, 0.88);"
>
    <div class="fqf-dialog-card w-full max-w-sm mx-4">
        <!-- Festive header -->
        <div class="fqf-dialog-header text-center py-6 px-6">
            <div class="text-4xl mb-2" aria-hidden="true">⚜️</div>
            <h2 class="text-2xl mb-1">Fest Schedule</h2>
            <p class="text-sm" style="color: rgba(245, 215, 110, 0.85);">
                French Quarter Fest 2026
            </p>
        </div>

        <div class="fqf-dialog-body flex flex-col gap-3">
            <!-- Optional name field always visible -->
            <div>
                <label
                    for="identity-name"
                    class="block text-xs font-semibold mb-1"
                    style="color: var(--mg-purple-deep);"
                >
                    Display name for sharing (optional)
                </label>
                <input
                    id="identity-name"
                    class="input w-full text-sm"
                    type="text"
                    placeholder="e.g. JazzFan, MG, …"
                    bind:value={nameInput}
                />
            </div>

            {#if mode === 'choose'}
                <button class="fqf-btn-gold" onclick={handleCreateNew} disabled={loading}>
                    {loading ? 'Creating…' : 'Create new identity'}
                </button>
                <button
                    class="fqf-btn-outline"
                    onclick={() => {
                        mode = 'enter-token';
                    }}
                    disabled={loading}
                >
                    I have a fest schedule identity
                </button>
            {:else if mode === 'enter-token'}
                <div>
                    <label
                        for="identity-token"
                        class="block text-xs font-semibold mb-1"
                        style="color: var(--mg-purple-deep);"
                    >
                        Your secret words
                    </label>
                    <input
                        id="identity-token"
                        class="input w-full text-sm mb-1"
                        type="text"
                        placeholder="Your three-word identity…"
                        bind:value={tokenInput}
                        onkeydown={handleKeydown}
                    />
                </div>

                {#if errorMsg}
                    <p class="text-sm" style="color: #dc2626;">{errorMsg}</p>
                {/if}

                <button class="fqf-btn-primary" onclick={handleConfirmToken} disabled={loading}>
                    {loading ? 'Loading…' : 'Confirm identity'}
                </button>

                {#if !appState.token}
                    <!-- Only show Back if user manually chose "enter token" -->
                    <button
                        class="fqf-btn-ghost"
                        onclick={() => {
                            mode = 'choose';
                            errorMsg = '';
                        }}
                        disabled={loading}
                    >
                        Back
                    </button>
                {/if}
            {/if}

            {#if appState.pendingShareId}
                <div
                    class="mt-1 pt-3 border-t text-center"
                    style="border-color: rgba(74, 26, 107, 0.15);"
                >
                    <p class="text-xs mb-2" style="color: rgba(74, 26, 107, 0.6);">
                        A shared schedule is waiting for you.
                    </p>
                    <button
                        class="fqf-btn-ghost text-sm"
                        onclick={async () => {
                            if (!appState.pendingShareId) return;
                            const { loadSharedSchedule } = await import('$lib/api');
                            const resp = await loadSharedSchedule(appState.pendingShareId);
                            await appState.addSharedSchedule({
                                share_id: appState.pendingShareId,
                                name: appState.pendingShareName ?? resp.name,
                                picks: resp.picks,
                                acts: resp.acts
                            });
                            appState.pendingShareId = null;
                            appState.pendingShareName = null;
                            // Confirm as guest — no token required
                            appState.confirmed = true;
                            appState.viewMode = 'share';
                            onconfirmed?.();
                        }}
                    >
                        View shared schedule only (no login)
                    </button>
                </div>
            {/if}
        </div>
    </div>
</div>
