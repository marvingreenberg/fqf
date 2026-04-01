<script lang="ts">
    import { goto } from '$app/navigation';
    import { loadSharedSchedule } from '$lib/api';
    import { appState } from '$lib/stores.svelte';
    import LoginForm from '$lib/components/LoginForm.svelte';

    interface Props {
        shareName: string;
        shareHash: string;
        ondismiss: () => void;
    }

    let { shareName, shareHash, ondismiss }: Props = $props();

    const MAIN_SCHEDULE_ROUTE = '/fq2026';

    async function attachShare(): Promise<void> {
        const shared = await loadSharedSchedule(shareHash);
        await appState.addSharedSchedule({
            share_id: shareHash,
            name: shared.name,
            picks: shared.picks,
            acts: shared.acts
        });
        appState.setViewMode('share');
        goto(MAIN_SCHEDULE_ROUTE);
    }
</script>

<div class="fqf-dialog-card w-full max-w-sm mx-4">
    <div class="fqf-dialog-header text-center py-6 px-6">
        <div class="text-4xl mb-2" aria-hidden="true">⚜️</div>
        <h2 class="text-2xl mb-1">{shareName}'s Schedule</h2>
        <p class="text-sm" style="color: rgba(245, 215, 110, 0.85);">French Quarter Fest 2026</p>
    </div>

    <div class="fqf-dialog-body flex flex-col gap-4">
        <LoginForm
            loadLabel="If you have an existing schedule, load it"
            newLabel="Create a new schedule, to compare with {shareName}'s picks!"
            onConfirmed={attachShare}
        >
            {#snippet newSectionExtra()}
                <p class="text-xs" style="color: rgba(74,26,107,0.65); font-style: italic;">
                    Give your schedule a name to share back
                </p>
                <p class="text-xs font-medium" style="color: rgba(74,26,107,0.8);">
                    🪄 {shareName}'s schedule will be added as a share
                </p>
            {/snippet}

            {#snippet footer()}
                <hr style="border-color: rgba(74,26,107,0.15);" />
                <button class="fqf-btn-gold w-full" onclick={ondismiss}>
                    See {shareName}'s schedule
                </button>
            {/snippet}
        </LoginForm>
    </div>
</div>
