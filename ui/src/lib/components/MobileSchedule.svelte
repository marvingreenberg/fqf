<script lang="ts">
    import type { ActSummary, ConflictLevel, MobileSortMode } from '$lib/types';
    import { CONFLICT_COLORS, MINUTES_PER_HOUR } from '$lib/constants';
    import { getWorstConflict, timeToMinutes } from '$lib/conflict';
    import ActRow from './ActRow.svelte';

    interface Props {
        acts: ActSummary[];
        picks: Set<string>;
        maybes: Set<string>;
        sortMode: MobileSortMode;
        onTogglePick: (slug: string) => void;
        onToggleMaybe: (slug: string) => void;
        onActDetail: (act: ActSummary) => void;
        readOnly?: boolean;
    }

    let {
        acts,
        picks,
        maybes,
        sortMode,
        onTogglePick,
        onToggleMaybe,
        onActDetail,
        readOnly = false
    }: Props = $props();

    const SLOT_INTERVAL_MINUTES = 30;

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

    const UNPICKED_BORDER_COLOR = 'transparent';

    function conflictColor(act: ActSummary): string {
        if (!picks.has(act.slug)) return UNPICKED_BORDER_COLOR;
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
            <ActRow
                {act}
                isPicked={picks.has(act.slug)}
                isMaybe={maybes.has(act.slug)}
                conflictColor={conflictColor(act)}
                {readOnly}
                {onTogglePick}
                {onToggleMaybe}
                {onActDetail}
            />
        {/each}
    {/each}
</div>
