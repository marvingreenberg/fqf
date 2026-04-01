<script lang="ts">
    import type { ActSummary, ViewMode } from '$lib/types';
    import { loadSharedSchedule } from '$lib/api';
    import { appState } from '$lib/stores.svelte';
    import FilterPanel from '$lib/components/FilterPanel.svelte';
    import ShareView from '$lib/components/ShareView.svelte';
    import ScheduleShell from '$lib/components/ScheduleShell.svelte';

    const VIEW_TABS: { value: ViewMode; label: () => string }[] = [
        { value: 'all-acts', label: () => 'All Acts' },
        { value: 'map', label: () => 'Map' },
        { value: 'my-schedule', label: () => `My Schedule (${appState.picks.size})` },
        { value: 'share', label: () => `Share (${appState.sharedSchedules.length})` }
    ];

    const LOAD_ALL_FOR_MODES: ViewMode[] = ['my-schedule', 'share', 'map'];

    // Per-day acts, synced from the shell — used for FilterPanel genre/stage dropdowns
    let dayActs = $state<ActSummary[]>([]);

    const uniqueGenres = $derived([...new Set(dayActs.map((a) => a.genre))].sort());
    const uniqueStages = $derived([...new Set(dayActs.map((a) => a.stage))]);

    async function loadPendingShare(shareId: string, shareName: string | null): Promise<void> {
        if (appState.ownShareId && shareId === appState.ownShareId) {
            appState.setViewMode('my-schedule');
            return;
        }
        try {
            const resp = await loadSharedSchedule(shareId);
            await appState.addSharedSchedule({
                share_id: shareId,
                name: shareName ?? resp.name,
                picks: resp.picks,
                acts: resp.acts
            });
            appState.setViewMode('share');
        } catch {
            // Share not found — silently ignore
        }
    }

    // Load pending share once confirmed — capture and clear to prevent re-entry
    $effect(() => {
        const confirmed = appState.confirmed;
        const shareId = appState.pendingShareId;
        const shareName = appState.pendingShareName;
        if (confirmed && shareId) {
            appState.pendingShareId = null;
            appState.pendingShareName = null;
            loadPendingShare(shareId, shareName);
        }
    });
</script>

<ScheduleShell
    bind:viewMode={appState.viewMode}
    bind:selectedDate={appState.selectedDate}
    bind:mobileSortMode={appState.mobileSortMode}
    picks={appState.picks}
    maybes={appState.maybes}
    readOnly={false}
    title="FQF 2026 Schedule Builder"
    viewTabs={VIEW_TABS}
    loadAllForModes={LOAD_ALL_FOR_MODES}
    actFilter={(a) => appState.isActVisible(a)}
    onTogglePick={(slug) => appState.togglePick(slug)}
    onToggleMaybe={(slug) => appState.toggleMaybe(slug)}
    onDayActsLoaded={(acts) => (dayActs = acts)}
>
    {#snippet filterPanel()}
        <FilterPanel genres={uniqueGenres} stages={uniqueStages} />
    {/snippet}

    {#snippet extraView({ allActs })}
        <ShareView
            selfActs={allActs}
            onTogglePick={(slug) => appState.togglePick(slug)}
            onToggleMaybe={(slug) => appState.toggleMaybe(slug)}
        />
    {/snippet}
</ScheduleShell>
