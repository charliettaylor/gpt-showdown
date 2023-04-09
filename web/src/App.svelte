<script lang="ts">
  import Play from "./components/Play.svelte";
  import Host from "./components/Host.svelte";

  const path = location.pathname;
</script>

<main>
  {#if path == "/"}
    <Play />
  {/if}
  {#if path == "/host"}
    <Host />
  {/if}
</main>

<style>
</style>
