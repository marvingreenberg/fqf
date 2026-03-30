<script lang="ts">
    import { createShare, deleteSchedule } from '$lib/api';
    import { appState } from '$lib/stores.svelte';

    const FLEUR = '⚜️';
    const SHARE_URL_BASE = '/fq2026';

    let open = $state(false);
    let shareUrl = $state<string | null>(null);
    let shareLoading = $state(false);
    let shareCopied = $state(false);

    // Logout modal: shown after logout to remind the user of their token
    let logoutModalVisible = $state(false);
    let logoutToken = $state('');

    // Delete confirmation dialog state
    let deleteConfirmVisible = $state(false);
    let deleteLoading = $state(false);
    let deleteError = $state('');

    const initials = $derived.by(() => {
        if (!appState.token) return '???';
        const words = appState.token.split('-');
        return words
            .slice(0, 3)
            .map((w) => w[0]?.toUpperCase() ?? '')
            .join('');
    });

    function buildShareUrl(shareId: string): string {
        const params = new URLSearchParams({ share: shareId });
        if (appState.name) params.set('name', appState.name);
        return `${SHARE_URL_BASE}?${params.toString()}`;
    }

    async function handleShare(): Promise<void> {
        if (!appState.token) return;
        shareLoading = true;
        try {
            const resp = await createShare(appState.token);
            shareUrl = buildShareUrl(resp.share_id);
        } finally {
            shareLoading = false;
        }
    }

    async function handleCopyShareUrl(): Promise<void> {
        if (!shareUrl) return;
        const fullUrl = `${window.location.origin}${shareUrl}`;
        await navigator.clipboard.writeText(fullUrl);
        shareCopied = true;
        setTimeout(() => {
            shareCopied = false;
        }, 2000);
    }

    function handleLogout(): void {
        open = false;
        shareUrl = null;
        // Capture token before clearing so we can show it in the reminder modal
        logoutToken = appState.token ?? '';
        appState.clearIdentity();
        logoutModalVisible = true;
    }

    function handleLogoutModalOk(): void {
        logoutModalVisible = false;
    }

    function handleDeleteClick(): void {
        open = false;
        shareUrl = null;
        deleteError = '';
        deleteConfirmVisible = true;
    }

    async function handleDeleteConfirm(): Promise<void> {
        if (!appState.token) return;
        deleteLoading = true;
        deleteError = '';
        try {
            await deleteSchedule(appState.token);
            deleteConfirmVisible = false;
            appState.clearIdentity();
        } catch {
            deleteError = 'Could not delete schedule. Please try again.';
        } finally {
            deleteLoading = false;
        }
    }

    function handleDeleteCancel(): void {
        deleteConfirmVisible = false;
        deleteError = '';
    }

    function handleOverlayClick(): void {
        open = false;
        shareUrl = null;
        shareCopied = false;
    }
</script>

<div class="relative">
    <button
        class="flex items-center gap-1.5 px-2 py-1 rounded-full transition-colors"
        style="border: 1px solid rgba(212, 168, 67, 0.5); background: rgba(212, 168, 67, 0.1); color: var(--mg-gold-bright);"
        onclick={() => {
            open = !open;
        }}
        aria-label="Identity menu"
        aria-expanded={open}
    >
        <span aria-hidden="true">{FLEUR}</span>
        <span
            class="text-xs font-bold tracking-wide"
            style="font-family: 'Courier New', monospace;"
        >
            {initials}
        </span>
    </button>

    {#if open}
        <!-- Overlay to close on outside click -->
        <button
            class="fixed inset-0 z-40"
            style="background: transparent; border: none; cursor: default;"
            onclick={handleOverlayClick}
            aria-label="Close menu"
            tabindex="-1"
        ></button>

        <div
            class="absolute right-0 top-full mt-2 z-50 w-64 rounded-xl overflow-hidden shadow-xl"
            style="background: var(--mg-cream); border: 1px solid rgba(74, 26, 107, 0.15);"
        >
            <!-- Token display -->
            <div
                class="px-4 py-3"
                style="background: linear-gradient(135deg, var(--mg-purple-deep) 0%, var(--mg-purple) 100%);"
            >
                <p
                    class="text-xs mb-0.5"
                    style="color: rgba(245, 215, 110, 0.7); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;"
                >
                    Your identity
                </p>
                <p
                    class="text-base font-bold"
                    style="font-family: 'Playfair Display', Georgia, serif; color: var(--mg-gold-bright); word-break: break-all;"
                >
                    {appState.token}
                </p>
                {#if appState.name}
                    <p class="text-xs mt-1" style="color: rgba(255,255,255,0.7);">
                        {appState.name}
                    </p>
                {/if}
            </div>

            <div class="px-4 py-3 flex flex-col gap-2">
                {#if shareUrl}
                    <div
                        class="rounded-lg p-2 text-xs break-all"
                        style="background: rgba(74, 26, 107, 0.07); border: 1px solid rgba(212, 168, 67, 0.35); color: var(--mg-purple-deep);"
                    >
                        {shareUrl}
                    </div>
                    <button class="fqf-btn-gold text-sm py-1.5" onclick={handleCopyShareUrl}>
                        {shareCopied ? 'Copied!' : 'Copy share link'}
                    </button>
                {:else}
                    <button
                        class="fqf-btn-outline text-sm py-1.5"
                        onclick={handleShare}
                        disabled={shareLoading || !appState.token}
                    >
                        {shareLoading ? 'Generating…' : 'Share my schedule'}
                    </button>
                {/if}

                <button class="fqf-btn-ghost text-sm" onclick={handleLogout}> Logout </button>
                <button
                    class="fqf-btn-ghost text-sm"
                    style="color: #dc2626; border-color: rgba(220, 38, 38, 0.3);"
                    onclick={handleDeleteClick}
                >
                    Delete schedule
                </button>
            </div>
        </div>
    {/if}
</div>

<!-- Logout reminder modal -->
{#if logoutModalVisible}
    <div
        class="fixed inset-0 z-50 flex items-center justify-center"
        style="background: rgba(26, 10, 40, 0.75);"
    >
        <div
            class="fqf-dialog-card w-full max-w-sm mx-4"
            role="dialog"
            aria-modal="true"
            aria-labelledby="logout-modal-title"
        >
            <div class="fqf-dialog-header text-center py-5 px-6">
                <h2 id="logout-modal-title" class="text-lg">Logged out</h2>
            </div>
            <div class="fqf-dialog-body flex flex-col gap-4">
                <p class="text-sm" style="color: var(--mg-purple-deep);">
                    Your schedule is still stored as
                </p>
                <p
                    class="text-base font-bold px-3 py-2 rounded-lg"
                    style="font-family: 'Courier New', monospace; background: rgba(74,26,107,0.07); color: var(--mg-gold-dark); word-break: break-all;"
                >
                    {logoutToken}
                </p>
                <p class="text-sm" style="color: var(--mg-purple-deep);">
                    You have to remember those secret words. You can load it on this or another
                    device.
                </p>
                <button class="fqf-btn-gold w-full" onclick={handleLogoutModalOk}>OK</button>
            </div>
        </div>
    </div>
{/if}

<!-- Delete confirmation dialog -->
{#if deleteConfirmVisible}
    <div
        class="fixed inset-0 z-50 flex items-center justify-center"
        style="background: rgba(26, 10, 40, 0.75);"
    >
        <div
            class="fqf-dialog-card w-full max-w-sm mx-4"
            role="dialog"
            aria-modal="true"
            aria-labelledby="delete-modal-title"
        >
            <div class="fqf-dialog-header text-center py-5 px-6">
                <h2 id="delete-modal-title" class="text-lg">Delete schedule?</h2>
            </div>
            <div class="fqf-dialog-body flex flex-col gap-4">
                <p class="text-sm" style="color: var(--mg-purple-deep);">
                    This will permanently delete your saved fest schedule. Are you sure?
                </p>
                {#if deleteError}
                    <p class="text-sm" style="color: #dc2626;">{deleteError}</p>
                {/if}
                <div class="flex gap-2">
                    <button
                        class="fqf-btn-ghost flex-1"
                        onclick={handleDeleteCancel}
                        disabled={deleteLoading}
                    >
                        Cancel
                    </button>
                    <button
                        class="fqf-btn-ghost flex-1"
                        style="color: #dc2626; border-color: rgba(220, 38, 38, 0.4); background: rgba(220, 38, 38, 0.07);"
                        onclick={handleDeleteConfirm}
                        disabled={deleteLoading}
                    >
                        {deleteLoading ? 'Deleting…' : 'Delete'}
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}
