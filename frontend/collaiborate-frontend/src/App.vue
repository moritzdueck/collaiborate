<script setup lang="ts">
import Explorer from './components/Explorer.vue'
import LocalView from "./components/LocalView.vue";
import {ref} from "vue";

const globalIndex = ref(271551)
// const globalIndex = ref(146028)
// const globalIndex = ref(146028)
//fun bee
//272791
// mosquito
//271551

</script>

<template>
  <Explorer v-if="!globalIndex" v-on:index="index => globalIndex=index"/>
  <LocalView v-if="globalIndex" v-on:index="index => globalIndex=index" :index="globalIndex"/>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
