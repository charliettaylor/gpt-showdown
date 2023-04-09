<script lang="ts">
  import Home from "./components/Home.svelte";
</script>

<nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a
      href="#"
      role="button"
      class="navbar-burger"
      aria-label="menu"
      aria-expanded="false"
    >
      <span aria-hidden="true" />
      <span aria-hidden="true" />
      <span aria-hidden="true" />
    </a>
  </div>
</nav>
<main>
  <Home />
</main>

<style>
  .navbar {
    background: none;
  }
</style>
