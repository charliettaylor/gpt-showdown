<script>
  let questions = [];
  let text = "";
  let choice1 = "";
  let choice2 = "";
  let choice3 = "";
  let choice4 = "";
  let answer;
  let title;
  let category;

  let question_type = "Multiple Choice";
  let types = [];
  let bottom_of_questions;

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  let answer_select;

  function go_back() {
    dispatch("quizzes", {
      state: "quizzes",
    });
  }

  const remove_question = (idx) => {
    questions = [...questions.slice(0, idx), ...questions.slice(idx + 1)];
  };

  const reset_form = () => {
    choice1 = "";
    choice2 = "";
    choice3 = "";
    choice4 = "";
    answer = "";
    text = "";
    // const last_question_dom = dom_questions[dom_questions.length - 1];
    console.log(bottom_of_questions);
    bottom_of_questions.scrollIntoView({
      behavior: "smooth",
      block: "center",
      inline: "center",
    });
  };

  const add_question = () => {
    const choices = [];
    types.push(question_type);
    let actual_answer = answer_select.value;

    if (question_type == "Multiple Choice") {
      choices.push(
        { choice: "A", value: choice1 },
        { choice: "B", value: choice2 },
        { choice: "C", value: choice3 },
        { choice: "D", value: choice4 }
      );
      answer = actual_answer;
    } else if (question_type == "True/False") {
      choices.push(
        { choice: "A", value: "True" },
        { choice: "B", value: "False" }
      );
      answer = actual_answer == "True" ? "A" : "B";
    } else {
      console.error("Unknown Question type: ", question_type);
      return;
    }

    questions.push({
      question: text,
      choices: choices,
      answer: answer,
    });
    questions = questions;
    reset_form();
  };

  const create_quiz = () => {
    const url = "https://gptquiz.xyz/api/quiz";
    // const url = "http://localhost:5005/quiz";
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: title,
        category: category,
        questions: questions,
      }),
    });
    setTimeout(() => {
      go_back();
    }, 1000);
  };
</script>

<div id="main" class="block">
  <div style="margin-bot: 2vh;">
    <h1>Create a Quiz</h1>
  </div>
  <form class="form box">
    <div class="field">
      <label for="title" class="label">Title</label>
      <input
        bind:value={title}
        name="title"
        class="input"
        placeholder="Title"
      />
    </div>
    <div class="field">
      <label for="category" class="label">Category</label>
      <input
        bind:value={category}
        name="category"
        class="input"
        placeholder="Category"
      />
    </div>
  </form>
  <div class="block">
    {#each questions as question, i}
      <div class="box">
        <b>{question.question}</b>
        {#if types[i] == "Multiple Choice"}
          <ul>
            <li>A: {question.choices[0].value}</li>
            <li>B: {question.choices[1].value}</li>
            <li>C: {question.choices[2].value}</li>
            <li>D: {question.choices[3].value}</li>
          </ul>
          <span>Answer: {question.answer}</span>
        {/if}
        {#if types[i] == "True/False"}
          <ul>
            <li>True</li>
            <li>False</li>
          </ul>
          <span>Answer: {question.answer == "A" ? "True" : "False"}</span>
        {/if}
        <div
          on:click={() => {
            remove_question(i);
          }}
          class="delete-question"
        >
          ❌
        </div>
      </div>
    {/each}
    <div class="bottom-of-questions" bind:this={bottom_of_questions} />
  </div>
  <form class="form box">
    <div class="field">
      <label for="text" class="label">Question</label>
      <textarea
        bind:value={text}
        name="text"
        class="textarea"
        placeholder="What is 2+2?"
      />
    </div>
    <div class="field">
      <label for="ismc" class="label">Question Type</label>
      <select bind:value={question_type} id="ismc" name="ismc">
        <option value="Multiple Choice">Multiple Choice </option>
        <option value="True/False"> True/False </option>
      </select>
    </div>
    {#if question_type == "Multiple Choice"}
      <div class="field">
        <label for="choice1" class="label">A</label>
        <input
          bind:value={choice1}
          name="choice1"
          class="input"
          placeholder="4"
        />
      </div>
      <div class="field">
        <label for="choice2" class="label">B</label>
        <input
          bind:value={choice2}
          name="choice2"
          class="input"
          placeholder="5"
        />
      </div>
      <div class="field">
        <label for="choice3" class="label">C</label>
        <input
          bind:value={choice3}
          name="choice3"
          class="input"
          placeholder="6"
        />
      </div>
      <div class="field">
        <label for="choice4" class="label">D</label>
        <input
          bind:value={choice4}
          name="choice4"
          class="input"
          placeholder="7"
        />
      </div>
    {/if}
    <div class="field">
      <label for="answer" class="label">Answer</label>
      <div class="select">
        <select bind:this={answer_select} name="answer">
          {#if question_type == "Multiple Choice"}
            <option selected>A</option>
            <option>B</option>
            <option>C</option>
            <option>D</option>
          {/if}
          {#if question_type == "True/False"}
            <option selected>True</option>
            <option>False</option>
          {/if}
        </select>
      </div>
    </div>
    {#if question_type == "Multiple Choice"}
      <button
        disabled={!choice1 || !choice2 || !choice3 || !choice4 || !text}
        class="button"
        on:click|preventDefault={add_question}>Add Question</button
      >
    {/if}
    {#if question_type == "True/False"}
      <button
        disabled={!text}
        class="button"
        on:click|preventDefault={add_question}>Add Question</button
      >
    {/if}
  </form>
  <button
    disabled={!title || !category || questions.length < 1}
    class="button"
    on:click|preventDefault={create_quiz}>Create Quiz</button
  >
</div>

<style>
  #main {
    min-width: 50vw;
  }

  @media (max-width: 850px) {
    #main {
      /* min-width: 50vw; */
    }
  }

  .delete-question {
    position: absolute;
    right: 0;
    top: 0;
    text-align: center;
    opacity: 0.5;
    cursor: pointer;
    /* background-color: red; */
  }

  .delete-question:hover {
    opacity: 0.9;
  }

  .box {
    position: relative;
  }
</style>
