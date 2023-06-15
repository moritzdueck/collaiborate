<template>
  <div class="distance-story-container">
    <div>
      <Distances :layer="layer" :sample="sample"/>
    </div>
    <div>
      <div>
        <CnnLayers :style="{visibility: showControls? 'visible' : 'hidden'}" class="layer-selection" :initial-layer="layer"
                   v-on:selected-layer="l => layer = l"/>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">

import {onBeforeMount, onMounted, ref} from "vue";
import Distances from "./Distances.vue";
import CnnLayers from "../../reusables/CnnLayers.vue";

const props = defineProps({
  sample: Number,
  initialLayer: Number,
  showControls: Boolean,
})

const layer = ref(0)

onBeforeMount(() => {
  layer.value = props.initialLayer || 0
})

</script>

<style scoped>
.distance-story-container {
  display: flex;
  width: 100%;
}

.distance-story-container > * {
  flex-grow: 1;
}

.layer-selection {
  width: 105px;
  max-width: 105px;
}
</style>