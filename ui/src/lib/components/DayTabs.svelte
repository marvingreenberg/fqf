<script lang="ts">
    import { FESTIVAL_DATES, DAY_LABELS } from '$lib/types';

    let { selectedDate = $bindable() }: { selectedDate: string } = $props();
</script>

<div
    class="flex gap-1 px-3 pt-2 pb-0"
    style="background-color: rgba(250, 246, 240, 0.95); border-bottom: 1px solid rgba(74, 26, 107, 0.12);"
>
    {#each FESTIVAL_DATES as d}
        <button
            class="fqf-day-tab {selectedDate === d ? 'fqf-day-tab-active' : ''}"
            onclick={() => (selectedDate = d)}
        >
            {DAY_LABELS[d]}
        </button>
    {/each}
</div>
