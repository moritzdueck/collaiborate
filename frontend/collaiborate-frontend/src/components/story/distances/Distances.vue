<template>
  <div style="width: 100%; position: relative">
    <div style="position: absolute; top: 5px">
      <p>
        <span style="width: 20px; height: 20px; border: 3px solid var(--blue); display: inline-block; vertical-align: middle; background-color: var(--blue-transparent);"></span>
        Sketches from the same class</p>
      <p>
        <span style="width: 20px; height: 20px; border: 3px solid var(--gray); display: inline-block; vertical-align: middle; background-color: var(--gray-transparent);"></span>
        Sketches from another class
      </p>
    </div>

    <div style="position: absolute; height:20px; bottom: 0; display: flex; align-items: center; justify-content: center; width:100%">
      <p>
        Distance
      </p>
    </div>

    <img :src="'src/assets/distances/'+sample+'-layer'+layer+'.svg'" style="width: 100%;"/>
  </div>
</template>

<script setup lang="ts">

const props = defineProps({
  sample: Number,
  layer: Number
})

</script>

<style scoped>

</style>