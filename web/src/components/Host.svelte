<script>
  import { onMount } from "svelte";
  import Quiz from "./Quiz.svelte";

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
      <Quiz name={quiz.name} category={quiz.category} />
    {/each}
  </div>
</div>
