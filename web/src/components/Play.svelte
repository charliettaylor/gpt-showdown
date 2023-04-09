<script>
  import { onMount } from "svelte";
  import Shape from "./Shape.svelte";

  let entered_name = false;
  let entered_code = false;

  let ws;

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
  };

  let ws_open = false;
  let error = "";

  onMount(() => {
    ws = new WebSocket("ws://localhost:8000/ws");

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
        <h1>GPT Showdown</h1>
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
          <button on:click|preventDefault={join_game}>Play</button>
        </form>
      {/if}
      {#if !entered_code}
        <form class="block">
          <div class="field">
            <label for="code" class="label">Enter Game Code</label>
            <div class="control">
              <input
                id="code_input"
                name="code"
                class="input"
                type="number"
                autocomplete="off"
                bind:value={game.game_id}
              />
            </div>
          </div>
          <button on:click|preventDefault={handleCodeInput}>Join</button>
        </form>
      {/if}
    </div>
    <footer>
      <small>Create a quiz <a href="/host">here!</a></small>
    </footer>
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
  {/if}

  {#if game.question && !game.choice}
    <div id="answer_choices">
      {#each game.question.choices as choice, i}
        <div class="choice">
          <button class={colors[i]} on:click={() => answer(choice.choice)}
            >{choice.value}</button
          >
        </div>
      {/each}
    </div>
  {/if}

  {#if game.answer}
    <h1>
      {game.answer}
    </h1>
  {/if}

  <!-- <div id="answer_choices"> -->
  <!--   <div class="choice"> -->
  <!--     <button>A</button> -->
  <!--   </div> -->
  <!--   <div class="choice"> -->
  <!--     <button>A</button> -->
  <!--   </div> -->

  <!--   <div class="choice"> -->
  <!--     <button>A</button> -->
  <!--   </div> -->

  <!--   <div class="choice"> -->
  <!--     <button>A</button> -->
  <!--   </div> -->
  <!-- </div> -->
</div>

<style>
  #answer_choices {
    display: grid;
    grid-template-columns: 1fr 1fr;
    place-items: center;
    padding: 0;
    background-color: red;
    width: 75vw;
  }

  @media (min-width: 851px) {
    .choice {
      min-width: 30vw;
      max-width: 40vw;
      aspect-ratio: 1;
      margin: 2px;
    }
  }

  @media (max-width: 850px) {
    #answer_choices {
      background-color: yellow;
      display: flex;
      flex-direction: column;
    }
    /* … */
    .choice {
      min-width: 100vw;
      min-height: 20vh;
      margin: 2px;
    }
  }

  .choice > button {
    width: 100%;
    height: 100%;
  }

  footer {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    padding: 0.01rem;
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

  #main {
    top: 0;
    min-height: 90vh;
  }
</style>
