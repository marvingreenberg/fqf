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
        <div class="sticky top-0 z-10 bg-surface-200 px-3 py-1.5 border-b border-surface-300">
            <span class="text-xs font-bold uppercase tracking-wider text-surface-600">
                {group.header}
            </span>
        </div>

        {#each group.acts as act (act.slug)}
            <!-- svelte-ignore a11y_no_static_element_interactions -->
            <!-- svelte-ignore a11y_click_events_have_key_events -->
            <div
                class="flex items-center gap-3 px-3 py-2.5 border-b border-surface-200
                       hover:bg-surface-100 transition-colors border-l-4"
                style="border-left-color: {conflictColor(act)};"
                onclick={() => onActDetail(act)}
            >
                <button
                    class="shrink-0 w-5 h-5 rounded border border-surface-400 bg-surface-50
                           flex items-center justify-center hover:bg-primary-100 transition-colors"
                    onclick={(e) => {
                        e.stopPropagation();
                        onTogglePick(act.slug);
                    }}
                    aria-label={picks.has(act.slug)
                        ? `Remove ${act.name} from picks`
                        : `Add ${act.name} to picks`}
                >
                    {#if picks.has(act.slug)}
                        <svg class="w-3 h-3 text-primary-600" viewBox="0 0 12 12" fill="none">
                            <path
                                d="M10 3L5 8.5 2 5.5"
                                stroke="currentColor"
                                stroke-width="1.5"
                                stroke-linecap="round"
                            />
                        </svg>
                    {/if}
                </button>

                <div class="flex-1 min-w-0">
                    <p class="text-sm font-semibold truncate">{act.name}</p>
                    <p class="text-xs text-surface-500 truncate">
                        {act.stage} &middot; {act.start}–{act.end}
                    </p>
                </div>

                <span class="shrink-0 text-xs text-surface-400 italic">{act.genre}</span>
            </div>
        {/each}
    {/each}
</div>
