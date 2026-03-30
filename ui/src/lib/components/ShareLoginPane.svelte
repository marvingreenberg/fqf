<script lang="ts">
    import { goto } from '$app/navigation';
    import { createSchedule, fuzzyLookup, loadSharedSchedule } from '$lib/api';
    import { getFingerprint } from '$lib/fingerprint';
    import { appState } from '$lib/stores.svelte';
    import { FINGERPRINT_COUNTER_KEY } from '$lib/types';

    interface Props {
        shareName: string;
        shareHash: string;
        ondismiss: () => void;
    }

    let { shareName, shareHash, ondismiss }: Props = $props();

    const MAIN_SCHEDULE_ROUTE = '/fq2026';

    let tripleInput = $state('');
    let nameInput = $state('');
    let errorMsg = $state('');
    let loading = $state(false);

    async function loadAndAttachShare(): Promise<void> {
        const shared = await loadSharedSchedule(shareHash);
        await appState.addSharedSchedule({
            share_id: shareHash,
            name: shared.name,
            picks: shared.picks,
            acts: shared.acts
        });
    }

    async function handleLoad(): Promise<void> {
        const triple = tripleInput.trim();
        if (!triple) {
            errorMsg = 'Please enter your secret words.';
            return;
        }
        loading = true;
        errorMsg = '';
        try {
            const result = await fuzzyLookup(triple);
            await appState.confirm(result.token, result.name);
            await loadAndAttachShare();
            appState.setViewMode('share');
            goto(MAIN_SCHEDULE_ROUTE);
        } catch {
            errorMsg = 'Schedule not found. Check your secret words.';
        } finally {
            loading = false;
        }
    }

    async function handleNew(): Promise<void> {
        const name = nameInput.trim();
        if (!name) {
            errorMsg = 'Please enter a name for your schedule.';
            return;
        }
        loading = true;
        errorMsg = '';
        try {
            const fingerprintHash = await getFingerprint();
            const rawCounter = localStorage.getItem(FINGERPRINT_COUNTER_KEY);
            const counter = rawCounter !== null ? parseInt(rawCounter, 10) || 0 : 0;

            const resp =
                fingerprintHash !== null
                    ? await createSchedule(name, fingerprintHash, counter)
                    : await createSchedule(name);

            const nextCounter = counter + 1;
            localStorage.setItem(FINGERPRINT_COUNTER_KEY, String(nextCounter));
            await appState.confirm(resp.token, name, nextCounter);
            await loadAndAttachShare();
            appState.setViewMode('share');
            goto(MAIN_SCHEDULE_ROUTE);
        } catch {
            errorMsg = 'Could not create schedule. Please try again.';
        } finally {
            loading = false;
        }
    }

    function handleSee(): void {
        ondismiss();
    }

    function handleTripleKeydown(e: KeyboardEvent): void {
        if (e.key === 'Enter') handleLoad();
    }

    function handleNameKeydown(e: KeyboardEvent): void {
        if (e.key === 'Enter') handleNew();
    }
</script>

<div class="fqf-dialog-card w-full max-w-sm mx-4">
    <div class="fqf-dialog-header text-center py-6 px-6">
        <div class="text-4xl mb-2" aria-hidden="true">⚜️</div>
        <h2 class="text-2xl mb-1">{shareName}'s Schedule</h2>
        <p class="text-sm" style="color: rgba(245, 215, 110, 0.85);">French Quarter Fest 2026</p>
    </div>

    <div class="fqf-dialog-body flex flex-col gap-4">
        <!-- Load existing schedule -->
        <div class="flex flex-col gap-2">
            <p class="text-xs" style="color: rgba(74,26,107,0.65); font-style: italic;">
                If you have an existing schedule, load it
            </p>
            <p class="text-xs font-medium" style="color: rgba(74,26,107,0.8);">
                🪄 {shareName}'s schedule will be added as a share
            </p>
            <button class="fqf-btn-gold w-full" onclick={handleLoad} disabled={loading}>
                {loading ? 'Loading…' : 'Load Schedule'}
            </button>
            <input
                id="share-triple"
                class="input w-full text-sm"
                type="text"
                placeholder="enter your secret words"
                style={tripleInput
                    ? 'color: #1a1a1a;'
                    : 'color: rgba(74,26,107,0.4); font-style: italic; font-size: 0.8rem;'}
                bind:value={tripleInput}
                onkeydown={handleTripleKeydown}
            />
        </div>

        <hr style="border-color: rgba(74,26,107,0.15);" />

        <!-- New schedule -->
        <div class="flex flex-col gap-2">
            <p class="text-xs" style="color: rgba(74,26,107,0.65); font-style: italic;">
                Create a new schedule, to compare with {shareName}'s picks!
            </p>
            <p class="text-xs" style="color: rgba(74,26,107,0.65); font-style: italic;">
                Give your schedule a name to share back
            </p>
            <button class="fqf-btn-gold w-full" onclick={handleNew} disabled={loading}>
                {loading ? 'Creating…' : 'New Schedule'}
            </button>
            <div class="flex items-center gap-2">
                <label
                    for="share-name"
                    class="text-sm font-semibold shrink-0"
                    style="color: var(--mg-purple-deep);"
                >
                    Name:
                </label>
                <input
                    id="share-name"
                    class="input flex-1 text-sm"
                    type="text"
                    placeholder="Fred, BooBoo, …"
                    style={nameInput
                        ? ''
                        : 'color: rgba(74,26,107,0.4); font-style: italic; font-size: 0.8rem;'}
                    bind:value={nameInput}
                    onkeydown={handleNameKeydown}
                />
            </div>
        </div>

        {#if errorMsg}
            <p class="text-sm" style="color: #dc2626;">{errorMsg}</p>
        {/if}

        <hr style="border-color: rgba(74,26,107,0.15);" />

        <!-- See read-only -->
        <button class="fqf-btn-gold w-full" onclick={handleSee} disabled={loading}>
            See {shareName}'s schedule
        </button>
    </div>
</div>
