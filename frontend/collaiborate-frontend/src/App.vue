<script setup lang="ts">
import Explorer from './components/demo/Explorer.vue'
import ScrollamaStory from "./components/story/Story.vue";
import {onMounted, ref, shallowRef} from "vue";
import LocalView from "./components/shared/LocalView.vue";
import PageTooSmallNotice from "./components/PageTooSmallNotice.vue";
import {breakpointsTailwind, useBreakpoints} from '@vueuse/core'

const allImages = shallowRef()
const lines = shallowRef()

const explorerIndex = ref(undefined as undefined | number)
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

const updateExplorerIndex = (index: number) => explorerIndex.value = index;


const props = defineProps(["allImages"])
const breakpoints = useBreakpoints(breakpointsTailwind)
const smallerThanLg = breakpoints.smaller('lg');

</script>

<template>
  <PageTooSmallNotice v-if="smallerThanLg"/>
  <ScrollamaStory :all-images="allImages" :lines="lines" v-if="stage === 'story' && !smallerThanLg"
                  v-on:show-demo="stage='demo'"/>
  <Explorer v-if="stage === 'demo' && !explorerIndex && !smallerThanLg" v-on:index="updateExplorerIndex"
            v-on:story="stage='story'"/>
  <LocalView v-if="stage === 'demo' && explorerIndex && !smallerThanLg" :lines="lines" :index="explorerIndex"
             :all-images="allImages"
             v-on:update-index="updateExplorerIndex"/>
</template>

<style scoped>

</style>

<style>
:root {
  --blue: #7EB0D5;
  --blue-transparent: #7EB0D6B2;
  --teal: #8BD3C7;
  --green: #B2E061;
  --green-transparent: #B2E061B2;
  --purple: #BD7EBE;
  --lavender: #BEB9DB;
  --red: #FC7F6F;
  --red-transparent: #FC7F6FB2;
  --rose: #FDCCE5;
  --orange: #FFB55A;
  --yellow: #FFEE65;
  --gray: #EFEFEF;
  --gray-transparent: #EFEFEFB2;
}

/*  Navive UI*/

.p-slider .p-slider-range {
  background: var(--blue) !important;
}

.p-slider .p-slider-handle {
  border: 2px solid var(--blue) !important;
}

.p-slider:not(.p-disabled) .p-slider-handle:hover {
  background: var(--blue) !important;
  border-color: var(--blue) !important;
}

</style>