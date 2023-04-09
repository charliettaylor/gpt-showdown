<script>
  import { onMount } from "svelte";
  export let quiz;

  let ws;

  const start_game = () => {
    game.action = "START";
    ws.send(JSON.stringify(game));
  };

  let game = {
    state: "NOT_CREATED",
    nickname: "host",
    quiz_id: quiz.id,
    player_count: 0,
  };

  onMount(() => {
    ws = new WebSocket("ws://localhost:8000/ws");

    ws.addEventListener("message", (e) => {
      const msg = JSON.parse(e.data);
      console.log(msg);
      game = msg;
    });

    ws.addEventListener("open", (e) => {
      game.action = "CREATE";
      ws.send(JSON.stringify(game));
    });
  });
</script>

<div>
  {#if game.state == "LOBBY"}
    <h1>
      {game.game_id}
    </h1>
    <button on:click={start_game}>Start Game</button>
  {/if}

  {#if game.countdown}
    <h1>
      {game.countdown}
    </h1>
  {/if}

  {#if game.question}
    <h1>
      {game.question.text}
    </h1>
    {#each game.question.choices as choice}
      <h3>{choice.value}</h3>
    {/each}
  {/if}

  {#if game.state == "ANSWER"}
    <h2>Answer</h2>
    <h3>{game.answer}</h3>
    <h3>Answer</h3>
    <h1>Leaderboard</h1>
    {#each game.leaderboard as player}
      <h3>{player.nickname}: {player.score}</h3>
    {/each}
  {/if}

  {#if game.state == "GAMEOVER"}
    <h1>Game Over!</h1>
  {/if}
</div>

<style>
  button {
    background-color: red;
  }
</style>
