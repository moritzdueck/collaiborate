<template>
  <div class="all">
    <div class="outer-group">
      <div style="width: 100%; margin-bottom: 10px" :class="'layer passive-gray input ' + (active===0? 'active' : '')" @click="setLayer(0)">Input</div>
    </div>
    <div class="network">
      <div class="layer-group">
        <div :class="'layer passive-gray convolution ' + (active===1? 'active' : '')" @click="setLayer(1)">Convolution</div>
        <div :class="'layer passive-gray relu ' + (active===2? 'active' : '')" @click="setLayer(2)">ReLU</div>
        <div :class="'layer passive-gray max-pooling ' + (active===3? 'active' : '')" @click="setLayer(3)">Max Pooling</div>
      </div>
      <div class="layer-group">
        <div :class="'layer passive-gray convolution ' + (active===4? 'active' : '')" @click="setLayer(4)">Convolution</div>
        <div :class="'layer passive-gray relu ' + (active===5? 'active' : '')" @click="setLayer(5)">ReLU</div>
        <div :class="'layer passive-gray max-pooling ' + (active===6? 'active' : '')" @click="setLayer(6)">Max Pooling</div>
      </div>
      <div class="layer-group">
        <div :class="'layer passive-gray convolution ' + (active===7? 'active' : '')" @click="setLayer(7)">Convolution</div>
        <div :class="'layer passive-gray relu ' + (active===8? 'active' : '')" @click="setLayer(8)">ReLU</div>
        <div :class="'layer passive-gray max-pooling ' + (active===9? 'active' : '')" @click="setLayer(9)">Max Pooling</div>
      </div>
      <div class="layer-group">
        <div :class="'layer passive-gray flatten ' + (active===10? 'active' : '')" @click="setLayer(10)">Flatten</div>
        <div :class="'layer passive-gray linear ' + (active===11? 'active' : '')" @click="setLayer(11)">Linear</div>
        <div :class="'layer passive-gray relu ' + (active===12? 'active' : '')" @click="setLayer(12)">ReLU</div>
        <div :class="'layer passive-gray linear ' + (active===13? 'active' : '')" @click="setLayer(13)">Linear</div>
      </div>
    </div>
    <p style="text-align: center; font-weight: bold">CNN</p>
  </div>

</template>

<script setup>

import {onMounted, ref, watch} from "vue";

const active = ref(0)
const emit = defineEmits(['selectedLayer'])
const props = defineProps(['initialLayer', 'controlled', 'locked'])

const setLayer = (layer) => {
  if(props.locked)
    return

  active.value = layer
  emit("selectedLayer", layer)
}

onMounted(() => {
  setLayer(props.initialLayer)

  if(props.controlled){
    watch(() => props.initialLayer, l => active.value = l);
  }
})

</script>
<style scoped>

.all{
  --network-background: var(--gray);

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
  border: 3px solid var(--gray);

  background-color: #ffffff;
  opacity: 1;
  background-size: 13px 13px;
  background-image:  repeating-linear-gradient(to right, var(--network-background), var(--network-background) 0.65px, #ffffff 0.65px, #ffffff);
}

.layer-group {
  margin-top: 20px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

</style>