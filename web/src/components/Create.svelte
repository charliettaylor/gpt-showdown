<script>
  let questions = [];
  let text;
  let choice1;
  let choice2;
  let choice3;
  let choice4;
  let answer;
  let title;
  let category;

  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  function go_back() {
    dispatch("quizzes", {
      state: "quizzes",
    });
  }

  const add_question = () => {
    questions.push({
      question: text,
      choices: [
        { choice: "A", value: choice1 },
        { choice: "B", value: choice2 },
        { choice: "C", value: choice3 },
        { choice: "D", value: choice4 },
      ],
      answer: answer,
    });
    questions = questions;
  };

  const create_quiz = () => {
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
  <div class="section">
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
    {#each questions as question}
      <div class="box">
        <b>{question.question}</b>
        <ul>
          <li>A: {question.choices[0].value}</li>
          <li>B: {question.choices[1].value}</li>
          <li>C: {question.choices[2].value}</li>
          <li>D: {question.choices[3].value}</li>
        </ul>
        <span>Answer: {question.answer}</span>
      </div>
    {/each}
  </div>
  <form class="form box">
    <div class="field">
      <label for="text" class="label">Question</label>
      <textarea
        bind:value={text}
        name="text"
        class="textarea"
        placeholder="Can pigs fly?"
      />
    </div>
    <div class="field">
      <label for="choice1" class="label">A</label>
      <input bind:value={choice1} name="choice1" class="input" />
    </div>
    <div class="field">
      <label for="choice2" class="label">B</label>
      <input bind:value={choice2} name="choice2" class="input" />
    </div>
    <div class="field">
      <label for="choice3" class="label">C</label>
      <input bind:value={choice3} name="choice3" class="input" />
    </div>
    <div class="field">
      <label for="choice4" class="label">D</label>
      <input bind:value={choice4} name="choice4" class="input" />
    </div>
    <div class="field">
      <label for="answer" class="label">Answer</label>
      <div class="select">
        <select bind:value={answer} name="answer">
          <option selected>A</option>
          <option>B</option>
          <option>C</option>
          <option>D</option>
        </select>
      </div>
    </div>
    <button class="button" on:click|preventDefault={add_question}
      >Add Question</button
    >
  </form>
  <button class="button" on:click|preventDefault={create_quiz}
    >Create Quiz</button
  >
</div>

<style>
  #main {
    min-width: 50vw;
  }
</style>
