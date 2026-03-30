<script lang="ts">
    import { onMount } from 'svelte';
    import { createSchedule, fuzzyLookup, loadSharedSchedule } from '$lib/api';
    import { getFingerprint } from '$lib/fingerprint';
    import { appState } from '$lib/stores.svelte';
    import { FINGERPRINT_COUNTER_KEY } from '$lib/types';

    interface Props {
        pendingShareId?: string | null;
        pendingShareName?: string | null;
    }

    let { pendingShareId = null, pendingShareName = null }: Props = $props();

    // null = not yet checked (pending), true/false = resolved after mount
    // Start as null only when there is a share to validate, otherwise false (no share)
    let shareValid = $state<boolean | null>(null);
    let shareValidName = $state<string>('');

    let nameInput = $state('');
    let tripleInput = $state('');
    let errorMsg = $state('');
    let shareError = $state('');
    let loading = $state(false);

    // Pre-fill triple if a stored token exists (e.g. after page load with stored identity)
    $effect(() => {
        if (appState.token) tripleInput = appState.token;
    });

    onMount(async () => {
        if (!pendingShareId) {
            shareValid = false;
            return;
        }
        try {
            const resp = await loadSharedSchedule(pendingShareId);
            shareValidName = pendingShareName ?? resp.name;
            shareValid = true;
        } catch {
            shareValid = false;
            shareError = '(!) Share not found';
        }
    });

    async function handleNewSchedule(): Promise<void> {
        if (!nameInput.trim()) {
            errorMsg = 'Please enter a name before creating a schedule.';
            return;
        }
        loading = true;
        errorMsg = '';
        try {
            const fingerprintHash = await getFingerprint();
            const rawCounter = localStorage.getItem(FINGERPRINT_COUNTER_KEY);
            const counter = rawCounter !== null ? parseInt(rawCounter, 10) || 0 : 0;

            const resp =
                fingerprintHash !== null
                    ? await createSchedule(nameInput.trim(), fingerprintHash, counter)
                    : await createSchedule(nameInput.trim());

            const nextCounter = counter + 1;
            localStorage.setItem(FINGERPRINT_COUNTER_KEY, String(nextCounter));
            await appState.confirm(resp.token, nameInput.trim(), nextCounter);
        } catch {
            errorMsg = 'Could not create schedule. Please try again.';
        } finally {
            loading = false;
        }
    }

    async function handleLoadSchedule(): Promise<void> {
        const triple = tripleInput.trim();
        if (!triple) {
            errorMsg = 'Please enter your secret words.';
            return;
        }
        loading = true;
        errorMsg = '';
        try {
            const result = await fuzzyLookup(triple);
            if (result.corrected) {
                // Auto-fill the corrected triple so the user sees what was matched
                tripleInput = result.token;
            }
            // Name comes from the stored schedule — no input required for load
            await appState.confirm(result.token, result.name);
        } catch {
            errorMsg = 'Schedule not found. Check your secret words.';
        } finally {
            loading = false;
        }
    }

    function handleViewShareOnly(): void {
        if (!pendingShareId) return;
        // Navigate to view-only route (Task 28)
        window.location.href = `/fq2026/${pendingShareId}`;
    }

    function handleKeydown(e: KeyboardEvent): void {
        if (e.key === 'Enter') handleLoadSchedule();
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

        <div class="fqf-dialog-body flex flex-col gap-4">
            <!-- Share-not-found banner -->
            {#if shareValid === false && shareError}
                <p class="text-sm font-medium" style="color: #c05000; font-style: italic;">
                    {shareError}
                </p>
            {/if}

            <!-- Load existing schedule section -->
            <div class="flex flex-col gap-2">
                <p class="text-xs" style="color: rgba(74,26,107,0.65); font-style: italic;">
                    If you have an existing schedule, you can load it
                </p>
                <button class="fqf-btn-gold w-full" onclick={handleLoadSchedule} disabled={loading}>
                    {loading ? 'Loading…' : 'Load Schedule'}
                </button>
                <input
                    id="identity-triple"
                    class="input w-full text-sm"
                    type="text"
                    placeholder="enter your secret words"
                    style="{tripleInput ? 'color: #1a1a1a;' : 'color: rgba(74,26,107,0.4); font-style: italic; font-size: 0.8rem;'}"
                    bind:value={tripleInput}
                    onkeydown={handleKeydown}
                />
            </div>

            <!-- Divider -->
            <hr style="border-color: rgba(74,26,107,0.15);" />

            <!-- New schedule section -->
            <div class="flex flex-col gap-2">
                <p class="text-xs" style="color: rgba(74,26,107,0.65); font-style: italic;">
                    Create a schedule. Name for sharing, a nickname is fine
                </p>
                {#if shareValid === true}
                    <p class="text-xs" style="color: rgba(74,26,107,0.6); font-style: italic;">
                        Create a schedule to allow comparing with {shareValidName}
                    </p>
                {/if}
                <button class="fqf-btn-gold w-full" onclick={handleNewSchedule} disabled={loading}>
                    {loading ? 'Creating…' : 'New Schedule'}
                </button>
                <div class="flex items-center gap-2">
                    <label
                        for="identity-name"
                        class="text-sm font-semibold shrink-0"
                        style="color: var(--mg-purple-deep);"
                    >
                        Name:
                    </label>
                    <input
                        id="identity-name"
                        class="input flex-1 text-sm"
                        type="text"
                        placeholder="Fred, BooBoo, …"
                        style={nameInput ? '' : 'color: rgba(74,26,107,0.4); font-style: italic; font-size: 0.8rem;'}
                        bind:value={nameInput}
                    />
                </div>
            </div>

            {#if errorMsg}
                <p class="text-sm" style="color: #dc2626;">{errorMsg}</p>
            {/if}

            <!-- View-only share option -->
            {#if pendingShareId && shareValid === true}
                <button class="fqf-btn-ghost" onclick={handleViewShareOnly} disabled={loading}>
                    View {shareValidName}'s schedule?
                    <span
                        class="block text-xs"
                        style="color: rgba(74,26,107,0.5); font-style: italic;"
                    >
                        view only, no changes can be made
                    </span>
                </button>
            {/if}
        </div>
    </div>
</div>
