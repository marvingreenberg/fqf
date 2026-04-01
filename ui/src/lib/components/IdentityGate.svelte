<script lang="ts">
    import { onMount } from 'svelte';
    import { loadSharedSchedule } from '$lib/api';
    import LoginForm from '$lib/components/LoginForm.svelte';

    interface Props {
        pendingShareId?: string | null;
        pendingShareName?: string | null;
    }

    let { pendingShareId = null, pendingShareName = null }: Props = $props();

    // null = not yet checked (pending), true/false = resolved after mount
    // Start as null only when there is a share to validate, otherwise false (no share)
    let shareValid = $state<boolean | null>(null);
    let shareValidName = $state<string>('');
    let shareError = $state('');

    onMount(async () => {
        if (!pendingShareId) {
            shareValid = false;
            return;
        }
        try {
            const resp = await loadSharedSchedule(pendingShareId);
            shareValidName = pendingShareName ?? resp.name;
            shareValid = true;
        } catch {
            shareValid = false;
            shareError = '(!) Share not found';
        }
    });

    function handleViewShareOnly(): void {
        if (!pendingShareId) return;
        window.location.href = `/fq2026/${pendingShareId}`;
    }
</script>

<div
    class="fixed inset-0 z-50 flex items-center justify-center"
    style="background: rgba(26, 10, 40, 0.88);"
>
    <div class="fqf-dialog-card w-full max-w-sm mx-4">
        <!-- Festive header -->
        <div class="fqf-dialog-header text-center py-6 px-6">
            <div class="text-4xl mb-2" aria-hidden="true">⚜️</div>
            <h2 class="text-2xl mb-1">Fest Schedule</h2>
            <p class="text-sm" style="color: rgba(245, 215, 110, 0.85);">
                French Quarter Fest 2026
            </p>
        </div>

        <div class="fqf-dialog-body flex flex-col gap-4">
            <!-- Share-not-found banner -->
            {#if shareValid === false && shareError}
                <p class="text-sm font-medium" style="color: #c05000; font-style: italic;">
                    {shareError}
                </p>
            {/if}

            <LoginForm
                loadLabel="If you have an existing schedule, you can load it"
                newLabel="Create a schedule. Name for sharing, a nickname is fine"
            >
                {#snippet newSectionExtra()}
                    {#if shareValid === true}
                        <p
                            class="text-xs"
                            style="color: rgba(74,26,107,0.6); font-style: italic;"
                        >
                            Create a schedule to allow comparing with {shareValidName}
                        </p>
                    {/if}
                {/snippet}

                {#snippet footer()}
                    {#if pendingShareId && shareValid === true}
                        <button
                            class="fqf-btn-ghost"
                            onclick={handleViewShareOnly}
                        >
                            View {shareValidName}'s schedule?
                            <span
                                class="block text-xs"
                                style="color: rgba(74,26,107,0.5); font-style: italic;"
                            >
                                view only, no changes can be made
                            </span>
                        </button>
                    {/if}
                {/snippet}
            </LoginForm>
        </div>
    </div>
</div>
