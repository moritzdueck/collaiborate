<template>
  <div class="all">
    <div class="outer-group">
      <div style="width: 100%; margin-bottom: 10px" :class="'layer input ' + (active===0? 'active' : '')" @click="setLayer(0)">Input</div>
    </div>
    <div class="network">
      <div class="layer-group">
        <div :class="'layer convolution ' + (active===1? 'active' : '')" @click="setLayer(1)">Convolution</div>
        <div :class="'layer relu ' + (active===2? 'active' : '')" @click="setLayer(2)">ReLU</div>
        <div :class="'layer max-pooling ' + (active===3? 'active' : '')" @click="setLayer(3)">Max Pooling</div>
      </div>
      <div class="layer-group">
        <div :class="'layer convolution ' + (active===4? 'active' : '')" @click="setLayer(4)">Convolution</div>
        <div :class="'layer relu ' + (active===5? 'active' : '')" @click="setLayer(5)">ReLU</div>
        <div :class="'layer max-pooling ' + (active===6? 'active' : '')" @click="setLayer(6)">Max Pooling</div>
      </div>
      <div class="layer-group">
        <div :class="'layer convolution ' + (active===7? 'active' : '')" @click="setLayer(7)">Convolution</div>
        <div :class="'layer relu ' + (active===8? 'active' : '')" @click="setLayer(8)">ReLU</div>
        <div :class="'layer max-pooling ' + (active===9? 'active' : '')" @click="setLayer(9)">Max Pooling</div>
      </div>
      <div class="layer-group">
        <div :class="'layer flatten ' + (active===10? 'active' : '')" @click="setLayer(10)">Flatten</div>
        <div :class="'layer linear ' + (active===11? 'active' : '')" @click="setLayer(11)">Linear</div>
        <div :class="'layer relu ' + (active===12? 'active' : '')" @click="setLayer(12)">ReLU</div>
        <div :class="'layer linear ' + (active===13? 'active' : '')" @click="setLayer(13)">Linear</div>
      </div>
    </div>
  </div>

</template>

<script setup>

import {onMounted, ref} from "vue";

const active = ref(0)
const emit = defineEmits(['selectedLayer'])
const props = defineProps(['initialLayer'])

const setLayer = (layer) => {
  active.value = layer
  emit("selectedLayer", layer)
}

onMounted(() => {
  setLayer(props.initialLayer)
})

</script>
<style scoped>

.all{
  display: flex;
  flex-direction: column;
}

.outer-group {
  width: 100%;
}

.network {
  width: 100%;
  border-radius: 10px;
  padding: 1px;
  flex-grow: 1;
}

.layer-group {
  margin-top: 20px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

</style>