<script lang="ts">
    import '../app.css';

    let { children } = $props();
</script>

<div class="min-h-screen flex flex-col">
    <header class="bg-primary-500 text-white p-4 flex items-center justify-between">
        <strong class="text-xl">FQF 2026</strong>
        <span class="text-sm opacity-75">French Quarter Fest Schedule Builder</span>
    </header>
    <main class="flex-1">
        {@render children()}
    </main>
</div>
