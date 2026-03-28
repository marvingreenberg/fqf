<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { appState } from '$lib/stores.svelte';
    import AvatarMenu from '$lib/components/AvatarMenu.svelte';
    import IdentityGate from '$lib/components/IdentityGate.svelte';

    let { children } = $props();

    let gateVisible = $state(true);

    onMount(async () => {
        // Load saved identity from localStorage
        appState.loadFromStorage();

        // Capture share query params before potentially hiding the gate
        const shareId = $page.url.searchParams.get('share');
        const shareName = $page.url.searchParams.get('name');
        if (shareId) {
            appState.pendingShareId = shareId;
            appState.pendingShareName = shareName;
        }

        // If a token was found in storage, auto-confirm so the gate never shows
        if (appState.token) {
            try {
                await appState.confirm(appState.token);
                gateVisible = false;
            } catch {
                // Token no longer valid — clear stale identity so gate shows clean
                appState.clearIdentity();
            }
            return;
        }

        // If already confirmed this session (e.g. guest view), skip gate
        if (appState.confirmed) {
            gateVisible = false;
        }
    });

    function handleConfirmed(): void {
        gateVisible = false;
    }
</script>

<div class="min-h-screen flex flex-col">
    <header class="fqf-header shrink-0 px-4 py-3 flex items-center justify-between">
        <div class="flex flex-col">
            <a href="/" style="text-decoration: none;">
                <span class="fqf-header-title">FQF 2026</span>
            </a>
            <span class="fqf-header-subtitle">Schedule Builder</span>
        </div>
        <div class="flex items-center gap-3">
            {#if appState.confirmed && appState.token}
                <AvatarMenu />
            {:else if appState.confirmed}
                <!-- Guest viewing a shared schedule -->
                <span class="text-xs" style="color: rgba(245,215,110,0.7);">Guest view</span>
            {/if}
        </div>
    </header>

    <main class="flex-1 overflow-hidden flex flex-col">
        {@render children()}
    </main>
</div>

{#if gateVisible}
    <IdentityGate onconfirmed={handleConfirmed} />
{/if}
