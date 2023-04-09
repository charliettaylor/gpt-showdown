<script>
  import Quizzes from "./Quizzes.svelte";
  import Game from "./Game.svelte";
  let state = "quizzes";
  let quiz;

  function handleMessage(event) {
    state = "host_game";
    quiz = event.detail.quiz;
  }
</script>

<div>
  {#if state == "quizzes"}
    <Quizzes on:select_quiz={handleMessage} />
  {/if}
  {#if state == "host_game"}
    <Game {quiz} />
  {/if}
</div>
