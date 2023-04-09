<script>
  export let quiz;

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  function select_quiz() {
    dispatch("select_quiz", {
      quiz: quiz,
    });
  }
</script>

<button on:click={select_quiz} class="box">
  <h3>{quiz.name}</h3>
  <p>{quiz.category}</p>
</button>
