<script>
  import { onMount } from "svelte";
  import { slide } from "svelte/transition";
  import Shape from "./Shape.svelte";

  let entered_name = false;
  let entered_code = false;

  let medals = "🥇🥈🥉" + " ".repeat(999);

  let ws;
  let footer;

  let colors = ["red", "blue", "yellow", "green"];

  let game = {
    state: "NOT_CREATED",
    nickname: null,
    game_id: null,
  };

  const answer = (choice) => {
    game.action = "SUBMIT";
    game.choice = choice;
    ws.send(JSON.stringify(game));
  };

  let show_footer = true;
  const focus_input = () => {
    // mostly for mobile compatability
    show_footer = false;
  };

  const unfocus_input = () => {
    show_footer = true;
  };

  const join_game = () => {
    console.log("joining game");
    game.action = "JOIN";
    game.game_id = "" + game.game_id;
    ws.send(JSON.stringify(game));
  };

  const handleCodeInput = () => {
    console.log("handling code input");
    entered_code = true;
    game.action = "PING";
    game.nickname = "";
    ws.send(JSON.stringify(game));
  };

  const tryAgain = () => {
    entered_code = false;
    game.state = "NOT_CREATED";
    error = "";
    window.location.reload();
  };

  let ws_open = false;
  let error = "";

  onMount(() => {
    const url = import.meta.env.VITE_WS_BASE_URL;
    ws = new WebSocket(url);

    ws.addEventListener("open", (event) => {
      ws_open = true;
      console.log(ws_open);
    });
    ws.addEventListener("close", (event) => {
      ws_open = false;
    });

    ws.addEventListener("message", (e) => {
      if (e.data == "pong") {
        ws_open = true;
        return;
      }
      const msg = JSON.parse(e.data);
      if (msg.error) {
        error = msg.error;
        entered_code = false;
      }
      console.log("message: ", msg);

      game = msg;
    });
  });
</script>

<div>
  {#if ws_open}<h3 class="connection">🔌</h3>{/if}
  {#if game.state == "NOT_CREATED"}
    <div id="main">
      <Shape shape="circle" />
      <Shape shape="line" />
      <Shape shape="diamond" />
      <Shape shape="square" />
      <div class="block">
        <h1>GPT Quiz</h1>
      </div>
      {#if entered_code && ws_open}
        <form class="block">
          <div class="field">
            <label for="name" class="label">Enter Name</label>
            <div class="control">
              <input
                id="code_input"
                name="name"
                class="input"
                type="text"
                autocomplete="off"
                bind:value={game.nickname}
              />
            </div>
          </div>
          <button class="blue" on:click|preventDefault={join_game}>Play</button>
        </form>
      {/if}
      {#if !entered_code}
        <form class="block">
          <div class="field">
            <label for="code" class="label">Enter Game Code</label>
            <div class="control">
              <input
                on:focusin={focus_input}
                on:focusout={unfocus_input}
                id="code_input"
                name="code"
                class="input"
                type="text"
                pattern="\d*"
                autocomplete="off"
                maxlength="4"
                bind:value={game.game_id}
              />
            </div>
          </div>
          <button on:click|preventDefault={handleCodeInput}>Join</button>
        </form>
        {#if show_footer}
          <footer bind:this={footer} transition:slide>
            <div class="footer-container">
              <div class="footer-element">
                <small>Made by Team WebSockets for FullyHacks '23</small>
              </div>
              <div class="footer-element footer-center">
                <a href="/host">Create a Quiz</a>
              </div>
              <div class="footer-element">
                <small />
              </div>
            </div>
          </footer>
        {/if}
      {/if}
    </div>
  {/if}
  {#if error.length > 0}
    <h1>{error}</h1>
    <button on:click={tryAgain}>Try Again</button>
  {/if}

  {#if game.state == "LOBBY"}
    <h1>Waiting for game to start...</h1>
  {/if}

  {#if game.state == "COUNTDOWN"}
    <h1>
      {game.countdown}
    </h1>
  {/if}

  {#if game.choice}
    <h1>Answer Submitted...</h1>
    <h4>You Chose: {game.choice}</h4>
  {/if}

  {#if game.question && !game.choice}
    <div class="question-text">{game.question.text}</div>
    <div id="answer_choices">
      {#each game.question.choices as choice, i}
        {#if choice.value != "None"}
          <div
            class="choice {colors[i]}"
            on:click={() => answer(choice.choice)}
          >
            {choice.value}
          </div>
        {/if}
      {/each}
    </div>
  {/if}

  {#if game.answer}
    <h1>
      {game.answer}
    </h1>
    <h3>{game.answer_text}</h3>
  {/if}
  {#if game.action != "PING"}
    <h4 id="nickname">{game.nickname ? game.nickname : ""}</h4>
  {/if}
  {#if game.state == "GAMEOVER"}
    <h2>Game Over!</h2>
    <div class="block">
      <h2>Leaderboard</h2>
    </div>
    <table class="table">
      <tbody class="tbody">
        {#each game.leaderboard as player, i}
          {#if player.nickname != "host"}
            <tr>
              <td
                >{medals.charAt(i * 2) +
                  medals.charAt(i * 2 + 1)}{player.nickname}</td
              >

              <td>{player.score}</td>
            </tr>
          {/if}
        {/each}
      </tbody>
    </table>
  {/if}
</div>

<style>
  #answer_choices {
    display: grid;
    grid-template-columns: 1fr 1fr;
    place-items: center;
    padding: 0;
  }

  @media (min-width: 851px) {
    .question-text {
      font-size: 2.45rem;
      position: fixed;
      top: 1%;
      text-align: center;
    }
    .choice {
      min-width: 15vw;
      aspect-ratio: 1;
      margin: 2px;
      border-radius: 5%;
      border: 5px solid black;
      font-size: 2.5rem;
    }

    #answer_choices {
      margin-top: 9vh;
    }
  }

  .choice {
    cursor: pointer;
    margin-top: 1.2vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  @media (max-width: 850px) {
    .question-text {
      font-size: 1.25rem;
      margin-bottom: 3vh;
      position: fixed;
      width: 100%;
      top: 5%;
    }

    .choice {
      width: 100%;
      height: 100%;
      margin: 2px;
      border: 3px solid black;
      border-radius: 5px;
      min-height: 18vh;
    }

    #answer_choices {
      min-width: 98vw;
    }
  }

  footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100vw;
  }

  small {
    font-size: 0.6em;
  }

  .footer-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin: 0 auto;
  }

  .footer-element {
    flex: 1;
    text-align: center;
  }

  .footer-center {
    text-align: center;
  }

  button {
    border: 4px solid black;
    background-color: white;
    /* margin: auto 2rem; */
  }

  .connection {
    font-size: 1em;
    position: absolute;
    top: 0%;
    left: 0%;
  }

  .blue {
    background-color: #78a1ff;
  }

  .red {
    background-color: #ff4949;
  }

  .yellow {
    background-color: #ffff33;
  }

  .green {
    background-color: #57ff84;
  }

  @media (max-width: 850px) {
    #main {
      margin-top: 15vh;
    }
  }

  #nickname {
    position: fixed;
    bottom: 1%;
    left: 50%;
    transform: translateX(-50%);
  }

  #main {
    top: 0;
    min-height: 90vh;
    min-width: 25vw;
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
</style>
