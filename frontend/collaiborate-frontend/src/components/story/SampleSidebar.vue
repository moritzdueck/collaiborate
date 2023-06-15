<template>
  <div class="sample-sidebar" v-if="allImages">
    <span v-for="sample of samples" :class="modelValue === sample? 'active' : ''"
          @click="$emit('update:modelValue', sample);">
      <img class="samples__image" :src="'data:image/png;base64, ' + allImages[sample]" alt=""/>
    </span>
  </div>
</template>

<script setup lang="ts">

import {ref} from "vue";

const props = defineProps(["allImages", "modelValue"])
const emit = defineEmits(['update:modelValue'])

const samples = ref([
  110635, //car
  101647, // wine bottle
  272791, //bee
  271551, // mosquito
  185767, // pineapple where first conv reacts strongly to round shapes
  146028, // plane with two wings
  115656, //train where conv layers extract relevant features but linear layers undecided
]);

</script>

<style scoped>
.sample-sidebar {
  width: 100%;
  max-width: 600px;
  height: 70%;
  border-radius: 100px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-around;
}

.sample-sidebar > span {
  cursor: pointer;
  background-color: white;
  border-radius: 100px;
  display: inline-flex;
  width: 60px;
  height: 60px;
  align-items: center;
  justify-content: center;
}

.sample-sidebar > span:hover, .sample-sidebar > span.active {
  border: 5px solid var(--blue);
}
</style>