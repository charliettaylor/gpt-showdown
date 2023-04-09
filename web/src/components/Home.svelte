<script>
  import Shape from "./Shape.svelte";
</script>

<div>
  <Shape shape="circle" />
  <Shape shape="line" />
  <Shape shape="diamond" />
  <Shape shape="square" />
  <div class="block">
    <h1>GPT Showdown</h1>
  </div>
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
        />
      </div>
    </div>
  </form>
</div>
