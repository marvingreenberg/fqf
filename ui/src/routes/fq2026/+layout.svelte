<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { appState } from '$lib/stores.svelte';
    import { initNetworkWatcher } from '$lib/network';
    import AvatarMenu from '$lib/components/AvatarMenu.svelte';
    import IdentityGate from '$lib/components/IdentityGate.svelte';
    import HelpPanel from '$lib/components/HelpPanel.svelte';

    let { children } = $props();

    // Suppress the gate during initial async auto-confirm to prevent flash
    let initializing = $state(true);

    // Help panel — hoisted from ScheduleShell so the (i) button can live in
    // the top header next to the FQF 2026 brand.
    let showHelp = $state(false);

    // Detect view-only share route — no identity gate needed
    const isViewOnlyRoute = $derived(
        $page.url.pathname !== '/fq2026' && $page.url.pathname !== '/fq2026/'
    );

    // Gate shows when: not confirmed AND not initializing AND not on a view-only share route
    const gateVisible = $derived(!appState.confirmed && !initializing && !isViewOnlyRoute);

    onMount(async () => {
        appState.loadFromStorage();

        // Start watching network status; clean up on component destroy.
        const cleanupNetwork = initNetworkWatcher(appState);

        const shareId = $page.url.searchParams.get('share');
        const shareName = $page.url.searchParams.get('name');
        if (shareId) {
            appState.pendingShareId = shareId;
            appState.pendingShareName = shareName;
        }

        if (appState.token) {
            // confirm() now handles the offline case internally (falls back to
            // localStorage picks) so we never need to clearIdentity here.
            await appState.confirm(appState.token);
        }
        initializing = false;

        // If a share link was opened and the user is still not confirmed, redirect to
        // the view-only route so ShareLoginPane can handle the context-specific login flow.
        if (appState.pendingShareId && !appState.confirmed) {
            goto(`/fq2026/${appState.pendingShareId}`);
        }

        return cleanupNetwork;
    });
</script>

{#if isViewOnlyRoute}
    <!-- View-only share route — child layout handles its own header -->
    {@render children()}
{:else}
    <div class="min-h-screen flex flex-col">
        <header class="fqf-header shrink-0 px-4 py-3 flex items-center justify-between">
            <div class="flex items-center gap-3 min-w-0">
                <a href="/" style="text-decoration: none;" class="flex flex-col min-w-0">
                    <span class="fqf-header-title">FQF 2026</span>
                    <span class="fqf-header-subtitle">Schedule Builder</span>
                </a>
                <button
                    class="fqf-help-button shrink-0 flex items-center justify-center"
                    onclick={() => (showHelp = true)}
                    aria-label="About this app"
                    title="About this app"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2.25"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        aria-hidden="true"
                    >
                        <circle cx="12" cy="12" r="10" />
                        <line x1="12" y1="16" x2="12" y2="12" />
                        <line x1="12" y1="8" x2="12.01" y2="8" />
                    </svg>
                </button>
            </div>
            <div class="flex items-center gap-3">
                <!-- Network / save status indicators -->
                <div class="flex items-center gap-1.5">
                    {#if !appState.isOnline}
                        <!-- Crossed-out wifi icon shown when offline -->
                        <span
                            title="Offline — changes will sync when you reconnect"
                            class="flex items-center"
                            style="color: var(--mg-gold-bright);"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="16"
                                height="16"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                aria-hidden="true"
                            >
                                <!-- Wifi arcs -->
                                <path d="M5 12.55a11 11 0 0 1 14.08 0" />
                                <path d="M1.42 9a16 16 0 0 1 21.16 0" />
                                <path d="M8.53 16.11a6 6 0 0 1 6.95 0" />
                                <circle cx="12" cy="20" r="1" fill="currentColor" />
                                <!-- Slash line -->
                                <line x1="1" y1="1" x2="23" y2="23" />
                            </svg>
                        </span>
                    {/if}
                    {#if appState.saveError}
                        <!-- Warning icon when last save failed -->
                        <span
                            title="Changes not saved — will retry when back online"
                            class="flex items-center"
                            style="color: var(--mg-gold-bright); opacity: 0.8;"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="14"
                                height="14"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2.5"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                aria-hidden="true"
                            >
                                <path
                                    d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                                />
                                <line x1="12" y1="9" x2="12" y2="13" />
                                <line x1="12" y1="17" x2="12.01" y2="17" />
                            </svg>
                        </span>
                    {:else if appState.savedFlash}
                        <!-- Brief "Saved" confirmation after recovering from an error -->
                        <span class="text-xs" style="color: rgba(245,215,110,0.8);">Saved</span>
                    {/if}
                </div>
                {#if appState.confirmed && appState.token}
                    <AvatarMenu />
                {:else if appState.confirmed}
                    <span class="text-xs" style="color: rgba(245,215,110,0.7);">Guest view</span>
                {/if}
            </div>
        </header>

        <main class="flex-1 overflow-hidden flex flex-col">
            {@render children()}
        </main>
    </div>
{/if}

{#if gateVisible}
    <IdentityGate
        pendingShareId={appState.pendingShareId}
        pendingShareName={appState.pendingShareName}
    />
{/if}

{#if showHelp}
    <HelpPanel onClose={() => (showHelp = false)} />
{/if}
