<script>
  import Quiz from "./Quiz.svelte";
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  function select_quiz(quiz) {
    dispatch("select_quiz", {
      quiz: quiz,
    });
  }

  let quizzes = [];

  onMount(async () => {
    const res = await fetch("http://localhost:8000/api/get_quizzes");
    quizzes = await res.json();
  });

  let search;
</script>

<div class="block">
  <div class="field search block">
    <label for="search">Search</label>
    <input
      bind:value={search}
      class="input"
      name="search"
      type="text"
      autocomplete="off"
    />
  </div>
  <div id="quizzes" class="section">
    {#each quizzes as quiz}
      {#if !search || quiz.name.includes(search)}
        <Quiz on:select_quiz={() => select_quiz(quiz)} {quiz} />
      {/if}
    {/each}
  </div>
</div>

<style>
  #quizzes {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>
