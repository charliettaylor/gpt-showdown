<script>
  import { onMount } from "svelte";
  import Shape from "./Shape.svelte";

  let entered_name = false;

  let ws;

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
    game.action = "JOIN";
    game.game_id = "" + game.game_id;
    ws.send(JSON.stringify(game));
  };

  onMount(() => {
    ws = new WebSocket("ws://localhost:8000/ws");

    ws.addEventListener("message", (e) => {
      const msg = JSON.parse(e.data);
      console.log(msg);
      game = msg;
    });
  });
</script>

<div>
  {#if game.state == "NOT_CREATED"}
    <div id="main">
      <Shape shape="circle" />
      <Shape shape="line" />
      <Shape shape="diamond" />
      <Shape shape="square" />
      <div class="block">
        <h1>GPT Showdown</h1>
      </div>
      {#if !entered_name}
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
          <button on:click|preventDefault={() => (entered_name = true)}
            >Submit</button
          >
        </form>
      {/if}
      {#if entered_name}
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
          <button on:click|preventDefault={join_game}>Join</button>
        </form>
      {/if}
    </div>
  {/if}

  {#if game.state == "LOBBY"}
    <h1>Waiting for game to start...</h1>
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
      <button on:click={() => answer(choice.choice)}>{choice.value}</button>
    {/each}
  {/if}

  {#if game.answer}
    <h1>
      {game.answer}
    </h1>
  {/if}

  {#if game.leaderboard}
    <h1>
      {game.question.text}
    </h1>
    {#each game.leaderboard as player}
      <h3>{player.nickname}: {player.score}</h3>
    {/each}
  {/if}
</div>

<style>
  button {
    background-color: #333;
  }

  #main {
    top: 0;
    min-height: 90vh;
  }
</style>
