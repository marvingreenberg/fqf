<script lang="ts">
    import type { Snippet } from 'svelte';
    import { fuzzyLookup } from '$lib/api';
    import { appState } from '$lib/stores.svelte';
    import { createNewSchedule, reverseDisplayToken } from '$lib/auth-utils';

    interface Props {
        /**
         * Called after the identity is confirmed (load or new).
         * Implement post-login side effects here (e.g. attach a share, navigate).
         */
        onConfirmed?: () => Promise<void>;
        /**
         * Optional extra content rendered in the "new schedule" section,
         * below the first descriptive line.
         */
        newSectionExtra?: Snippet;
        /**
         * Optional footer slot rendered after the error message row.
         */
        footer?: Snippet;
        /**
         * Descriptive text shown above the Load button.
         */
        loadLabel?: string;
        /**
         * Descriptive text shown above the New button.
         */
        newLabel?: string;
    }

    let {
        onConfirmed,
        newSectionExtra,
        footer,
        loadLabel = 'If you have an existing schedule, you can load it',
        newLabel = 'Create a schedule. Name for sharing, a nickname is fine'
    }: Props = $props();

    let tripleInput = $state('');
    let nameInput = $state('');
    let errorMsg = $state('');
    let loading = $state(false);

    // Pre-fill triple if a stored token exists
    $effect(() => {
        if (appState.token) tripleInput = appState.token;
    });

    async function handleLoad(): Promise<void> {
        const triple = reverseDisplayToken(tripleInput.trim());
        if (!triple) {
            errorMsg = 'Please enter your secret words.';
            return;
        }
        loading = true;
        errorMsg = '';
        try {
            const result = await fuzzyLookup(triple);
            if (result.corrected) {
                tripleInput = result.token;
            }
            await appState.confirm(result.token, result.name);
            await onConfirmed?.();
        } catch {
            errorMsg = 'Schedule not found. Check your secret words.';
        } finally {
            loading = false;
        }
    }

    async function handleNew(): Promise<void> {
        if (!nameInput.trim()) {
            errorMsg = 'Please enter a name before creating a schedule.';
            return;
        }
        loading = true;
        errorMsg = '';
        try {
            await createNewSchedule(nameInput.trim());
            await onConfirmed?.();
        } catch {
            errorMsg = 'Could not create schedule. Please try again.';
        } finally {
            loading = false;
        }
    }

    function handleTripleKeydown(e: KeyboardEvent): void {
        if (e.key === 'Enter') handleLoad();
    }

    function handleNameKeydown(e: KeyboardEvent): void {
        if (e.key === 'Enter') handleNew();
    }
</script>

<!-- Load existing schedule section -->
<div class="flex flex-col gap-2">
    <p class="text-xs" style="color: rgba(74,26,107,0.65); font-style: italic;">
        {loadLabel}
    </p>
    <button class="fqf-btn-gold w-full" onclick={handleLoad} disabled={loading}>
        {loading ? 'Loading…' : 'Load Schedule'}
    </button>
    <input
        class="input w-full text-sm"
        type="text"
        placeholder="enter your secret words"
        style={tripleInput
            ? 'color: #1a1a1a;'
            : 'color: rgba(74,26,107,0.4); font-style: italic; font-size: 0.8rem;'}
        bind:value={tripleInput}
        onkeydown={handleTripleKeydown}
    />
</div>

<hr style="border-color: rgba(74,26,107,0.15);" />

<!-- New schedule section -->
<div class="flex flex-col gap-2">
    <p class="text-xs" style="color: rgba(74,26,107,0.65); font-style: italic;">
        {newLabel}
    </p>
    {#if newSectionExtra}
        {@render newSectionExtra()}
    {/if}
    <button class="fqf-btn-gold w-full" onclick={handleNew} disabled={loading}>
        {loading ? 'Creating…' : 'New Schedule'}
    </button>
    <div class="flex items-center gap-2">
        <label
            for="login-form-name"
            class="text-sm font-semibold shrink-0"
            style="color: var(--mg-purple-deep);"
        >
            Name:
        </label>
        <input
            id="login-form-name"
            class="input flex-1 text-sm"
            type="text"
            placeholder="Fred, BooBoo, …"
            style={nameInput
                ? ''
                : 'color: rgba(74,26,107,0.4); font-style: italic; font-size: 0.8rem;'}
            bind:value={nameInput}
            onkeydown={handleNameKeydown}
        />
    </div>
</div>

{#if errorMsg}
    <p class="text-sm" style="color: #dc2626;">{errorMsg}</p>
{/if}

{#if footer}
    {@render footer()}
{/if}
