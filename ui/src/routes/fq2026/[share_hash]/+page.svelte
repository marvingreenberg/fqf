<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import type { MobileSortMode, ViewMode } from '$lib/types';
    import { FESTIVAL_DATES } from '$lib/types';
    import { loadSharedSchedule } from '$lib/api';
    import ShareLoginPane from '$lib/components/ShareLoginPane.svelte';
    import ScheduleShell from '$lib/components/ScheduleShell.svelte';

    type SharedViewMode = Exclude<ViewMode, 'share'>;

    const VIEW_TABS: { value: SharedViewMode; label: () => string }[] = [
        { value: 'all-acts', label: () => 'All Acts' },
        { value: 'map', label: () => 'Map' },
        { value: 'my-schedule', label: () => `Their Schedule (${picks.size})` }
    ];

    const LOAD_ALL_FOR_MODES: SharedViewMode[] = ['my-schedule', 'map'];

    let sharedLoading = $state(true);
    let sharedError = $state<string | null>(null);
    let ownerName = $state('');
    let showLoginPane = $state(true);
    let picks = $state<Set<string>>(new Set());
    let selectedDate = $state<string>(FESTIVAL_DATES[0]);
    let viewMode = $state<SharedViewMode>('all-acts');
    let mobileSortMode = $state<MobileSortMode>('by-time');

    onMount(async () => {
        const shareHash = $page.params.share_hash;
        try {
            const resp = await loadSharedSchedule(shareHash);
            ownerName = resp.name;
            picks = new Set(resp.picks);
        } catch {
            sharedError = 'Schedule not found. The link may be invalid or expired.';
        } finally {
            sharedLoading = false;
        }
    });
</script>

{#if sharedLoading}
    <div class="flex items-center justify-center h-full flex-1">
        <p style="color: var(--mg-purple); opacity: 0.6;">Loading shared schedule…</p>
    </div>
{:else if sharedError}
    <div class="flex flex-col items-center justify-center h-full flex-1 gap-4">
        <p class="text-lg font-medium" style="color: var(--mg-purple-deep);">{sharedError}</p>
        <a href="/fq2026" class="text-sm underline" style="color: var(--mg-purple);">
            Go to my schedule
        </a>
    </div>
{:else if showLoginPane}
    <!-- Context-specific login pane — shown until the user dismisses via "See" -->
    <div
        class="fixed inset-0 z-50 flex items-center justify-center"
        style="background: rgba(26, 10, 40, 0.88);"
    >
        <ShareLoginPane
            shareName={ownerName}
            shareHash={$page.params.share_hash}
            ondismiss={() => (showLoginPane = false)}
        />
    </div>
{:else}
    <ScheduleShell
        bind:viewMode
        bind:selectedDate
        bind:mobileSortMode
        {picks}
        maybes={new Set()}
        readOnly={true}
        viewTabs={VIEW_TABS}
        loadAllForModes={LOAD_ALL_FOR_MODES}
    />
{/if}
