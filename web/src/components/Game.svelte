<script>
  import { onMount } from "svelte";
  export let quiz;

  let ws;
  let time;

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
      if (msg.state == "QUESTION") {
        time = 30;
        setInterval(() => {
          if (time > 0) {
            time -= 1;
          } else {
            clearInterval(this);
          }
        }, 1000);
      }
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
    <div class="block">
      <p id="splash">Enter the code:</p>
      <h1 id="game_code">
        {game.game_id}
      </h1>
    </div>
    <div class="block" id="players">{game.player_count} Players</div>
    <div class="block"><button on:click={start_game}>Start Game</button></div>
  {/if}

  {#if game.countdown}
    <h1>{game.countdown}</h1>
  {/if}

  {#if game.question}
    <div id="time">{time}</div>
    <h1>{game.question.text}</h1>
    <div id="answer_choices">
      {#each game.question.choices as choice}
        <div class="choice">{choice.value}</div>
      {/each}
    </div>
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
  #time {
    position: absolute;
    top: 3em;
    right: 3em;
    font-size: 2em;
  }

  button {
    background-color: red;
  }

  #answer_choices {
    display: flex;
    flex-wrap: wrap;
  }

  #answer_choices > div {
    flex: 50%;
    margin-bottom: 10px;
  }

  .choice {
    width: 100%;
    background-color: orange;
  }

  #players {
    font-size: 2em;
  }

  #splash {
    position: relative;
    font-size: 2em;
    transform: translateX(-50%) rotate(-15deg);
  }

  #game_code {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: min(20vw, 8rem);
    animation: 5s float ease-in-out infinite;
    text-shadow: #ccc 3px 5px 2px;
  }
</style>
