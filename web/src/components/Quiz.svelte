<script>
  import { onMount } from "svelte";

  export let quiz;
  let questions = [];
  let show_questions = false;

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  const fetch_questions = async () => {
    // const url = `http://localhost:5005/get_questions?quiz_id=${quiz.id}`;
    const url = `https://gptquiz.xyz/api/get_questions?quiz_id=${quiz.id}`;
    const res = await fetch(url);
    questions = await res.json();
    let cleaned_questions = [];
    for (let i = 0; i < questions.length; ++i) {
      let question = questions[i];
      let question_text = question.question.replace(/\d+\.\w*/, "");
      question.question = question_text;
      cleaned_questions.push(question);
    }
    questions = cleaned_questions;
  };

  function select_quiz() {
    show_questions = true;
    setTimeout(() => {
      can_close_modal = true;
    }, 200);
  }

  const start_quiz = () => {
    dispatch("select_quiz", {
      quiz: quiz,
    });
  };

  let modal_content;
  let can_close_modal = false;

  const close_modal = () => {
    show_questions = false;
    can_close_modal = false;
  };

  onMount(() => {
    fetch_questions();
    document.addEventListener("click", function (event) {
      if (!modal_content) return;
      // Check if the click target is outside of the modal container
      if (!modal_content.contains(event.target) && can_close_modal) {
        close_modal();
      }
    });
  });
</script>

{#if !show_questions}
  <div class="block">
    <button on:click={select_quiz} class="box">
      <h3>{quiz.name}</h3>
      <p>{quiz.category}</p>
      <small>Questions: {quiz.num_questions}</small>
      <!-- <small>{quiz.id}</small> -->
    </button>
    <div on:click={start_quiz} class="start-shortcut" style="color: green;">
      ▶
    </div>
  </div>
{/if}

{#if show_questions}
  <div class="popup">
    <div bind:this={modal_content} class="popup-content">
      <h3 style="font-size: 80px;">Questions</h3>
      {#each questions as question, i}
        <small>{i + 1}. {question.question}</small>
        <br />
      {/each}
      <button on:click={start_quiz}>Start Quiz</button>
    </div>
  </div>
{/if}

<style>
  .popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(
      0,
      0,
      0,
      0.5
    ); /* Use rgba for background with transparency */
    backdrop-filter: blur(5px); /* Use backdrop-filter to apply blur effect */
    justify-content: center;
    align-items: center;
    z-index: 9999; /* Set a higher z-index to ensure modal appears on top of other content */
  }

  @media (max-width: 850px) {
    .popup-content {
      font-size: 11px !important;
    }
  }

  .popup-content {
    position: fixed;
    top: 10%;
    line-height: 3rem;
    font-size: 40px;
    left: 10%;
    width: 80%;
    min-height: 80%;
    border: 2px solid #333;
    border-radius: 10px;
    background-color: rgba(244, 244, 244, 0.9);
  }

  button {
    min-width: 50vw;
  }

  .block {
    position: relative;
    max-width: 70vw;
    transition: all 0.2s cubic-bezier(0.86, 0, 0.07, 1);
  }

  .block:hover {
    transform: scale(1.08);
  }

  small {
    color: rgba(55, 55, 55, 0.8);
  }

  @media (max-width: 850px) {
    .block {
      font-size: 0.5em;
    }
    p {
      font-size: 1.8em;
    }
    small {
      font-size: 1.8em;
    }
  }

  .start-shortcut {
    position: absolute;
    top: 1%;
    right: 1%;
    cursor: pointer;
  }

  .start-shortcut:hover {
    transform: scale(1.2);
  }
</style>
