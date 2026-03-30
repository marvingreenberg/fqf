<script lang="ts">
    import { goto } from '$app/navigation';

    const MAIN_ROUTE = '/fq2026';

    let { children }: { children: import('svelte').Snippet } = $props();
</script>

<div class="min-h-screen flex flex-col">
    <header class="fqf-header shrink-0 px-4 py-3 flex items-center justify-between">
        <div class="flex flex-col">
            <a href="/" style="text-decoration: none;">
                <span class="fqf-header-title">FQF 2026</span>
            </a>
            <span class="fqf-header-subtitle">Shared Schedule</span>
        </div>
        <div class="flex items-center gap-3">
            <button
                class="text-xs underline"
                style="color: rgba(245,215,110,0.8);"
                onclick={() => goto(MAIN_ROUTE)}
            >
                ← Back to my schedule
            </button>
        </div>
    </header>

    <main class="flex-1 overflow-hidden flex flex-col">
        {@render children()}
    </main>
</div>
