<template>
  <div class="layer-dropdown" @click="showOptions = !showOptions">
    <div style="margin: -5px;" :class="'layer '+modelValue.type">{{ modelValue.label }}</div>
    <div v-if="showOptions" class="options">
      <div class="flex align-items-center" v-for="layer of layers" @click.stop="showOptions = false; modelValue = layer; $emit('update:modelValue', layer);">
        <div :class="'layer '+layer.type">{{ layer.label }}</div>
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">
import {ref} from "vue";
import {layers} from "../../utils/utils";

const props = defineProps(["modelValue"])
const emit = defineEmits(['update:modelValue'])

const showOptions = ref(false)
</script>

<style scoped>

.layer-dropdown{
  display: inline;
  position: relative;
  align-items: center;
}

.options{
  position: absolute;
  left: 0;
  width: 150px;
  min-height: 10px;
  max-height: 200px;
  overflow: auto;
  background-color: white;
  box-shadow: 3px 5px 7px 0px #d4d4d469;
  border: 1px solid var(--gray);
}
</style>