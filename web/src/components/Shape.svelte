<script>
  export let shape;
</script>

<div class="cartoon {shape}" />

<style>
  .cartoon {
    position: absolute;
    left: 150px;
    top: 200px;
    border: 4px solid black;
    border-radius: 5px;
  }

  .square {
    width: 50px;
    height: 50px;
    animation: rotate 20s linear infinite;
    background-color: #78a1ff;
  }

  .diamond {
    left: 100px;
    top: 600px;
    width: 50px;
    height: 50px;
    animation: zoom 10s linear infinite;
    transform: rotate(45deg);
    background-color: #ff4949;
  }

  .line {
    left: 100px;
    top: 100px;
    width: 100px;
    height: 25px;
    animation: rotate_fast 10s ease-in-out infinite;
    background-color: #57ff84;
  }

  .circle {
    left: 200px;
    top: 600px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    animation: float 5s ease-in-out infinite;
    background-color: #ffff33;
  }
</style>
