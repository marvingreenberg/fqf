<script lang="ts">
    import '../app.css';
    import TokenDialog from '$lib/components/TokenDialog.svelte';
    import { appState } from '$lib/stores.svelte';

    let { children } = $props();

    let dialogOpen = $state(false);
</script>

<div class="min-h-screen flex flex-col">
    <header class="fqf-header shrink-0 px-4 py-3 flex items-center justify-between">
        <div class="flex flex-col">
            <span class="fqf-header-title">FQF 2026</span>
            <span class="fqf-header-subtitle">Schedule Builder</span>
        </div>
        <div class="flex items-center gap-3">
            {#if appState.token}
                <span class="fqf-token-display hidden sm:inline-block" title={appState.token}>
                    {appState.token}
                </span>
            {/if}
            <button
                class="fqf-btn-switch"
                onclick={() => {
                    dialogOpen = true;
                }}
            >
                {appState.token ? 'Switch' : 'My Schedule'}
            </button>
        </div>
    </header>
    <main class="flex-1">
        {@render children()}
    </main>
</div>

<TokenDialog bind:open={dialogOpen} />
