<script lang="ts">
    import { FESTIVAL_DATES, DAY_LABELS } from '$lib/types';

    let { selectedDate = $bindable() }: { selectedDate: string } = $props();
</script>

<div class="flex gap-1 p-2">
    {#each FESTIVAL_DATES as d}
        <button
            class="px-6 py-2 text-lg font-semibold rounded-lg transition-colors"
            class:bg-primary-500={selectedDate === d}
            class:text-white={selectedDate === d}
            class:bg-surface-200={selectedDate !== d}
            onclick={() => (selectedDate = d)}
        >
            {DAY_LABELS[d]}
        </button>
    {/each}
</div>
