<template>
  <div style="width: 100%; height: 100%; overflow: hidden; position: relative">
    <div style="position: absolute; top: 5px; left: 20px">
      <p>
        <span style="width: 20px; height: 20px; border: 3px solid var(--blue); display: inline-block; vertical-align: middle; background-color: var(--blue-transparent);"></span>
        Sketches from the same class</p>
      <p>
        <span style="width: 20px; height: 20px; border: 3px solid var(--gray); display: inline-block; vertical-align: middle; background-color: var(--gray-transparent);"></span>
        Sketches from another class
      </p>
    </div>

    <div style="position: absolute; height:20px; bottom: 80px; display: flex; align-items: center; justify-content: center; width:100%">
      <p>
        Distance
      </p>
    </div>

    <img :src="'/distancesImg/'+sample+'-layer'+layer+'.svg'" style="width: 100%; height: 90%; max-width: 100%; max-height: 90%;"/>
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