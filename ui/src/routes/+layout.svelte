<script lang="ts">
    import '../app.css';
    import TokenDialog from '$lib/components/TokenDialog.svelte';
    import { appState } from '$lib/stores.svelte';

    let { children } = $props();

    let dialogOpen = $state(false);
</script>

<div class="min-h-screen flex flex-col">
    <header class="bg-primary-500 text-white p-4 flex items-center justify-between">
        <strong class="text-xl">FQF 2026</strong>
        <div class="flex items-center gap-3">
            {#if appState.token}
                <span
                    class="hidden sm:inline-block bg-primary-700 text-white text-xs font-mono
                           px-2 py-1 rounded-full truncate max-w-40"
                    title={appState.token}
                >
                    {appState.token}
                </span>
            {/if}
            <button
                class="btn btn-sm preset-outlined-surface-50 text-white border-white/40
                       hover:bg-white/10 text-sm"
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
