<script lang="ts">
    import type { ActSummary, ConflictLevel, MergeEntry } from '$lib/types';
    import { DAY_LABELS } from '$lib/types';
    import { mergeSchedules } from '$lib/api';
    import { assignEmojis } from '$lib/emoji-mapper';
    import { getWorstConflict } from '$lib/conflict';
    import { CONFLICT_COLORS, MAX_MERGE_TOKENS } from '$lib/constants';
    import { appState } from '$lib/stores.svelte';

    const BADGE_COUNT = 4;

    let inputToken = $state('');
    let extraTokens = $state<string[]>([]);
    let mergeData = $state<{ schedules: MergeEntry[]; acts: ActSummary[] } | null>(null);
    let loading = $state(false);
    let error = $state<string | null>(null);

    const allTokens = $derived.by(() => {
        const base = appState.token ? [appState.token] : [];
        return [...base, ...extraTokens];
    });

    const emojiMap = $derived(assignEmojis(allTokens));

    const atCapacity = $derived(allTokens.length >= MAX_MERGE_TOKENS);

    // Map each token to a badge index (cycles through 0..BADGE_COUNT-1)
    const tokenBadgeIndex = $derived.by(() => {
        const map = new Map<string, number>();
        allTokens.forEach((token, i) => map.set(token, i % BADGE_COUNT));
        return map;
    });

    function addToken(): void {
        const trimmed = inputToken.trim();
        if (!trimmed || allTokens.includes(trimmed) || atCapacity) return;
        extraTokens = [...extraTokens, trimmed];
        inputToken = '';
    }

    function removeToken(token: string): void {
        extraTokens = extraTokens.filter((t) => t !== token);
    }

    function handleKeydown(e: KeyboardEvent): void {
        if (e.key === 'Enter') addToken();
    }

    $effect(() => {
        const tokens = allTokens;
        if (tokens.length === 0) {
            mergeData = null;
            return;
        }
        loading = true;
        error = null;
        mergeSchedules(tokens)
            .then((data) => {
                mergeData = data;
            })
            .catch((err: unknown) => {
                error = err instanceof Error ? err.message : 'Failed to load merged schedules';
            })
            .finally(() => {
                loading = false;
            });
    });

    const pickersBySlug = $derived.by(() => {
        if (!mergeData) return new Map<string, string[]>();
        const map = new Map<string, string[]>();
        for (const entry of mergeData.schedules) {
            for (const slug of entry.picks) {
                if (!map.has(slug)) map.set(slug, []);
                map.get(slug)!.push(entry.token);
            }
        }
        return map;
    });

    const groupedByDay = $derived.by(() => {
        if (!mergeData) return [];
        const sorted = [...mergeData.acts].sort(
            (a, b) => a.date.localeCompare(b.date) || a.start.localeCompare(b.start)
        );
        const byDate = new Map<string, ActSummary[]>();
        for (const act of sorted) {
            if (!byDate.has(act.date)) byDate.set(act.date, []);
            byDate.get(act.date)!.push(act);
        }
        return [...byDate.entries()].map(([date, acts]) => ({ date, acts }));
    });

    const allPickSets = $derived.by(() => {
        if (!mergeData) return new Set<string>();
        const union = new Set<string>();
        for (const entry of mergeData.schedules) {
            for (const slug of entry.picks) union.add(slug);
        }
        return union;
    });

    function conflictColor(act: ActSummary): string {
        if (!mergeData) return CONFLICT_COLORS.none;
        const level: ConflictLevel = getWorstConflict(act, mergeData.acts, allPickSets);
        return CONFLICT_COLORS[level];
    }

    function badgeClass(token: string): string {
        const idx = tokenBadgeIndex.get(token) ?? 0;
        return `fqf-merge-badge-${idx}`;
    }
</script>

<div class="flex flex-col overflow-y-auto h-full">
    <!-- Token bar -->
    <div class="shrink-0 px-3 py-2 border-b fqf-filter-panel">
        <div class="flex flex-wrap gap-1.5 items-center mb-2">
            {#if appState.token}
                <span
                    class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium {badgeClass(
                        appState.token
                    )}"
                >
                    <span class="fqf-emoji-circle {badgeClass(appState.token)}">
                        {emojiMap[appState.token]}
                    </span>
                    {appState.token}
                    <span class="text-xs opacity-60">(you)</span>
                </span>
            {/if}
            {#each extraTokens as token (token)}
                <span
                    class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium {badgeClass(
                        token
                    )}"
                >
                    <span class="fqf-emoji-circle {badgeClass(token)}">
                        {emojiMap[token]}
                    </span>
                    {token}
                    <button
                        class="ml-0.5 leading-none opacity-60 hover:opacity-100 transition-opacity"
                        onclick={() => removeToken(token)}
                        aria-label="Remove {token}"
                    >
                        &times;
                    </button>
                </span>
            {/each}
        </div>

        <div class="flex gap-2">
            <input
                type="text"
                placeholder="Add friend's token…"
                bind:value={inputToken}
                onkeydown={handleKeydown}
                disabled={atCapacity}
                class="flex-1 text-sm px-2 py-1 rounded border disabled:opacity-50 focus:outline-none"
                style="border-color: rgba(74, 26, 107, 0.25); background: var(--mg-card); focus:border-color: var(--mg-purple);"
            />
            <button
                onclick={addToken}
                disabled={atCapacity || !inputToken.trim()}
                class="px-3 py-1 text-sm rounded font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                style="background: var(--mg-purple); color: white;"
            >
                Add
            </button>
        </div>
        {#if atCapacity}
            <p class="text-xs mt-1" style="color: rgba(74, 26, 107, 0.5);">
                Maximum of {MAX_MERGE_TOKENS} tokens reached.
            </p>
        {/if}
    </div>

    <!-- Content area -->
    {#if allTokens.length === 0}
        <div
            class="flex flex-col items-center justify-center h-full gap-2"
            style="color: rgba(74, 26, 107, 0.5);"
        >
            <p class="text-lg font-medium">No tokens added</p>
            <p class="text-sm">Add your token or a friend's to see merged picks.</p>
        </div>
    {:else if loading}
        <div class="flex items-center justify-center h-full">
            <p style="color: var(--mg-purple); opacity: 0.6;">Loading merged schedule…</p>
        </div>
    {:else if error}
        <div class="flex items-center justify-center h-full">
            <p style="color: #dc2626;">{error}</p>
        </div>
    {:else if mergeData && mergeData.acts.length === 0}
        <div class="flex items-center justify-center h-full" style="color: rgba(74, 26, 107, 0.5);">
            <p>No acts picked across these schedules.</p>
        </div>
    {:else if mergeData}
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
                                {#each pickers as token (token)}
                                    <span
                                        class="fqf-emoji-circle {badgeClass(token)}"
                                        title={token}
                                        aria-label={token}
                                    >
                                        {emojiMap[token] ?? '?'}
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

        <!-- Legend -->
        <div
            class="shrink-0 border-t px-3 py-2 flex flex-wrap gap-x-4 gap-y-1"
            style="border-color: rgba(74, 26, 107, 0.12); background: rgba(250, 246, 240, 0.95);"
        >
            {#each allTokens as token (token)}
                <span class="inline-flex items-center gap-1 text-xs" style="color: var(--mg-text);">
                    <span class="fqf-emoji-circle {badgeClass(token)}">
                        {emojiMap[token]}
                    </span>
                    {token}
                    {#if token === appState.token}
                        <span style="color: rgba(74, 26, 107, 0.4);">(you)</span>
                    {/if}
                </span>
            {/each}
        </div>
    {/if}
</div>
