<script lang="ts">
  import Home from "./components/Home.svelte";
  import Host from "./components/Host.svelte";

  const path = location.pathname;

</script>

<main>
  {#if (path == "/")}
    <Home />
    <footer>
      <small>Create a quiz <a href="/host">here!</a></small>
    </footer>
  {/if}
  {#if (path == "/host")}
    <Host />
  {/if}
</main>

<style>
  footer {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    padding: 10px;
  }
</style>
