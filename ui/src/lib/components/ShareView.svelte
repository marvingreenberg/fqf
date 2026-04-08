<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import { DAY_LABELS } from '$lib/types';
    import { assignEmojis } from '$lib/emoji-mapper';
    import { getWorstConflict } from '$lib/conflict';
    import { CONFLICT_COLORS, FLEUR_PATH, QUESTION_PATH, PICKED_FLEUR_FILL } from '$lib/constants';
    import { bareSlug, isPicked, isMaybe } from '$lib/picks';
    import { appState } from '$lib/stores.svelte';
    import ActRow from './ActRow.svelte';

    const BADGE_COUNT = 4;
    const SELF_LABEL = 'Self';

    interface Props {
        selfActs: ActSummary[];
        onTogglePick: (slug: string) => void;
        onToggleMaybe: (slug: string) => void;
        onActDetail: (act: ActSummary) => void;
    }

    let { selfActs, onTogglePick, onToggleMaybe, onActDetail }: Props = $props();

    interface ScheduleEntry {
        id: string; // token for self, share_id for shared
        label: string;
        picks: Set<string>;
    }

    // Build the full list of schedule entries: self first, then shared schedules
    const allEntries = $derived.by((): ScheduleEntry[] => {
        const entries: ScheduleEntry[] = [];
        if (appState.token && appState.confirmed) {
            entries.push({
                id: appState.token,
                label: appState.name || SELF_LABEL,
                picks: appState.picks
            });
        }
        for (const s of appState.sharedSchedules) {
            entries.push({ id: s.share_id, label: s.name || s.share_id, picks: new Set(s.picks) });
        }
        return entries;
    });

    // Checked state — all enabled by default. Derived from entries so it
    // never reads+writes the same state (which would cause an infinite loop).
    let manuallyUnchecked = $state<Set<string>>(new Set());

    // All entries are checked unless manually unchecked
    const checkedIds = $derived(
        new Set(allEntries.map((e) => e.id).filter((id) => !manuallyUnchecked.has(id)))
    );

    const activeEntries = $derived(allEntries.filter((e) => checkedIds.has(e.id)));

    const emojiMap = $derived(assignEmojis(allEntries.map((e) => e.id)));

    // Map slug -> list of entry ids that picked it (among active entries)
    const pickersBySlug = $derived.by(() => {
        const map = new Map<string, string[]>();
        for (const entry of activeEntries) {
            for (const rawSlug of entry.picks) {
                const slug = bareSlug(rawSlug);
                if (!map.has(slug)) map.set(slug, []);
                map.get(slug)!.push(entry.id);
            }
        }
        return map;
    });

    // Union of all picks across active entries (bare slugs for visibility filtering)
    const allPickSlugs = $derived.by(() => {
        const union = new Set<string>();
        for (const entry of activeEntries) {
            for (const rawSlug of entry.picks) union.add(bareSlug(rawSlug));
        }
        return union;
    });

    // Raw picks union preserving ?-prefixes (for conflict detection)
    const allPicksRaw = $derived.by(() => {
        const union = new Set<string>();
        for (const entry of activeEntries) {
            for (const rawSlug of entry.picks) union.add(rawSlug);
        }
        return union;
    });

    function getEntryPicks(entryId: string): Set<string> {
        if (entryId === appState.token) return appState.picks;
        const shared = appState.sharedSchedules.find((s) => s.share_id === entryId);
        return shared ? new Set(shared.picks) : new Set();
    }

    // All acts: self picks + shared schedules, deduped by slug
    const allActs = $derived.by((): ActSummary[] => {
        const bySlug = new Map<string, ActSummary>();
        for (const act of selfActs) {
            bySlug.set(act.slug, act);
        }
        for (const schedule of appState.sharedSchedules) {
            for (const act of schedule.acts) {
                bySlug.set(act.slug, act);
            }
        }
        return [...bySlug.values()].sort(
            (a, b) => a.date.localeCompare(b.date) || a.start.localeCompare(b.start)
        );
    });

    const groupedByDay = $derived.by(() => {
        const visible = allActs.filter((a) => allPickSlugs.has(a.slug));
        const byDate = new Map<string, ActSummary[]>();
        for (const act of visible) {
            if (!byDate.has(act.date)) byDate.set(act.date, []);
            byDate.get(act.date)!.push(act);
        }
        return [...byDate.entries()].map(([date, acts]) => ({ date, acts }));
    });

    function conflictColor(act: ActSummary): string {
        const level: ConflictLevel = getWorstConflict(act, allActs, allPicksRaw);
        return CONFLICT_COLORS[level];
    }

    function badgeClass(id: string): string {
        const idx = allEntries.findIndex((e) => e.id === id);
        return `fqf-merge-badge-${(idx < 0 ? 0 : idx) % BADGE_COUNT}`;
    }

    function toggleChecked(id: string): void {
        const next = new Set(manuallyUnchecked);
        if (next.has(id)) next.delete(id);
        else next.add(id);
        manuallyUnchecked = next;
    }

    // Refresh shared schedules
    let refreshing = $state(false);
    let refreshStatus = $state<string | null>(null);
    const REFRESH_STATUS_DURATION_MS = 3000;

    async function handleRefresh(): Promise<void> {
        if (appState.sharedSchedules.length === 0) return;
        refreshing = true;
        refreshStatus = null;
        try {
            const { loadSharedSchedule } = await import('$lib/api');
            const checkId = appState.ownShareId || undefined;
            let changed = false;
            const updated = await Promise.all(
                appState.sharedSchedules.map(async (s) => {
                    const resp = await loadSharedSchedule(s.share_id, checkId);
                    const picksChanged =
                        JSON.stringify(resp.picks.sort()) !== JSON.stringify([...s.picks].sort());
                    if (picksChanged) changed = true;
                    return {
                        ...s,
                        picks: resp.picks,
                        acts: resp.acts,
                        name: resp.name || s.name,
                        shared_back: resp.has_back_share ?? s.shared_back
                    };
                })
            );
            appState.sharedSchedules = updated;
            refreshStatus = changed ? 'Updated!' : 'No changes';
        } catch {
            refreshStatus = 'Refresh failed';
        } finally {
            refreshing = false;
            setTimeout(() => {
                refreshStatus = null;
            }, REFRESH_STATUS_DURATION_MS);
        }
    }

    // Share back to another user
    let sharingBackTo = $state<string | null>(null);

    async function handleShareBack(shareId: string): Promise<void> {
        if (!appState.ownShareId || !appState.name) return;
        sharingBackTo = shareId;
        try {
            const { shareBack } = await import('$lib/api');
            await shareBack(shareId, appState.ownShareId, appState.name);
            appState.sharedSchedules = appState.sharedSchedules.map((s) =>
                s.share_id === shareId ? { ...s, shared_back: true } : s
            );
        } catch {
            // Silently fail — button remains visible for retry
        } finally {
            sharingBackTo = null;
        }
    }
</script>

<div class="flex flex-col overflow-y-auto h-full">
    <!-- Person toggles -->
    {#if allEntries.length > 0}
        <div class="shrink-0 px-3 py-2 border-b fqf-filter-panel flex flex-wrap items-center gap-3">
            {#each allEntries as entry (entry.id)}
                <div class="flex items-center gap-1.5">
                    <label class="flex items-center gap-1.5 cursor-pointer select-none">
                        <input
                            type="checkbox"
                            checked={checkedIds.has(entry.id)}
                            onchange={() => toggleChecked(entry.id)}
                            class="rounded"
                            style="accent-color: var(--mg-purple);"
                        />
                        <span
                            class="fqf-emoji-circle {badgeClass(entry.id)}"
                            aria-hidden="true"
                            title={entry.id}
                        >
                            {emojiMap[entry.id] ?? '?'}
                        </span>
                        <span class="text-sm font-medium" style="color: var(--mg-purple-deep);">
                            {entry.label}
                            {#if entry.id === appState.token}
                                <span
                                    class="text-xs font-normal"
                                    style="color: rgba(74,26,107,0.5);"
                                >
                                    (you)
                                </span>
                            {/if}
                        </span>
                    </label>
                    {#if entry.id !== appState.token}
                        <button
                            class="text-xs leading-none"
                            style="color: rgba(74,26,107,0.4);"
                            title="Remove {entry.label}"
                            aria-label="Remove {entry.label}"
                            onclick={() => appState.removeSharedSchedule(entry.id)}
                        >
                            ×
                        </button>
                        {#if appState.ownShareId}
                            {@const shared = appState.sharedSchedules.find(
                                (s) => s.share_id === entry.id
                            )}
                            {#if shared && shared.shared_back !== true}
                                <button
                                    class="fqf-btn-outline text-xs py-0.5 px-1.5 leading-tight"
                                    onclick={() => handleShareBack(entry.id)}
                                    disabled={sharingBackTo === entry.id}
                                    title="Add your schedule to {entry.label}'s shares"
                                >
                                    {sharingBackTo === entry.id ? '...' : '↗'} Share back
                                </button>
                            {/if}
                        {/if}
                    {/if}
                </div>
            {/each}
            <!-- Refresh button -->
            {#if appState.sharedSchedules.length > 0}
                <button
                    class="fqf-btn-outline text-xs py-0.5 px-1.5 leading-tight"
                    onclick={handleRefresh}
                    disabled={refreshing}
                    title="Refresh shared schedules"
                >
                    {refreshing ? '⟳' : '↻'}
                </button>
                {#if refreshStatus}
                    <span
                        class="text-xs font-medium"
                        style="color: {refreshStatus === 'Updated!'
                            ? 'var(--mg-green-deep)'
                            : 'rgba(74,26,107,0.5)'};"
                    >
                        {refreshStatus}
                    </span>
                {/if}
            {/if}
        </div>
    {/if}

    <!-- Content area -->
    {#if allEntries.length === 0}
        <div
            class="flex flex-col items-center justify-center h-full gap-2"
            style="color: rgba(74, 26, 107, 0.5);"
        >
            <p class="text-lg font-medium">No shared schedules yet</p>
            <p class="text-sm">Use the share button in the avatar menu to generate a share link.</p>
        </div>
    {:else if activeEntries.length === 0 || allPickSlugs.size === 0}
        <div class="flex items-center justify-center h-full" style="color: rgba(74, 26, 107, 0.5);">
            <p>No picks to show — check at least one person above.</p>
        </div>
    {:else}
        <div class="flex-1 overflow-y-auto">
            {#each groupedByDay as group (group.date)}
                <div class="sticky top-0 z-10 fqf-group-header px-3 py-1.5">
                    <span>{DAY_LABELS[group.date] ?? group.date}</span>
                </div>

                {#each group.acts as act (act.slug)}
                    {@const pickers = pickersBySlug.get(act.slug) ?? []}
                    <ActRow
                        {act}
                        isPicked={appState.picks.has(act.slug)}
                        isMaybe={appState.isMaybe(act.slug)}
                        conflictColor={conflictColor(act)}
                        {onTogglePick}
                        {onToggleMaybe}
                        {onActDetail}
                    >
                        {#snippet extra()}
                            <div class="flex gap-0.5">
                                {#each pickers as id (id)}
                                    {@const entry = allEntries.find((e) => e.id === id)}
                                    {@const entryPicks = getEntryPicks(id)}
                                    {@const isPickedByEntry = isPicked(act.slug, entryPicks)}
                                    {@const isMaybeByEntry = isMaybe(act.slug, entryPicks)}
                                    <span
                                        class="fqf-emoji-circle {badgeClass(id)}"
                                        style="position: relative;"
                                        title={entry?.label ?? id}
                                        aria-label={entry?.label ?? id}
                                    >
                                        {emojiMap[id] ?? '?'}
                                        {#if isPickedByEntry}
                                            <span class="fqf-emoji-sub-indicator">
                                                <svg
                                                    viewBox="0 0 16 16"
                                                    width="10"
                                                    height="10"
                                                    fill={PICKED_FLEUR_FILL}
                                                >
                                                    <path d={FLEUR_PATH} />
                                                </svg>
                                            </span>
                                        {:else if isMaybeByEntry}
                                            <span class="fqf-emoji-sub-indicator">
                                                <svg
                                                    viewBox="0 0 16 16"
                                                    width="10"
                                                    height="10"
                                                    fill="#7c3aed"
                                                >
                                                    <path d={QUESTION_PATH} />
                                                </svg>
                                            </span>
                                        {/if}
                                    </span>
                                {/each}
                            </div>
                        {/snippet}
                    </ActRow>
                {/each}
            {/each}
        </div>
    {/if}
</div>
