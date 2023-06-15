<script setup lang="ts">
import Explorer from './components/demo/Explorer.vue'
import ScrollamaStory from "./components/story/Story.vue";
import {onMounted, ref, shallowRef} from "vue";

const allImages = shallowRef()
const lines = shallowRef()

const stage = ref('story' as 'story' | 'demo')
const apiUrl = import.meta.env.VITE_APIURL

onMounted(() => {
  fetch(apiUrl + "all")
      .then(res => res.json())
      .then(d => {
        allImages.value = d
      })

  fetch(apiUrl + 'lines')
      .then(res => res.json())
      .then(d => {
        lines.value = d
      })
})

</script>

<template>
  <ScrollamaStory :all-images="allImages" :lines="lines"/>
  <Explorer v-if="stage === 'demo'"/>
</template>

<style scoped>

</style>

<style>
:root {
  --blue: #7EB0D5;
  --blue-transparent: #7EB0D6B2;
  --teal: #8BD3C7;
  --green: #B2E061;
  --purple: #BD7EBE;
  --lavender: #BEB9DB;
  --red: #FC7F6F;
  --rose: #FDCCE5;
  --orange: #FFB55A;
  --yellow: #FFEE65;
  --gray: #EFEFEF;
  --gray-transparent: #EFEFEFB2;
}
</style>