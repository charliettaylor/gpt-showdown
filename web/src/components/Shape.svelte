<script>
  export let shape;
</script>

<div class="cartoon {shape}" />

<style>
  .cartoon {
    position: relative;
    border: 4% solid black;
    border-radius: 5%;
    filter: opacity(0.9);
  }

  .square {
    left: 290px;
    top: 230px;
    width: 2em;
    height: 2em;
    animation: rotate 20s linear infinite;
    background-color: #78a1ff;
  }

  .diamond {
    left: 70px;
    top: -20px;
    width: 2em;
    height: 2em;
    aspect-ratio: 1;
    animation: zoom 10s linear infinite;
    transform: rotate(45deg);
    background-color: #ff4949;
  }

  .line {
    left: 60%;
    top: 75%;
    width: 8em;
    height: 2em;
    animation: rotate_fast 10s ease-in-out infinite;
    background-color: #57ff84;
  }

  .circle {
    left: 15px;
    top: 320px;
    width: 2em;
    height: 2em;
    border-radius: 50%;
    animation: float 5s ease-in-out infinite;
    background-color: #ffff33;
  }
</style>
