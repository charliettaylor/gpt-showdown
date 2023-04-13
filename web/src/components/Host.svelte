<script>
  import Quizzes from "./Quizzes.svelte";
  import Game from "./Game.svelte";
  import Create from "./Create.svelte";

  //let state = "quizzes";
  let state = "quizzes";
  let quiz;

  function handleMessage(event) {
    state = "host_game";
    quiz = event.detail.quiz;
  }

  function state_change(event) {
    state = "quizzes";
  }
</script>

<div id="main" class="block">
  {#if state != "host_game"}
    <footer><a href="/">Go Back Home</a></footer>
  {/if}
  {#if state == "quizzes"}
    <h1 class="block">Select a Quiz</h1>
    <h4>or</h4>
    <button class="button" on:click={() => (state = "create_quiz")}
      >Create a Quiz</button
    >
    <Quizzes on:select_quiz={handleMessage} />
  {/if}
  {#if state == "host_game"}
    <Game {quiz} />
  {/if}
  {#if state == "create_quiz"}
    <Create on:quizzes={state_change} />
  {/if}
</div>

<style>
  #main {
    padding: 5vw;
    /* min-width: 50vw; */
    max-width: 70vw;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .block {
    margin-bottom: 0;
  }

  .button {
    margin-bottom: 2vh;
    border: 2px solid #333;
    transition: all 0.1s;
  }

  .button:hover {
    transform: scale(1.02);
  }

  footer {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
  }
</style>
