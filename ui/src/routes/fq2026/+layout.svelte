<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { appState } from '$lib/stores.svelte';
    import AvatarMenu from '$lib/components/AvatarMenu.svelte';
    import IdentityGate from '$lib/components/IdentityGate.svelte';

    let { children } = $props();

    // Gate is visible whenever the user is not confirmed — reacts automatically
    // when clearIdentity() sets confirmed = false (e.g. logout from avatar menu).
    const gateVisible = $derived(!appState.confirmed);

    onMount(async () => {
        appState.loadFromStorage();

        const shareId = $page.url.searchParams.get('share');
        const shareName = $page.url.searchParams.get('name');
        if (shareId) {
            appState.pendingShareId = shareId;
            appState.pendingShareName = shareName;
        }

        if (appState.token) {
            try {
                await appState.confirm(appState.token);
            } catch {
                // Token no longer valid — clear stale identity so gate shows clean
                appState.clearIdentity();
            }
        }
    });
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
    <IdentityGate
        pendingShareId={appState.pendingShareId}
        pendingShareName={appState.pendingShareName}
    />
{/if}
