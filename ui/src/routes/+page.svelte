<script lang="ts">
    const APP_DESCRIPTION =
        'This app is not associated with any public or private festival, but provides publicly available fest schedules for fest-goers\u2019 convenience.';
</script>

<div
    class="min-h-screen flex flex-col items-center justify-center px-6"
    style="background: linear-gradient(160deg, var(--mg-purple-deep) 0%, var(--mg-purple) 60%, var(--mg-green-deep) 100%);"
>
    <div class="text-center max-w-md">
        <!-- Fleur-de-lis accent -->
        <div class="text-5xl mb-4" aria-hidden="true">⚜️</div>

        <h1
            class="text-5xl font-bold mb-3"
            style="color: var(--mg-gold-bright); font-family: 'Playfair Display', Georgia, serif; text-shadow: 0 2px 8px rgba(0,0,0,0.4);"
        >
            Fest Schedule
        </h1>

        <p class="text-lg mb-2" style="color: rgba(255,255,255,0.85);">
            Your personal festival schedule builder
        </p>

        <p class="text-sm mb-8 leading-relaxed" style="color: rgba(255,255,255,0.55);">
            {APP_DESCRIPTION}
        </p>

        <a
            href="/fq2026"
            class="inline-block px-8 py-3 rounded-full font-bold text-base transition-opacity hover:opacity-90"
            style="background: linear-gradient(135deg, var(--mg-gold-rich) 0%, var(--mg-gold-bright) 100%); color: var(--mg-purple-deep); text-decoration: none; box-shadow: 0 4px 16px rgba(0,0,0,0.25);"
        >
            French Quarter Fest 2026 →
        </a>
    </div>
</div>
