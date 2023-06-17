<template>
  <div style="position: relative">
    <div style="height: 100vh; width: 100vw;">
      <LandingPage :all-images="allImages" v-on:show-demo="$emit('showDemo')"></LandingPage>
    </div>

    <div
        style="width:100%; height: 20vh; background-color: #d7d7d73d; backdrop-filter: blur(2px); display: flex; justify-content: center; align-items: end">
      <h3 style="margin-bottom: 20px">At any point, choose a different sample for the story:</h3>
    </div>

    <div
        style="position: sticky; top: 0; left: 0; padding: 10px; width: 100%; display: flex; align-items: center; justify-content: center; z-index: 999; backdrop-filter: blur(2px); background-color: #d7d7d73d;">
      <SampleSidebar :all-images="allImages" v-model="sample" v-show="displaySidebar"/>
    </div>

    <div
        style="width:100%; height: 20vh; background-color: white; display: flex; justify-content: center; align-items: end">
    </div>

    <div style="width:100vw; display: flex">


      <div id="story" style="position: sticky; top: 100px; height: 80vh; width: 60vw; background-color: white">

<!--
        <div v-if="textIndex === 0" style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">
        </div>
-->

        <div v-show="textIndex === 1" style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">
          <DistancesStoryStep :sample="sample" :show-controls="true" :initial-layer="0"/>
        </div>

        <div v-show="textIndex === 2" style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">
          <DistancesStoryStep :sample="sample" :show-controls="true" :initial-layer="13"/>
        </div>

        <div v-if="textIndex === 3" style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">
          <SimpleNeighborhoodUnsorted v-if="allImages"
                              :transition-duration="1000"
                              :allImages="allImages" :index="sample" :num-samples="numSamples" :img-size="25"
                              color="var(--yellow)" :referenceLayer="0" :comparison-layer="0"/>
        </div>

        <div v-if="textIndex === 4 || textIndex === 5 || textIndex === 6"
             style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">

          <div style="position: absolute; top:20px">
            <div class="layer input">Input</div>
          </div>
          <div style="position: absolute; bottom:20px">
            <div :class="'layer ' + lineLayer.type ">{{ lineLayer.label }}</div>
          </div>

          <ParallelLineExplanation :step="textIndex - 3"
                                   :allImages="allImages"
                                   :index="sample"
                                   :num-samples="numSamples"
                                   :img-size="20"
                                   color1="var(--yellow)"
                                   :color2="lineLayer.color"
                                   :layer1="0"
                                   :layer2="lineLayer.value"
                                   v-on:overlap-count="c => overlapCount = c"
                                   style="height: 100%;"/>
        </div>

        <div v-if="textIndex === 7 || textIndex === 8"
             style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">

          <ParallelLineStory :lines="lines" :all-images="allImages"
                             :highlighted-sample="textIndex === 7? [sample] : [110635,101647,272791,271551,185767,146028,115656]"/>

        </div>

        <div v-if="textIndex === 9"
             style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">

          <ParallelLines :animate-line-draw="currentDirection==='down'" :data="lines" :selection="[]" v-on:selection=""
                         :enable-brush="false"/>

        </div>

        <div v-if="textIndex === 10"
             style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">

          <ParallelLines :animate-line-draw="false" :data="lines" v-if="lines"
                         :selection="lines.items.filter((l:any) => l.y === classes.indexOf('wine bottle')).map((item:any) => item.idx)"
                         v-on:selection="" :enable-brush="false"/>

        </div>

        <div v-if="textIndex === 11"
             style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">

          <ParallelLines :animate-line-draw="false" :data="lines" v-if="lines"
                         :selection="lines.items.filter((l:any) => l.y === classes.indexOf('wine bottle')).filter((l:any) => l.mean > 71).map((item:any) => item.idx)"
                         v-on:selection="" :enable-brush="false"/>

        </div>

        <div v-if="textIndex === 12"
             style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">

          <ParallelLines :animate-line-draw="false" :data="lines" v-if="lines"
                         :selection="lines.items.filter((l:any) => l.y === classes.indexOf('wine bottle')).filter((l:any) => l.mean < 35).map((item:any) => item.idx)"
                         v-on:selection="" :enable-brush="false"/>

        </div>

        <div v-if="textIndex === 13" style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">
          <SimpleNeighborhoodUnsorted v-if="allImages"
                              :transition-duration="1000"
                              :allImages="allImages" :index="sample" :num-samples="numSamples" :img-size="25"
                              color="var(--yellow)" :referenceLayer="0" :comparison-layer="0"/>
        </div>

        <div v-if="[14,15,16].includes(textIndex)" style=" height: 100%; width: 100%; border: 30px solid rgba(0,0,0,0);">
          <SimpleNeighborhood v-if="allImages"
                                      :transition-duration="1"
                                      :allImages="allImages" :index="sample" :num-samples="numSamples" :img-size="25"
                                      color="var(--yellow)" :referenceLayer="getRightLayer()" :comparison-layer="0"/>
        </div>

      </div>
      <div>
        <div style="height: 0;" :class="'text-block'" id="84373847"></div>

        <h2 style="padding: 20px">1. Distances</h2>

        <div :class="'text-block ' + ((activeText === '984398')? 'active' : '')" id="984398">
          <p>
            Let’s calculate the euclidean distance of our {{ sampleLabel }} sketch <span v-if="allImages"
                                                                                         class="icon-in-text"><img
              :src="'data:image/png;base64, ' + allImages[sample]" alt=""/></span> to all other samples in our
            validation dataset.
            We might start
            by asking if other {{ sampleLabel }}s are closer in space than let’s say
            {{ classes.filter(c => c !== sampleLabel)[0] }}s or {{ classes.filter(c => c !== sampleLabel)[1] }}s. The
            blue
            distribution shows the
            distances to other {{ sampleLabel }}s, while all grey distributions show the distances to samples of other
            classes. Here, we
            are using the <span class="layer input" style="padding: 5px; margin: -5px;">input</span>
            representation, i.e. the pixel values of our sketches.
          </p>


          <p v-if="[146028,115656,272791,271551,185767].includes(sample)">
            We see that by just looking at the black and white squares that the image is made up of and comparing them,
            other {{ sampleLabel }}s are not necessarily closer to our sketch than any other sketch in the dataset.
          </p>

          <p v-if="[110635,101647].includes(sample)">
            While a few other {{ sampleLabel }}s are already close to our sketch in euclidean space, we see that the
            distributions still overlap heavily, so not all {{ sampleLabel }}s are very similar.
          </p>
        </div>
        <div :class="'text-block ' + ((activeText === '490029')? 'active' : '')" id="490029">
          <p>If we jump all the way to the end of the network, the output of the <span
              style="padding: 5px; margin: -5px;" :class="'layer '+layers[13].type"> Linear </span> layer, we get quite
            a
            different picture. Calculating the distances between samples, we see that {{ sampleLabel }}s are now
            generally
            closer in
            space, while samples from other
            categories moved away from the sketch.</p>
          <p>In order for our network to accurately classify all samples, the output of the final layer, often referred
            to
            as logits, will be a vector of dimensions corresponding to the number of classes (15 in this case). The
            ideal
            behavior of the network is to produce a value of 1 at the index corresponding to the correct label and 0 for
            all other indices. If the network achieved perfect classification for every sample, we would hence see the
            distributions completely collapsed into these two points. Yet, this will not happen for any real dataset
            as there are ambiguous sketches and labelling errors. (optional mention: overfitting)</p>
          <p>Now, what happens in between these two extremes? If you are curios, you can already look at the
            effects by stepping through the layers on the left.</p>
          <p></p>
        </div>

        <h2 style="padding: 20px">2. Building a visualization</h2>

        <div :class="'text-block ' + ((activeText === '209834')? 'active' : '')" id="209834">
          <p>
            For understanding the neighborhood of a single sketch, we look at the distances we computed before and only
            take the first few samples that are the closest to our sketch.
            Here, we see <span class="text-highlight"> the {{ numSamples }} closest samples to the
          selected {{ sampleLabel }}</span>. Try to change the sample!
          </p>

          <p>
            Note: Our validation dataset has 300.000 samples, from here on we use a randomly subsampled dataset of
            10.000 samples. This has computational advantages but also makes the neighborhoods easier to analyse
            visually
            as
            samples from other classes enter the neighborhood earlier.
          </p>


        </div>
        <div :class="'text-block ' + ((activeText === '230920')? 'active' : '')" id="230920">
          <p>
            As our data is processed by the network, each layer will transform the numerical representation of each
            sketch. With that, the neighborhood of the sketch will change.
            When <span class="text-highlight"> we compare the neighborhood in the
          <span class="layer input" style="padding: 5px; margin: -5px;">input</span>
          representation to the one produced by the {{ ordinalLayer }} layer:
          <LayerDropdownSelect v-model="lineLayer"/>
          <ClickHere :size="24"/></span>
            , can we summarize the effects on the
            neighborhood in a concise way?
          </p>
          <p>
            A simple approximation is looking at the overlap of the neighborhood before and after the transformation.
          </p>
        </div>
        <div :class="'text-block ' + ((activeText === '457838')? 'active' : '')" id="457838">
          <p>
            <span class="text-highlight">Let's line up all samples from the two representations and count pairs</span>.
            Intuitively, the higher the count,
            the less the network impacted the neighborhood.
            In this case, {{ overlapCount }} samples of {{ numSamples }} in total are present in both representations.
          </p>
          <p>
            {{
              ((overlapCount > 80) ? "This is a rather high value and other samples will be impacted much stronger. This indicates that the current sample has a stable neighborhood." : "")
              + ((overlapCount <= 80 && overlapCount > 60) ? "This is an average number, for many other samples the neighborhood changes with similar strength." : "")
              + ((overlapCount <= 60) ? "This is an relatively low number, do you already have some ideas what this might mean for this sample?" : "")

            }}
          </p>
        </div>
        <div :class="'text-block ' + ((activeText === '148832')? 'active' : '')" id="148832">
          <p>
            For the sketch <span v-if="allImages" class="icon-in-text"><img
              :src="'data:image/png;base64, ' + allImages[sample]" alt=""/></span>, we can thus record the following
            result:

            <span class="text-highlight">{{ overlapCount }} of the {{ numSamples }} nearest neighbors in the <span class="layer input"
                                                                                    style="padding: 5px; margin: -5px;">input</span>
            layer are still part of the {{ numSamples }} nearest neighbors after the
            <span style="padding: 5px" :class="'layer '+lineLayer.type">
            {{ lineLayer.label }} </span> layer </span>, i.e. in the intermediate latent space created by propagating all
            samples through the network up to that layer.
          </p>

        </div>
        <div :class="'text-block ' + ((activeText === '563234')? 'active' : '')" id="563234">
          <p>
            If we repeat this analysis for each layer, we can see a trajectory of our sample throughout the network
            telling us
            how many of the initial neighbors are left after each transformation.
          </p>
        </div>
        <div :class="'text-block ' + ((activeText === '298048')? 'active' : '')" id="298048">
          <p>
            We can then compare multiple samples using this visualization to see patterns in the data.
            We color the lines according to the number of samples that are present in both the
            <span class="layer input" style="padding: 5px; margin: -5px;">input</span>
            and after the last <span class="layer linear" style="padding: 5px; margin: -5px;">linear</span> layer.
            We can observe that the car and wine bottle keep many of their inital neighbors whereas the train and the
            plane
            quickly lose most of their initial neighborhood. A good explanation could be that the first two sketches are
            very prototypical for their class and are surrounded by many similar samples that get transformed in similar
            ways. For the latter, it is likely that there aren't a lot of similar sketches which is why we observe more
            variation.
          </p>
        </div>

        <h2 style="padding: 20px">3. Exploring our new visualization</h2>

        <div :class="'text-block ' + ((activeText === '965932')? 'active' : '')" id="965932">
          <p>
            When we include the sketches from the whole dataset, several things are noteworthy:
          </p>
          <ul>
            <li>the number of remaining neighbors continuously decreases, confirming that <span class="text-highlight"> the network
            is transforming the space with each layer step by step </span>. If instead, the pattern would exhibit
              much more variance, then we would likely conclude that we cannot look at CNNs as a continuous
              transformation
              of space – rather at any point, any layer could significantly and unexpectedly transform one neighborhood
              but not the other.
            </li>
            <li>there is correlation that samples which neighborhoods are not heavily impacted by one layer will likely
              not be strongly impacted by other layers too – and vice versa. This indicates that
              <span class="text-highlight"> the visualization depends on
            the data characteristics </span> and not solely on the selected model architecture.
            </li>
          </ul>
        </div>
        <div :class="'text-block ' + ((activeText === '758388')? 'active' : '')" id="758388">
          <p>
            We already established that the visualization depends on the data, now we are going to explore some
            effects in more detail. Let's start by subsetting the data to <span
              class="text-highlight">only wine bottles</span>.
          </p>
          <p>
            We see that they significantly differ from the other trajectories of other classes, many of the samples
            keep many of their neighbors throughout the transformations of the network. Our hypothesis is
            that as there is little variation in the way people draw wine bottles, the numerical representations
            are very similar to each other. Therefore, the mathematical operations performed by the network also
            transform them in similar ways.
          </p>
        </div>


        <div :class="'text-block ' + ((activeText === '2399230')? 'active' : '')" id="2399230">
          <p>
            Let's pick a few samples of wine bottles with trajectories indicating stable neighborhoods,
            i.e. <span class="text-highlight">high numbers throughout</span>:
          </p>
          <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <span v-if="allImages && lines"
                  v-for="s of lines.items.filter((l:any) => l.y === classes.indexOf('wine bottle')).filter((l:any) => l.mean > 71).map((item:any) => item.idx)">
              <img :src="'data:image/png;base64, ' + allImages[s]" alt=""/>
            </span>
          </div>

          <p>
            They tend to be very <span class="text-highlight">prototypical wine bottles</span>. This is in line with the argumentation above:
            These samples potentially have other sketches surrounding them that are so similar, that they always stick together while being
            transformed.
          </p>
        </div>

        <div :class="'text-block ' + ((activeText === '623811')? 'active' : '')" id="623811">
          <p>
            Looking at the other end of the spectrum within the sketches labelled as wine bottles, we can see some
            interesting cases.
            Here are the samples:
          </p>
          <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <span v-if="allImages && lines"
                  v-for="s of lines.items.filter((l:any) => l.y === classes.indexOf('wine bottle')).filter((l:any) => l.mean < 35).map((item:any) => item.idx)">
              <img :src="'data:image/png;base64, ' + allImages[s]" alt=""/>
            </span>
          </div>

          <p>
            The <span class="text-highlight">sketches with low numbers tend to be either mislabelled or wine bottles drawn in unusual ways</span>,
            i.e. with a glass next to the bottle.
            For these cases, the surrounding closest samples are less uniform and therefore we see more variation.
          </p>
        </div>

        <h2 style="padding: 20px">4. Let's zoom in!</h2>

        <div :class="'text-block ' + ((activeText === '3490339')? 'active' : '')" id="3490339">
          <p>
           Our global view allows us to find interesting sketches, yet up to know we had to speculate about what happens
            concretely within the neighborhood of each sample. Now we will change this. We go back to the local neighborhood,
            showing the {{numSamples}} nearest neighbors from all given sketches for our sketch.
          </p>
        </div>

        <div :class="'text-block ' + ((activeText === '9439340')? 'active' : '')" id="9439340">
          <p>
           As we like it neat and tidy, we sort the neighbors by their label and put them into different sectors. The size
            of each sector corresponds to the share of samples of this class in the neighborhood.

            If you haven't changed the samples at the top so far, this is a good time to do so!
          </p>
        </div>

        <div :class="'text-block ' + ((activeText === '124111')? 'active' : '')" id="124111">
          <p>
            Let's watch our sketches as their get transformed by the first layer of the network. We trace the movement of
            the sketches with green when they move closer and red if they move away. The convolutional layer is an
            interesting one to start with: Convolutional layers can be interpreted as filters in classical image processing
            that respond to simple lines and shapes in early layers, and more and more complex features in later layers.
            Can you generate an hypothesis why the samples move like they do right here?
          </p>
        </div>


        <div :class="'text-block ' + ((activeText === '34099')? 'active' : '')" id="34099">
          <p>
            We can jump all the way to the end of the network now. There's a lot to explain here that I haven't put
            into nice words yet!
          </p>
        </div>


        <div :class="'text-block ' + ((activeText === '0348281')? 'active' : '')" id="0348281">
          <p>
            Feel free to explore for yourself now in our
            <span class="jump-section" @click="$emit('showDemo')">
               Explorer
            <img class="right" src="/arrow_right.svg">
            </span>

          </p>
        </div>

      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import ParallelLineExplanation from "./neighborhood/ParallelLineExplanation.vue";
import scrollama from "scrollama";
import {computed, onMounted, ref} from "vue";
import SampleSidebar from "./SampleSidebar.vue";
import {classes, layers, samples} from "../../utils/utils";
import LandingPage from "../LandingPage.vue";
import LayerDropdownSelect from "../reusables/LayerDropdownSelect.vue";
import ClickHere from "../reusables/ClickHere.vue";
import ParallelLineStory from "./parallelLines/ParallelLineStory.vue";
import DistancesStoryStep from "./distances/DistancesStoryStep.vue";
import SimpleNeighborhood from "../reusables/SimpleNeighborhood.vue";
import ParallelLines from "../shared/ParallelLines.vue";
import SimpleNeighborhoodUnsorted from "../reusables/SimpleNeighborhoodUnsorted.vue";

const props = defineProps({
  allImages: {} as any,
  lines: {} as any
})

defineEmits({
  showDemo: () => true
})

const activeText = ref("")
const textIndex = ref(0)
const currentDirection = ref("down" as 'down' | 'up')
const currentProgress = ref(0)
const scroller = scrollama();
const sample = ref(110635)
const displaySidebar = ref(true)
const lineLayer = ref(layers[1])
const overlapCount = ref(0)
const numSamples = ref(100)

onMounted(() => {
  scroller
      .setup({
        step: ".text-block",
        progress: true,
      })
      .onStepEnter((e: any) => {
        activeText.value = e.element.id
        textIndex.value = e.index
        currentDirection.value = e.direction


        displaySidebar.value = textIndex.value < 8 || textIndex.value > 12

      })
      .onStepProgress((e: any) => {
        currentProgress.value = e.progress
      })
      .onStepExit((response: any) => {
        // { element, index, direction }
      });
})

const ordinalLayer = computed(() => {
  let n = lineLayer.value.value;
  let s = ["th", "st", "nd", "rd"];
  let v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
})

const sampleLabel = computed(() => samples[sample.value].label)


const getRightLayer = () => {
  if(textIndex.value === 14){
    return 0
  }
  if(textIndex.value === 15){
    return 1
  }
  if(textIndex.value === 16){
    return 12
  }
}

</script>

<style scoped>

.text-block {
  border-left: 5px solid white;
  margin: 20px;
  width: calc(40vw - 100px);
  background-color: white;
  padding: 20px;
  font-size: large;
  line-height: 1.8;
  /*min-height: 300px;*/
}

.top-margin {
  height: 500px;
}

.text-block:last-of-type {
  margin-bottom: 60vh;
}

.active {
  border-left: 5px solid var(--blue);
}

.icon-in-text {
  display: inline-block;
  margin-top: -60px;
  margin-bottom: -60px;
  height: 2px;
}

.icon-in-text > img {
  vertical-align: middle;
}

.text-highlight {
  font-weight: bold;
}

.text-highlight::after {
  font-weight: bold;
}

</style>