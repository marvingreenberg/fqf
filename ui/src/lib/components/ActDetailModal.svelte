<script lang="ts">
    import type { ActDetail } from '$lib/types';
    import { formatTime12 } from '$lib/map-utils';
    import PickButtons from '$lib/components/PickButtons.svelte';
    import Modal from '$lib/components/Modal.svelte';

    interface Props {
        act: ActDetail | null;
        loading: boolean;
        stageLocations: Map<string, { lat: number; lng: number }>;
        isPicked: boolean;
        isMaybe: boolean;
        readOnly: boolean;
        onTogglePick?: () => void;
        onToggleMaybe?: () => void;
        onClose: () => void;
    }

    let {
        act,
        loading,
        stageLocations,
        isPicked,
        isMaybe,
        readOnly,
        onTogglePick,
        onToggleMaybe,
        onClose
    }: Props = $props();
</script>

<Modal {onClose} ariaLabel="Act detail">
    {#if loading}
        <p style="color: var(--mg-purple); opacity: 0.6;">Loading…</p>
    {:else if act}
        <div class="flex items-center gap-2 mb-3">
            {#if !readOnly}
                <PickButtons
                    {isPicked}
                    {isMaybe}
                    size={20}
                    onTogglePick={() => onTogglePick?.()}
                    onToggleMaybe={() => onToggleMaybe?.()}
                    ariaName={act?.name ?? 'act'}
                />
            {/if}

            {#if act.websites.length > 0}
                {#each act.websites as url}
                    <a
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        title={new URL(url).hostname.replace('www.', '')}
                        class="shrink-0 hover:scale-110 transition-transform"
                        style="color: var(--mg-purple);"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="18"
                            height="18"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        >
                            <circle cx="12" cy="12" r="10" />
                            <path d="M2 12h20" />
                            <path
                                d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"
                            />
                        </svg>
                    </a>
                {/each}
            {/if}

            {#if stageLocations.has(act.stage)}
                {@const loc = stageLocations.get(act.stage)}
                <a
                    href="https://www.google.com/maps/dir/?api=1&destination={loc?.lat},{loc?.lng}"
                    target="_blank"
                    rel="noopener noreferrer"
                    title="Directions to {act.stage}"
                    class="shrink-0 hover:scale-110 transition-transform"
                    style="color: var(--mg-green-deep);"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    >
                        <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" />
                        <circle cx="12" cy="10" r="3" />
                    </svg>
                </a>
            {/if}

            <h2
                class="flex-1 min-w-0 text-xl font-bold leading-snug"
                style="font-family: 'Playfair Display', Georgia, serif; color: var(--mg-purple-deep);"
            >
                {act.name}
            </h2>

            <span class="fqf-genre-badge shrink-0">
                {act.genre}
            </span>
        </div>

        <p class="fqf-card-time mb-3 flex items-center gap-1.5">
            {act.stage} &middot; {formatTime12(act.start)}&#8211;{formatTime12(act.end)}
        </p>

        <div class="fqf-bio-body-scroll">
            <p class="fqf-bio-body">
                {act.about || 'No bio available yet.'}
            </p>
        </div>
    {/if}
</Modal>
