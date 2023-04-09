<script>
  import { onMount } from "svelte";
  export let quiz;

  let ws;
  let time;

  let colors = ["red", "blue", "yellow", "green"];


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
    setInterval(() => {
      if (time && time > 0) {
        time -= 1;
      }
    }, 1000);
    ws = new WebSocket("ws://localhost:8000/ws");

    ws.addEventListener("message", (e) => {
      const msg = JSON.parse(e.data);
      if (msg.state == "QUESTION") {
        time = 30;
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
    <div class="block">
      <button class="green" on:click={start_game}>Start Game</button>
    </div>
  {/if}

  {#if game.countdown}
    <h1>{game.countdown}</h1>
  {/if}

  {#if game.question}
    <div id="time">{time}</div>
    <h1>{game.question.text}</h1>
    <div id="answer_choices">
      {#each game.question.choices as choice, i}
        <div class="choice"><div class={colors[i]}>{choice.value}</div></div>
      {/each}
    </div>
  {/if}

  {#if game.state == "ANSWER"}
    <div class="leader">
      <div class="block">
        <h2>Answer: {game.answer}</h2>
      </div>
      <div class="block">
        <h2>Leaderboard</h2>
      </div>
      <table class="table">
        <tbody class="tbody">
          {#each game.leaderboard as player}
            {#if player.nickname != "host"}
              <tr>
                <td>{player.nickname}</td>
                <td>{player.score}</td>
              </tr>
            {/if}
          {/each}
        </tbody>
      </table>
    </div>
  {/if}

  {#if game.state == "GAMEOVER"}
    <h1>Game Over!</h1>
  {/if}
</div>

<style>

  #answer_choices {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
  }

  #answer_choices > div {
    flex: 50%;
    margin-bottom: 10px;
  }

  .choice {
    width: 100%;
  }

  .choice > div {
    border: 4px solid black;
    border-radius: 10px;
    background-color: white;
    padding: 10px;
    width: 20vw;
    padding: 50px;
    height: 100%;
  }

  .leader {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  table,
  tbody {
    background: none;
    border: 4px solid black;
    border-radius: 10px;
  }

  h2 {
    font-size: 2em;
  }

  td {
    font-size: 3em;
  }

  #time {
    position: absolute;
    top: 3em;
    right: 3em;
    font-size: 2em;
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
