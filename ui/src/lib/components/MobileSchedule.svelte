<script lang="ts">
    import type { ActSummary, ConflictLevel, MobileSortMode } from '$lib/types';
    import { CONFLICT_COLORS } from '$lib/constants';
    import { getWorstConflict } from '$lib/conflict';

    interface Props {
        acts: ActSummary[];
        picks: Set<string>;
        sortMode: MobileSortMode;
        onTogglePick: (slug: string) => void;
        onActDetail: (act: ActSummary) => void;
    }

    let { acts, picks, sortMode, onTogglePick, onActDetail }: Props = $props();

    const SLOT_INTERVAL_MINUTES = 30;
    const MINUTES_PER_HOUR = 60;

    function timeToMinutes(time: string): number {
        const [h, m] = time.split(':').map(Number);
        return h * MINUTES_PER_HOUR + m;
    }

    function slotLabel(slotMinutes: number): string {
        const h = Math.floor(slotMinutes / MINUTES_PER_HOUR);
        const m = slotMinutes % MINUTES_PER_HOUR;
        const suffix = h >= 12 ? 'pm' : 'am';
        const displayH = h > 12 ? h - 12 : h === 0 ? 12 : h;
        return m === 0
            ? `${displayH}${suffix}`
            : `${displayH}:${String(m).padStart(2, '0')}${suffix}`;
    }

    // Groups: [{header, acts[]}]
    const groups = $derived.by(() => {
        if (sortMode === 'by-stage') {
            const order: string[] = [];
            const byStage = new Map<string, ActSummary[]>();
            for (const act of acts) {
                if (!byStage.has(act.stage)) {
                    order.push(act.stage);
                    byStage.set(act.stage, []);
                }
                byStage.get(act.stage)!.push(act);
            }
            return order.map((stage) => ({ header: stage, acts: byStage.get(stage)! }));
        }

        // by-time: bucket acts into 30-minute slots by start time
        const bySlot = new Map<number, ActSummary[]>();
        for (const act of acts) {
            const startMin = timeToMinutes(act.start);
            const slot = Math.floor(startMin / SLOT_INTERVAL_MINUTES) * SLOT_INTERVAL_MINUTES;
            if (!bySlot.has(slot)) bySlot.set(slot, []);
            bySlot.get(slot)!.push(act);
        }
        const slots = [...bySlot.keys()].sort((a, b) => a - b);
        return slots.map((slot) => ({ header: slotLabel(slot), acts: bySlot.get(slot)! }));
    });

    function conflictColor(act: ActSummary): string {
        if (!picks.has(act.slug)) return CONFLICT_COLORS.none;
        const level: ConflictLevel = getWorstConflict(act, acts, picks);
        return CONFLICT_COLORS[level];
    }
</script>

<div class="flex flex-col overflow-y-auto h-full">
    {#each groups as group (group.header)}
        <div class="sticky top-0 z-10 fqf-group-header px-3 py-1.5">
            <span>{group.header}</span>
        </div>

        {#each group.acts as act (act.slug)}
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
                    aria-label={picks.has(act.slug)
                        ? `Remove ${act.name} from picks`
                        : `Add ${act.name} to picks`}
                >
                    {#if picks.has(act.slug)}
                        <svg viewBox="0 0 16 16" width="18" height="18" fill="var(--mg-gold-rich)">
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

                <span class="shrink-0 text-xs italic" style="color: rgba(74, 26, 107, 0.45);">
                    {act.genre}
                </span>
            </div>
        {/each}
    {/each}
</div>
