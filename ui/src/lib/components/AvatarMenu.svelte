<script lang="ts">
    import { createShare } from '$lib/api';
    import { appState } from '$lib/stores.svelte';

    const FLEUR = '⚜️';
    const SHARE_URL_BASE = '/fq2026';

    let open = $state(false);
    let shareUrl = $state<string | null>(null);
    let shareLoading = $state(false);
    let shareCopied = $state(false);

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

    function handleClearIdentity(): void {
        open = false;
        shareUrl = null;
        appState.clearIdentity();
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

                <button class="fqf-btn-ghost text-sm" onclick={handleClearIdentity}>
                    Clear identity
                </button>
            </div>
        </div>
    {/if}
</div>
