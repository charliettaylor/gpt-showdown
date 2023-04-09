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
</script>

<div class="block">
  <div class="field search">
    <label for="search">Filter</label>
    <input class="input" name="search" type="text" />
  </div>
  <div class="block">
    {#each quizzes as quiz}
      <Quiz on:select_quiz={() => select_quiz(quiz)} {quiz} />
    {/each}
  </div>
</div>
