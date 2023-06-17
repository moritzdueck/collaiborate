<template>
  <div style="overflow: hidden; position: relative; height: 100vh">

    <div ref="n1" id="n1"
         :style="{width: '220px', height:'220px', position: 'absolute', cursor: 'grab'}">
      <SimpleNeighborhood v-if="allImages"
                          :transition-duration="100"
                          :allImages="allImages" index="146028" :num-samples="70" :img-size="15"
                          color="var(--red)" :referenceLayer="layer1" :comparison-layer="0"/>
    </div>

    <div ref="n2" id="n2"
         :style="{width: '600px', height:'600px', position: 'absolute', cursor: 'grab'}">
      <SimpleNeighborhood v-if="allImages"
                          :transition-duration="100"
                          :allImages="allImages" index="271551" :num-samples="samples" :img-size="25"
                          color="var(--yellow)" :referenceLayer="layer2" :comparison-layer="0"/>
    </div>

    <div ref="n3" id="n3"
         :style="{width: '150px', position: 'absolute', cursor: 'grab'}">
      <SimpleNeighborhood v-if="allImages"
                          :transition-duration="100"
                          :allImages="allImages" index="101647" :num-samples="50" :img-size="15"
                          color="var(--blue)" :referenceLayer="layer3" :comparison-layer="0"/>
    </div>

    <div :style="{width: '150px', position: 'absolute', right: '100px', bottom: '80px'}">
      <span class="jump-section" @click="$emit('showDemo')">
        Jump to Explorer
      <img class="right" src="/arrow_right.svg">
      </span>
    </div>

    <div class="text-wrapper">
      <h1 style="word-wrap: break-word;">Neighbor&shy;hoods Explored</h1>
      <p style="font-size: 20px">A Journey into CNNs for Sketch Classification</p>
      <p style="text-align: justify;">Convolutional Neural Networks (CNNs) have transformed image classification. But
        the inner workings of these networks trained on datasets like QuickDraw remain hard to understand for humans. In
        this interactive article, we explore the importance of neighbourhoods of samples in CNNs, building some
        intuition on what these networks learn by observing how they transform space. Join us as we dive into the topic
        and explore for yourself.</p>
    </div>


  </div>


</template>

<script setup>
import {onMounted, onUnmounted, ref} from "vue";
import SimpleNeighborhood from "./reusables/SimpleNeighborhood.vue";

const props = defineProps(["allImages"])

defineEmits({
  showDemo: () => true
})

const n1 = ref(null)
const n2 = ref(null)
const n3 = ref(null)

const samples = ref(100)
const layer1 = ref(0)
const layer2 = ref(0)
const layer3 = ref(0)

const position = ref([
  [0, 0],
  [0, 0],
  [0, 0],
])

let lastScrollY = window.scrollY
const handleScroll = () => {
  n1.value.style.top = (n1.value.offsetTop - (lastScrollY - window.scrollY) * 0.3) + "px"
  n2.value.style.top = (n2.value.offsetTop - (lastScrollY - window.scrollY) * 0.2) + "px"
  n3.value.style.top = (n3.value.offsetTop - (lastScrollY - window.scrollY) * 0.4) + "px"

  lastScrollY = window.scrollY
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  dragElement(n1.value, undefined, layer1)
  dragElement(n2.value, undefined, layer2)
  dragElement(n3.value, undefined, layer3)

  n1.value.style.left = window.innerWidth * 0.1 + "px"
  n1.value.style.top = window.innerHeight * 0.4 + "px"
  layer1.value = Math.max(0, Math.min(Math.floor(((n1.value.offsetLeft + n1.value.clientWidth / 2) / window.innerWidth) * 13), 13))

  n2.value.style.left = window.innerWidth * 0.3 + "px"
  n2.value.style.top = window.innerHeight * 0.5 + "px"
  layer2.value = Math.max(0, Math.min(Math.floor(((n2.value.offsetLeft + n2.value.clientWidth / 2) / window.innerWidth) * 13), 13))

  n3.value.style.left = window.innerWidth * 0.7 + "px"
  n3.value.style.top = window.innerHeight * 0.3 + "px"
  layer3.value = Math.max(0, Math.min(Math.floor(((n3.value.offsetLeft + n3.value.clientWidth / 2) / window.innerWidth) * 13), 13))


})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
})


function dragElement(elmnt, count, layer) {
  let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

  elmnt.onmousedown = dragMouseDown;

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";

    if (count) {
      count.value = ((elmnt.offsetTop + elmnt.clientHeight) / window.innerHeight) * 200
    }

    if (layer) {
      layer.value = Math.max(0, Math.min(Math.floor(((elmnt.offsetLeft + elmnt.clientWidth / 2) / window.innerWidth) * 13), 13))
    }
  }

  function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
  }
}


</script>

<style scoped>
.text-wrapper {
  max-width: 900px;
  padding-left: 50px;
  padding-right: 50px;
}
</style>