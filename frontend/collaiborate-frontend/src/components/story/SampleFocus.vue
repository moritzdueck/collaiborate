<template>
  <div class="sample-focus-container">
    <span>
      <img v-if="allImages" :src="'data:image/png;base64, ' + allImages[sample]" alt=""/>
    </span>
    <div class="box">
      <slot></slot>
    </div>
  </div>


</template>

<script setup lang="ts">
const props = defineProps(['sample', 'allImages'])
</script>

<style scoped>

.sample-focus-container {
  position: relative;
}

span {
  border: 2px solid var(--red);
  border-radius: 100px;
  width: 35px;
  height: 35px;
  display: inline-flex;
  justify-content: center;
  align-items: center;


  position: absolute;
  top: -15px;
  left: -10px;
  background-color: white;
}

img {
  width: 40px;
}

.box {
  border: 2px solid var(--red);
  border-radius: 5px;
  padding: 15px;
}
</style>