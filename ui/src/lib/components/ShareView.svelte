<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import { DAY_LABELS } from '$lib/types';
    import { assignEmojis } from '$lib/emoji-mapper';
    import { getWorstConflict } from '$lib/conflict';
    import { CONFLICT_COLORS } from '$lib/constants';
    import { appState } from '$lib/stores.svelte';

    const BADGE_COUNT = 4;
    const SELF_LABEL = 'Self';

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

    // Checked state — all enabled by default
    let checkedIds = $state<Set<string>>(new Set());

    $effect(() => {
        // When entries change, ensure all new entries are checked
        const next = new Set(checkedIds);
        for (const e of allEntries) {
            next.add(e.id);
        }
        checkedIds = next;
    });

    const activeEntries = $derived(allEntries.filter((e) => checkedIds.has(e.id)));

    const emojiMap = $derived(assignEmojis(allEntries.map((e) => e.id)));

    // Map slug -> list of entry ids that picked it (among active entries)
    const pickersBySlug = $derived.by(() => {
        const map = new Map<string, string[]>();
        for (const entry of activeEntries) {
            for (const slug of entry.picks) {
                if (!map.has(slug)) map.set(slug, []);
                map.get(slug)!.push(entry.id);
            }
        }
        return map;
    });

    // Union of all picks across active entries
    const allPickSlugs = $derived.by(() => {
        const union = new Set<string>();
        for (const entry of activeEntries) {
            for (const slug of entry.picks) union.add(slug);
        }
        return union;
    });

    // All acts from all shared schedules (union, deduped by slug)
    const allActs = $derived.by((): ActSummary[] => {
        const bySlug = new Map<string, ActSummary>();
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
        const level: ConflictLevel = getWorstConflict(act, allActs, allPickSlugs);
        return CONFLICT_COLORS[level];
    }

    function badgeClass(id: string): string {
        const idx = allEntries.findIndex((e) => e.id === id);
        return `fqf-merge-badge-${(idx < 0 ? 0 : idx) % BADGE_COUNT}`;
    }

    function toggleChecked(id: string): void {
        const next = new Set(checkedIds);
        if (next.has(id)) next.delete(id);
        else next.add(id);
        checkedIds = next;
    }
</script>

<div class="flex flex-col overflow-y-auto h-full">
    <!-- Person toggles -->
    {#if allEntries.length > 0}
        <div class="shrink-0 px-3 py-2 border-b fqf-filter-panel flex flex-wrap items-center gap-3">
            {#each allEntries as entry (entry.id)}
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
                            <span class="text-xs font-normal" style="color: rgba(74,26,107,0.5);">
                                (you)
                            </span>
                        {/if}
                    </span>
                </label>
            {/each}
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
                    <div
                        class="fqf-list-row flex items-center gap-3 px-3 py-2.5 border-l-4"
                        style="border-left-color: {conflictColor(act)};"
                    >
                        <div class="flex-1 min-w-0">
                            <p class="text-sm font-semibold truncate">{act.name}</p>
                            <p class="text-xs truncate" style="color: rgba(74, 26, 107, 0.5);">
                                {act.stage} &middot; {act.start}–{act.end}
                            </p>
                        </div>

                        <div class="shrink-0 flex items-center gap-1.5">
                            <div class="flex gap-0.5">
                                {#each pickers as id (id)}
                                    {@const entry = allEntries.find((e) => e.id === id)}
                                    <span
                                        class="fqf-emoji-circle {badgeClass(id)}"
                                        title={entry?.label ?? id}
                                        aria-label={entry?.label ?? id}
                                    >
                                        {emojiMap[id] ?? '?'}
                                    </span>
                                {/each}
                            </div>
                            <span class="text-xs italic" style="color: rgba(74, 26, 107, 0.45);">
                                {act.genre}
                            </span>
                        </div>
                    </div>
                {/each}
            {/each}
        </div>
    {/if}
</div>
