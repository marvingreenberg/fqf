<script lang="ts">
    import type { ActSummary, ConflictLevel } from '$lib/types';
    import { DAY_LABELS } from '$lib/types';
    import { assignEmojis } from '$lib/emoji-mapper';
    import { getWorstConflict } from '$lib/conflict';
    import { CONFLICT_COLORS } from '$lib/constants';
    import { appState } from '$lib/stores.svelte';

    const BADGE_COUNT = 4;
    const SELF_LABEL = 'Self';

    interface Props {
        selfActs: ActSummary[];
        onTogglePick: (slug: string) => void;
        onActDetail: (act: ActSummary) => void;
    }

    let { selfActs, onTogglePick, onActDetail }: Props = $props();

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
        const level: ConflictLevel = getWorstConflict(act, allActs, allPickSlugs);
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
                    {/if}
                </div>
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
                    {@const isSelfPicked = appState.picks.has(act.slug)}
                    <!-- svelte-ignore a11y_no_static_element_interactions -->
                    <!-- svelte-ignore a11y_click_events_have_key_events -->
                    <div
                        class="fqf-list-row flex items-center gap-3 px-3 py-2.5 border-l-4"
                        style="border-left-color: {conflictColor(act)};"
                        onclick={() => onActDetail(act)}
                    >
                        <button
                            class="fqf-fleur shrink-0"
                            style="width: 1.25rem; height: 1.25rem;"
                            onclick={(e) => {
                                e.stopPropagation();
                                onTogglePick(act.slug);
                            }}
                            aria-label={isSelfPicked
                                ? `Remove ${act.name} from picks`
                                : `Add ${act.name} to picks`}
                        >
                            {#if isSelfPicked}
                                <svg
                                    viewBox="0 0 16 16"
                                    width="18"
                                    height="18"
                                    fill="var(--mg-gold-rich)"
                                >
                                    <path
                                        d="M8 0C8 0 6.5 3.5 6.5 5.5C6.5 7 7 8 8 9C9 8 9.5 7 9.5 5.5C9.5 3.5 8 0 8 0ZM4.5 6C2.5 6 0 7.5 0 7.5C0 7.5 2 9 4.5 9C5.5 9 6.5 8.5 7 8C6 7.5 5.5 7 4.5 6ZM11.5 6C10.5 7 10 7.5 9 8C9.5 8.5 10.5 9 11.5 9C14 9 16 7.5 16 7.5C16 7.5 13.5 6 11.5 6ZM8 10C7 10 5 10.5 5 12C5 14 8 16 8 16C8 16 11 14 11 12C11 10.5 9 10 8 10Z"
                                    />
                                </svg>
                            {:else}
                                <svg
                                    viewBox="0 0 16 16"
                                    width="18"
                                    height="18"
                                    fill="none"
                                    stroke="rgba(74, 26, 107, 0.3)"
                                    stroke-width="0.75"
                                >
                                    <path
                                        d="M8 0C8 0 6.5 3.5 6.5 5.5C6.5 7 7 8 8 9C9 8 9.5 7 9.5 5.5C9.5 3.5 8 0 8 0ZM4.5 6C2.5 6 0 7.5 0 7.5C0 7.5 2 9 4.5 9C5.5 9 6.5 8.5 7 8C6 7.5 5.5 7 4.5 6ZM11.5 6C10.5 7 10 7.5 9 8C9.5 8.5 10.5 9 11.5 9C14 9 16 7.5 16 7.5C16 7.5 13.5 6 11.5 6ZM8 10C7 10 5 10.5 5 12C5 14 8 16 8 16C8 16 11 14 11 12C11 10.5 9 10 8 10Z"
                                    />
                                </svg>
                            {/if}
                        </button>

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
