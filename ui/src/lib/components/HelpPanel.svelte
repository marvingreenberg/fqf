<script lang="ts">
    import { FLEUR_PATH, QUESTION_PATH, PICKED_FLEUR_FILL } from '$lib/constants';
    import Modal from '$lib/components/Modal.svelte';

    const MAYBE_FILL = '#7c3aed';
    const ICON_SIZE = 16;
    const VIEWBOX = '0 0 16 16';

    interface Props {
        onClose: () => void;
    }

    let { onClose }: Props = $props();
</script>

<Modal {onClose} ariaLabel="Help">
    <h2
        class="text-lg font-bold mb-4"
        style="font-family: 'Playfair Display', Georgia, serif; color: var(--mg-purple-deep);"
    >
        FQF 2026 Schedule Builder
    </h2>

    <div class="text-sm leading-relaxed flex flex-col gap-4" style="color: var(--mg-text);">
        <section>
            <h3 class="font-semibold mb-1" style="color: var(--mg-purple-deep);">
                Picking &amp; Maybe
            </h3>
            <div class="flex flex-col gap-1.5">
                <p class="flex items-start gap-2">
                    <svg
                        class="shrink-0 mt-0.5"
                        viewBox={VIEWBOX}
                        width={ICON_SIZE}
                        height={ICON_SIZE}
                        fill={PICKED_FLEUR_FILL}
                    >
                        <path d={FLEUR_PATH} />
                    </svg>
                    <span
                        ><strong>Fleur-de-lis</strong> marks an act as a definite pick. It appears in
                        your schedule, shows conflicts with other picks, and syncs across devices.</span
                    >
                </p>
                <p class="flex items-start gap-2">
                    <svg
                        class="shrink-0 mt-0.5"
                        viewBox={VIEWBOX}
                        width={ICON_SIZE}
                        height={ICON_SIZE}
                        fill={MAYBE_FILL}
                    >
                        <path d={QUESTION_PATH} />
                    </svg>
                    <span
                        ><strong>Question mark</strong> marks an act as "maybe." It appears in your schedule
                        but doesn't trigger conflict warnings. Use it for acts you're interested in but
                        haven't committed to.</span
                    >
                </p>
                <p class="opacity-70">
                    The two are mutually exclusive. Tapping one clears the other. Tap again to
                    deselect.
                </p>
            </div>
        </section>

        <section>
            <h3 class="font-semibold mb-1" style="color: var(--mg-purple-deep);">Views</h3>
            <dl class="flex flex-col gap-1.5">
                <div>
                    <dt class="font-medium inline">All Acts</dt>
                    <dd class="inline opacity-80">
                        &mdash; browse every act by day. Desktop shows a time grid; mobile shows a
                        scrollable list. Use the filter panel to narrow by genre or stage.
                    </dd>
                </div>
                <div>
                    <dt class="font-medium inline">Map</dt>
                    <dd class="inline opacity-80">
                        &mdash; see what's playing at each stage. Scroll the time slider or tap
                        "Now" for live status. "My Schedule" mode shows your picks on the map with
                        numbered markers and walking paths.
                    </dd>
                </div>
                <div>
                    <dt class="font-medium inline">My Schedule</dt>
                    <dd class="inline opacity-80">
                        &mdash; your picks and maybes for the day, ordered by time. Shows conflicts
                        and walking distances between consecutive picks.
                    </dd>
                </div>
                <div>
                    <dt class="font-medium inline">Share</dt>
                    <dd class="inline opacity-80">
                        &mdash; compare schedules with friends. Generate a share link from the
                        avatar menu (top right), then send it. Shared schedules show each person's
                        picks with emoji badges.
                    </dd>
                </div>
            </dl>
        </section>

        <section>
            <h3 class="font-semibold mb-1" style="color: var(--mg-purple-deep);">
                Conflicts &amp; Distances
            </h3>
            <p class="opacity-80">
                When two picked acts overlap in time, both get colored borders:
                <span class="font-medium" style="color: #eab308;">yellow</span> for minor overlap,
                <span class="font-medium" style="color: #ef4444;">red</span> for major. Acts marked as "maybe" do not
                trigger conflicts. In My Schedule, walking distances between stages help you plan transitions.
            </p>
        </section>

        <section>
            <h3 class="font-semibold mb-1" style="color: var(--mg-purple-deep);">Offline</h3>
            <p class="opacity-80">
                The app works offline after first load. Your picks are saved locally and sync when
                you're back online. A wifi icon in the header shows your connection status.
            </p>
        </section>
    </div>
</Modal>
