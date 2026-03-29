<script lang="ts">
    import { FESTIVAL_DATES, DAY_LABELS } from '$lib/types';

    let { selectedDate = $bindable() }: { selectedDate: string } = $props();
</script>

<div class="flex gap-1 px-3 pt-2 pb-0 fqf-day-tabs">
    {#each FESTIVAL_DATES as d}
        <button
            class="fqf-day-tab {selectedDate === d ? 'fqf-day-tab-active' : ''}"
            onclick={() => (selectedDate = d)}
        >
            {DAY_LABELS[d]}
        </button>
    {/each}
</div>
