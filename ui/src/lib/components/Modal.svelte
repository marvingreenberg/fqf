<script lang="ts">
    import type { Snippet } from 'svelte';

    interface Props {
        onClose: () => void;
        ariaLabel?: string;
        children: Snippet;
    }

    let { onClose, ariaLabel = 'Dialog', children }: Props = $props();
</script>

<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
<div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    onclick={onClose}
    role="dialog"
    aria-modal="true"
    aria-label={ariaLabel}
    onkeydown={(e) => e.key === 'Escape' && onClose()}
    tabindex="-1"
>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    <div
        class="fqf-modal-card max-w-lg w-full mx-4 relative"
        onclick={(e) => e.stopPropagation()}
        role="document"
    >
        <div class="fqf-modal-header-strip"></div>

        <button
            class="absolute top-5 right-4 text-xl leading-none z-10"
            style="color: rgba(74, 26, 107, 0.5);"
            onclick={onClose}
            aria-label="Close"
        >
            ✕
        </button>

        <div class="p-6">
            {@render children()}
        </div>
    </div>
</div>
