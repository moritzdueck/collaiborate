<template>
  <div style="position: relative">
    <div style="height: 100vh; width: 100vw;">
      <LandingPage :all-images="allImages" v-on:show-demo="$emit('showDemo')"></LandingPage>
    </div>

    <!--  Background  -->
    <div
        style=" width: 100vw; padding: 50px; background-color: var(--gray); display: flex; justify-content: center">
      <div style="max-width: 1280px; width: 100%; font-size: larger">
        <h2 @click="showBackground = !showBackground" class="background-toggle">Background <img
            :class="showBackground? 'rotated' : ''" src="/plus.svg"/></h2>
        <template v-if="showBackground">

          <div style="overflow: hidden">
            <p style="margin-top: 0">
              We analyze a convolutional neural network that is trained to classify images of the QuickDraw dataset. The
              dataset contains over 50 million drawings of people depicting everyday objects, grouped into 345
              categories.
              We will focus on the following 15 categories to keep things simple: airplane, apple, bee, car, dragon,
              mosquito, moustache, mouth, pear, piano, pineapple, smiley face, train, umbrella and wine bottle. In order
              to have a perfectly balanced dataset, we sampled 100.000 instances of each class. The network should learn
              to classify these training samples correctly. We used 80% of the data for training and the other 20%,
              amounting to 300.000 samples across the fifteen categories, representing our test data we use for probing
              and analyzing the model in the following.
            </p>

            <p>
              The <a
                href="https://github.com/moritzdueck/collaiborate/blob/2f7911658ac06ca745e63f86d5268ff4858789c0/collaiborate/train_script.py#L37-L51"
                target="_blank">model</a>
              was trained using PyTorch and has the following architecture:
            </p>

            <img style="width: 100%;" src="/cnnCollaiborate.svg"/>

            <p>
              For many machine learning models, visually analyzing latent spaces provides interesting insights into the
              inner workings of general deep learning models [<span v-html="getCitation('embeddingComparator')"/>, <span
                v-html="getCitation('latentSpaceCartography')"/>]
              or language models [<span v-html="getCitation('LMFingerprints')"/>,
              <span v-html="getCitation('NeuralWordEmbeddings')"/>]. In this work, we treat each layer of the CNN as a
              function whose multidimensional output range can be interpreted as a latent space. Within each of these
              latent spaces, we can analyze our whole dataset and investigate the distances between individual samples.
              Papernot et al. [<span v-html="getCitation('dKNN')"/>] has
              used the idea of calculating the k nearest neighbors across layer representation for CNN model robustness,
              demonstrating that these neighborhoods contain useful information. Embeddings can stem from a variety of
              models and techniques, so other authors focus on analyzing embeddings irrespective of data and model
              specifics. Heimerl et al. [<span v-html="getCitation('embComp')"/>] use local neighborhood
              information together with global patterns to compare embeddings in a visual system, focusing on the
              comparison of any two different embeddings of the same data. Inspired by these
              contributions, our investigation is motivated by the following questions: Focusing on a CNN image
              classification model, is the locality within its latent spaces meaningful? Can such an investigation help
              explain how the model behaves and what it has learnt? And how do individual network layers affect and
              transform these spaces as samples are propagated through the model? This last aspect is specific to our
              work
              due to the well-defined relation between the spaces through the mathematical operations performed by the
              model.
            </p>

            <p>Let's embark on this journey!</p>
          </div>


        </template>

        <template v-if="!showBackground">
          <div class="gradient-opacity" @click="showBackground = !showBackground">
            <p style="margin-top: 0">
              We analyze a convolutional neural network that is trained to classify images of the QuickDraw dataset. The
              dataset contains over 50 million drawings of people depicting everyday objects, grouped into 345
              categories.
              We will focus on the following 15 categories to keep things simple: airplane, apple, bee, car, dragon,
              mosquito, moustache, mouth, pear, piano, pineapple, smiley face, train, umbrella and wine bottle. In order
              to have a perfectly balanced dataset, we sampled 100.000 instances of each class. The network should learn
              to classify these training samples correctly. We used 80% of the data for training and the other 20%,
              amounting to 300.000 samples across the fifteen categories, representing our test data we use for probing
              and analyzing the model in the following.
            </p>
          </div>
        </template>
      </div>
    </div>

    <div style="display: flex; justify-content: center">
      <div
          style="max-width: 1920px; width:100%; height: 50vh; display: flex; justify-content: left; align-items: end;">
        <h3 style="margin-bottom: 20px; margin-left: 20px">At any point, you can interact with this menu:</h3>
      </div>
    </div>


    <div style="display: flex; justify-content: center">
      <div style="width:100vw; display: flex; max-width: 1920px;">
        <div id="story" class="story-container">

          <div class="story-menu">
            <div style="display: flex; align-items: center;" v-if="topMenu.showSample">
              <p style="writing-mode: vertical-lr;">Sample</p>
              <SampleSidebar :all-images="allImages" v-model="sample"/>
            </div>
            <div style="display: flex; align-items: center;" v-if="topMenu.showNumSamples">
              <p style="width: 120px;">{{ numSamples2 }} neighbors</p>
              <div style="width: 100%; padding: 10px">
                <Slider v-model:model-value="numSamples2" :min="2" :max="750"/>
              </div>
            </div>
            <div style="display: flex; align-items: center;" v-if="topMenu.showNetwork">
              <p style="writing-mode: vertical-lr;">Representation</p>
              <CnnLayersShapes :show-pin="[16, 17].includes(textIndex)" :initial-layer="layer"
                               v-on:selected-layer="l => layer = l" :controlled="true"/>
            </div>
            <div v-if="[3,4,5,6,7].includes(textIndex)" style="display: flex; align-items: center;">
              <p style="writing-mode: vertical-lr;">Representation</p>
              <CnnLayersShapesPassive :show-input="[3,4,5,6].includes(textIndex)"
                                      :show-conv="[4,5,6,7].includes(textIndex)"/>
            </div>
          </div>

          <div v-show="textIndex === 1" class="story-illustration-container">
            <Distances :layer="layer" :sample="sample"/>
          </div>

          <div v-show="textIndex === 2" class="story-illustration-container">
            <Distances :layer="layer" :sample="sample"/>
          </div>

          <div v-if="textIndex === 3" class="story-illustration-container">
            <SimpleNeighborhoodUnsorted v-if="allImages"
                                        :transition-duration="1000"
                                        :allImages="allImages" :index="sample" :num-samples="numSamples" :img-size="25"
                                        color="var(--yellow)" :referenceLayer="0" :comparison-layer="0"/>
          </div>

          <div v-if="textIndex === 4 || textIndex === 5 || textIndex === 6 || textIndex === 7"
               class="story-illustration-container">

            <div style="position: absolute; top:33%" v-if="textIndex === 4 || textIndex === 5">
              <div class="layer input">Input</div>
            </div>
            <div style="position: absolute; bottom:33%" v-if="textIndex === 4 || textIndex === 5">
              <div :class="'layer ' + lineLayer.type ">{{ lineLayer.label }}</div>
            </div>


            <div style="position: absolute; left:0px; width: 100%; height: 100%;">
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

          </div>

          <div v-if="textIndex === 8 || textIndex === 9"
               class="story-illustration-container">

            <div style="position: absolute; left:0; width: 100%; height: 100%;">
              <ParallelLineStory :lines="lines" :all-images="allImages"
                                 :highlighted-sample="textIndex === 8? [sample] : [110635,101647,272791,271551,185767,146028,115656]"/>
            </div>


          </div>

          <div v-if="textIndex === 10"
               class="story-illustration-container">

            <div style="position: absolute; width: 100%; height: 100%;">
              <ParallelLines :animate-line-draw="currentDirection==='down'" :data="lines" :selection="[]"
                             v-on:selection=""
                             :enable-brush="false"/>
            </div>


          </div>

          <div v-if="textIndex === 11"
               class="story-illustration-container">
            <div style="position: absolute; left:0; width: 100%; height: 100%;">
              <ParallelLines :animate-line-draw="false" :data="lines" v-if="lines"
                             :selection="lines.items.filter((l:any) => l.y === classes.indexOf('wine bottle')).map((item:any) => item.idx)"
                             v-on:selection="" :enable-brush="false"/>
            </div>

          </div>

          <div v-if="textIndex === 12"
               class="story-illustration-container">
            <div style="position: absolute; left:0; width: 100%; height: 100%;">
              <ParallelLines :animate-line-draw="false" :data="lines" v-if="lines"
                             :selection="lines.items.filter((l:any) => l.y === classes.indexOf('wine bottle')).filter((l:any) => l.mean > 71).map((item:any) => item.idx)"
                             v-on:selection="" :enable-brush="false"/>
            </div>

          </div>

          <div v-if="textIndex === 13"
               class="story-illustration-container">

            <div style="position: absolute; left:0; width: 100%; height: 100%;">
              <ParallelLines :animate-line-draw="false" :data="lines" v-if="lines"
                             :selection="lines.items.filter((l:any) => l.y === classes.indexOf('wine bottle')).filter((l:any) => l.mean < 35).map((item:any) => item.idx)"
                             v-on:selection="" :enable-brush="false"/>
            </div>

          </div>

          <div v-if="textIndex === 14" class="story-illustration-container">
            <div style="display: flex; height: 100%">
              <SimpleNeighborhoodUnsorted v-if="allImages"
                                          :transition-duration="1"
                                          :allImages="allImages" :index="sample" :num-samples="numSamples2"
                                          :img-size="25"
                                          color="var(--gray)" :referenceLayer="layer"
                                          :comparison-layer="layer"/>
            </div>
          </div>

          <div v-if="[15,16,17].includes(textIndex)"
               class="story-illustration-container">
            <div style="display: flex; height: 100%">
              <SimpleNeighborhood v-if="allImages && lines"
                                  :transition-duration="0"
                                  :color-sector="lines.items.find((i:any) => i.idx === sample).y"
                                  :allImages="allImages" :index="sample" :num-samples="numSamples2" :img-size="25"
                                  color="var(--gray)" :referenceLayer="layer"
                                  :comparison-layer="textIndex === 15? layer : 0"/>
            </div>

          </div>

        </div>
        <div>
          <div style="height: 50vh;" :class="'text-block'" id="84373847"></div>

          <h2 style="padding: 20px">1. Distances</h2>

          <div :class="'text-block ' + ((activeText === '984398')? 'active' : '')" id="984398">
            <p>
              Let’s calculate the euclidean distance of our {{ sampleLabel }} sketch <span v-if="allImages"
                                                                                           class="icon-in-text"><img
                :src="'data:image/png;base64, ' + allImages[sample]" alt=""/></span> to all other samples in our
              test dataset. Here, we
              are using the <span class="text-layer-highlight">Input</span>
              representation, i.e. the pixel values of our sketches.

              Samples from the same class can already be numerically similar in the input representation. For example,
              many people
              will draw a car in a similar way:

            </p>

            <span v-if="allImages" class="icon-in-text"><img :src="'data:image/png;base64, ' + allImages[62252]"
                                                             alt=""/></span>
            <span v-if="allImages" class="icon-in-text"><img :src="'data:image/png;base64, ' + allImages[168945]"
                                                             alt=""/></span>
            <span v-if="allImages" class="icon-in-text"><img :src="'data:image/png;base64, ' + allImages[89829]"
                                                             alt=""/></span>
            <span v-if="allImages" class="icon-in-text"><img :src="'data:image/png;base64, ' + allImages[270910]"
                                                             alt=""/></span>
            <span v-if="allImages" class="icon-in-text"><img :src="'data:image/png;base64, ' + allImages[150474]"
                                                             alt=""/></span>

            <p>
              With that in mind, we might start
              by asking if for our specific sample <span v-if="allImages"
                                                         class="icon-in-text"><img
                :src="'data:image/png;base64, ' + allImages[sample]" alt=""/></span>, other {{ sampleLabel }}s are
              closer in space than, let’s say,
              {{ classes.filter(c => c !== sampleLabel)[0] }}s or {{ classes.filter(c => c !== sampleLabel)[1] }}s.


              <span class="text-highlight">The <span style="color: var(--blue); font-weight: bold">blue</span>
                distribution shows the distances to other {{ sampleLabel }}s</span>,
              while all gray distributions show the distances to samples of other
              classes.
            </p>

            <SampleFocus :all-images="allImages" :sample="sample" v-if="[110635,101647].includes(sample)">
              While the closest samples to our {{ sampleLabel }} are other {{ sampleLabel }}s, a large part of the
              distribution overlaps with the distances to other classes, so for most {{ sampleLabel }}s the initial
              distance does not tell us anything about the class label.
            </SampleFocus>


            <SampleFocus :all-images="allImages" :sample="sample"
                         v-if="[146028,115656,272791,271551,185767].includes(sample)">
              We see that by just looking at the black and white squares that the image is made up of and comparing
              them,
              other {{ sampleLabel }}s are not necessarily closer to our sketch than any other sketch in the dataset.
            </SampleFocus>

          </div>
          <div :class="'text-block ' + ((activeText === '490029')? 'active' : '')" id="490029">
            <p>If we jump all the way to the end of the network, the output of the
              <span class="text-layer-highlight">Linear</span> layer, we get quite a
              different picture.

              After calculating the distances from our source image to all other samples, <span class="text-highlight">we see that the other
              {{ sampleLabel }}s moved closer in space</span> , while samples from other categories moved away from the
              sketch. But be careful: this separation does not work equally well for all samples.
            </p>


            <p>
              The output of the final layer will be a vector of dimensions corresponding to the number of classes (15 in
              this case). The ideal behavior of the network is to produce a high positive value at the index
              corresponding
              to the correct label while setting all other values far below zero. As neural networks tend to produce
              smooth representations, this incentive is enough to observe samples of the target class moving closer to
              each other. Now, what happens in between these two extremes? If you are curious, you can already look at
              the
              effects by stepping through the layers on the left.
            </p>
          </div>

          <h2 style="padding: 20px">2. Building a visualization</h2>

          <div :class="'text-block ' + ((activeText === '209834')? 'active' : '')" id="209834">
            <p>
              For understanding the neighborhood of a single sketch, we look at the distances we computed before and
              only
              take the first few samples that are the closest to our sketch.
              Here, we see <span class="text-highlight"> the {{ numSamples }} closest samples to the
          selected {{ sampleLabel }}</span>.
            </p>

            <p>
              Note: Our validation dataset has 300.000 samples, from here on we use a randomly subsampled dataset of
              10.000 samples. This has computational advantages but also makes the neighborhoods easier to analyse
              visually as samples from other classes enter the neighborhood earlier.
            </p>


          </div>
          <div :class="'text-block ' + ((activeText === '230920')? 'active' : '')" id="230920">
            <p>
              As our data is processed by the network, each layer will transform the numerical representation of each
              sketch. With that, the neighborhood of the sketch will change.
              When <span class="text-highlight"> we compare the neighborhood in the
          <span class="layer input" style="padding: 5px; margin: -5px;">input</span>
          representation to the one produced by the {{ ordinalLayer }} layer:
              <!--          <LayerDropdownSelect v-model="lineLayer"/>-->
            <span class="layer convolution" style="padding: 5px; margin: -5px;">{{ lineLayer.label }}</span>
          </span>
              , can we summarize the effects on the
              neighborhood in a concise way?
            </p>
            <p>
              A simple approximation is looking at the overlap of the neighborhood before and after the transformation.
            </p>
          </div>
          <div :class="'text-block ' + ((activeText === '457838')? 'active' : '')" id="457838">
            <p>
              We can project the samples back to one dimension – still sorted by distance – and compare the two
              representations.
              <span class="text-highlight"> We draw a line between
            samples that are present in both representations.</span>
            </p>

          </div>
          <div :class="'text-block ' + ((activeText === '3499233')? 'active' : '')" id="3499233">
            <p>
              <span class="text-highlight">Let's count pairs</span>.
              Intuitively, the higher the count,
              the less the network impacted the neighborhood.
              In this case, {{ overlapCount }} samples of {{ numSamples }} in total are present in both representations.
            </p>

            <SampleFocus :sample="sample" :all-images="allImages" v-if="overlapCount > 80">
              This is a rather high value and other samples will be impacted much stronger. This indicates that the
              current sample has a stable neighborhood.
            </SampleFocus>

            <SampleFocus :sample="sample" :all-images="allImages" v-if="(overlapCount <= 80 && overlapCount > 60)">
              This is an average number, for many other samples the neighborhood changes with similar strength.
            </SampleFocus>

            <SampleFocus :sample="sample" :all-images="allImages" v-if="overlapCount <= 60">
              This is an relatively low number, do you already have some ideas what this might mean for this sample?
            </SampleFocus>

          </div>
          <div :class="'text-block ' + ((activeText === '148832')? 'active' : '')" id="148832">
            <p>
              For the sketch <span v-if="allImages" class="icon-in-text"><img
                :src="'data:image/png;base64, ' + allImages[sample]" alt=""/></span>, we can thus record the following
              result:

              <span class="text-highlight">{{ overlapCount }} of the {{ numSamples }} nearest neighbors in the <span
                  class="layer input"
                  style="padding: 5px; margin: -5px;">input</span>
            layer are still part of the {{ numSamples }} nearest neighbors after the
            <span style="padding: 5px" :class="'layer '+lineLayer.type">
            {{ lineLayer.label }} </span> layer </span>, i.e. in the intermediate latent space created by propagating
              all
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
              quickly lose most of their initial neighborhood. A good explanation could be that the first two sketches
              are
              very prototypical for their class and are surrounded by many similar samples that get transformed in
              similar
              ways. For the latter, it is likely that there aren't a lot of similar sketches which is why we observe
              more
              variation.
            </p>
          </div>

          <h2 style="padding: 20px">3. Exploring our new visualization</h2>

          <div :class="'text-block ' + ((activeText === '965932')? 'active' : '')" id="965932">
            <p>
              When we include the sketches from the whole dataset, several things are noteworthy:
            </p>
            <ul>
              <li>
                the number of remaining neighbors continuously decreases, confirming that <span class="text-highlight">the network is transforming the space with each layer step by step</span>.
                If instead, the numbers for one sample would fluctuate with high variance it would mean that at any
                point, any layer could significantly and unexpectedly transform one neighborhood but not the other,
                rendering any global analysis of effects impossible.
              </li>
              <li>
                Secondly, there is a correlation that samples keeping most of their neighbors in one layer are also
                keeping many of their neighbors in other layers – and vice versa. Visually, this corresponds to colors
                staying separated. This indicates that <span class="text-highlight">the visualization depends on the data characteristics</span>
                and not solely on the selected model architecture.
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
              We see that they significantly differ from the other trajectories of other classes: Many of the samples
              keep many of their neighbors throughout the transformations of the network. Our hypothesis is that, as
              there is little variation in the way people draw wine bottles, the numerical representations are very
              similar to each other. Therefore, the mathematical operations performed by the network transform them in
              similar ways, keeping clusters closer together than for other classes.
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
              They tend to be very <span class="text-highlight">prototypical wine bottles</span>. This is in line with
              the
              argumentation above:
              These samples potentially have other sketches surrounding them that are so similar, that they always stick
              together while being
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
              Our global view allows us to find interesting sketches, yet up to now we had to speculate about what
              happens
              concretely within the neighborhood of each sample. Now we will change this. We go back to the local
              neighborhood,
              showing the {{ numSamples2 }} nearest neighbors from all given sketches for our sketch.
            </p>
          </div>

          <div :class="'text-block ' + ((activeText === '9439340')? 'active' : '')" id="9439340">
            <p>
              As we like it neat and tidy, we sort the neighbors by their label and put them into different sectors. The
              size
              of each sector corresponds to the share of samples of this class in the neighborhood.

              If you haven't changed the samples at the top so far, this is a good time to do so!
            </p>
          </div>

          <div :class="'text-block ' + ((activeText === '124111')? 'active' : '')" id="124111">
            <p>
              Let's watch our sketches as their get transformed by the first layer of the network.
              We will always compare the change in euclidean distances <span class="text-highlight"> with respect to distances in the
            Input</span> representation, signaled by the pin
              <img src="/pin_red.svg" alt="pin"
                   style="width: 25px; vertical-align: middle; display: inline-block; writing-mode: vertical-lr;"/>.
              We trace the movement of the sketches with <span class="text-highlight"> <span
                style="color: var(--blue); font-weight: bold">blue</span>
            when they move closer
            and
            <span style="color: var(--orange); font-weight: bold">orange</span> if they move away</span>. The
              convolutional
              layer is an
              interesting one to start with: Convolutional layers can be interpreted as filters in classical image
              processing
              that respond to simple lines and shapes in early layers, and more and more complex features in later
              layers.
              Can you generate a hypothesis why the samples move like they do right here?
            </p>
          </div>


          <div :class="'text-block ' + ((activeText === '34099')? 'active' : '')" id="34099">
            <p>
              We can jump all the way to the end of the network now.
            </p>

            <SampleFocus :sample="sample" :all-images="allImages" v-if="sample === 110635">
              We can see that the final neighborhood consists purely of cars. If the sample and sufficiently many
              other samples of the same class are predicted with high certainty, the logits will be close
              to each other in euclidean space.
            </SampleFocus>

            <SampleFocus :sample="sample" :all-images="allImages" v-if="sample === 101647">
              We can see that the final neighborhood consists purely of wine bottles. This sample is arguably the
              easiest
              to classify for the network, a simple KNN classifier in the input space would already clearly identify the
              sample as a wine bottle.
            </SampleFocus>

            <SampleFocus :sample="sample" :all-images="allImages" v-if="sample === 272791">
              This sample shows an interesting trajectory as the initial neighborhood contains a very low number of
              bees,
              i.e. the pixel overlap with other bee sketches is rather low. As the drawing is propagated through the
              layers,
              more and more bees enter.
            </SampleFocus>

            <SampleFocus :sample="sample" :all-images="allImages" v-if="sample === 271551">
              Look at the closest samples to our mosquito from the bee class in the final representation.
              They are arguably very similar sketches and I myself would classify these bees as a mosquito as well.
              Good job network!
            </SampleFocus>

            <SampleFocus :sample="sample" :all-images="allImages" v-if="sample === 185767">
              For this sample, the network is also able to clear the neighborhood of any samples that are not
              pineapples.
              Interestingly, the first few layers reposition this sample closer to wine bottles and pears rather than
              pineapples. Later layers then clearly revert this early trend.
            </SampleFocus>

            <SampleFocus :sample="sample" :all-images="allImages" v-if="sample === 146028">
              We see that some mosquitos are left in the final neighborhood. Visually, that seems quite plausible.
              Interestingly, the sample still has a large number of trains in the neighborhood after the convolutional
              layers – the linear layers then reshape the neighborhood significantly.
            </SampleFocus>

            <SampleFocus :sample="sample" :all-images="allImages" v-if="sample === 115656">
              Here, the final neighborhood is much more diverse than for the other examples. From the color patterns, we
              can also tell that the network is pulling samples from other classes closer, for example dragons or cars.
            </SampleFocus>

            <p>
              Conceptually, the convolutional layers of a CNN are often regarded as feature extractors, so the output of
              the last max-pooling layer is often used for analyzing the model’s latent understanding of the data. Try
              exploring this representation and compare it to the final layers. Can you identify a change in behavior of
              the model when switching from the convolutional to the linear layers?
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


    <div
        style="min-height: 100vh; width: 100vw; padding: 50px; background-color: var(--gray); display: flex; justify-content: center">
      <div style="max-width: 1280px; font-size: larger">
        <h2>Summary</h2>
        <p>
          In this paper we contributed the following three visualizations:
        </p>

        <div class="display-visualization">
          <div style="position: relative">
            <img src="/visualizations/distanceToAll.svg"/>
            <div style="position: absolute; top: 5px; left: 20px">
              <p>
                <span
                    style="width: 20px; height: 20px; border: 3px solid var(--blue); display: inline-block; vertical-align: middle; background-color: var(--blue-transparent);"></span>
                Sketches from the same class</p>
              <p>
                <span
                    style="width: 20px; height: 20px; border: 3px solid var(--gray); display: inline-block; vertical-align: middle; background-color: var(--gray-transparent);"></span>
                Sketches from another class
              </p>
            </div>
          </div>
          <div style="margin-bottom: 100px;">
            <h3>1. Distances of one sample to all other samples grouped by class label</h3>
            <p>We compute the euclidean distance of a single sample to all other individual samples in the test dataset.
              We group these distances by class label and aggregate them into distributions using kernel density
              estimation. The <span style="color: var(--blue); font-weight: bold">blue</span>
              distribution contains the distances to samples with matching class labels.</p>
            Questions answered by this visualization:
            <ol>
              <li>Does the network learn to encode class probabilities in Euclidean space?</li>
              <li>How well separated is the target class after each layer?</li>
            </ol>
          </div>
        </div>

        <div class="display-visualization">

          <div style="margin-bottom: 100px;">
            <h3>2. Global neighborhood stability plot</h3>
            <p>
              We propagate each sample through the convolutional neural network and record the 100 nearest neighbors
              after each layer. For each layer, we compute the cardinality of the set intersection between the 100
              nearest neighbors in the input and after the layer. The visualization emerges by connecting these points
              for each sample across the layers.
            </p>

            Questions answered by this visualization:
            <ol>
              <li>How strongly do neighborhoods of samples in the dataset get affected by each layer?</li>
              <li>How do the trajectories of different samples or groups of samples compare?</li>
            </ol>
          </div>

          <img src="/visualizations/localSlim.svg"/>
        </div>

        <div class="display-visualization">

          <img src="/visualizations/local.svg"/>

          <div style="margin-bottom: 100px;">
            <h3>3. Local neighborhood transformation plot</h3>

            <p>
              Given one specific sample, we compute the k nearest neighbors and radially position them around the
              sample. The radius corresponds to the euclidean distance to the sample and is min-max normalized.
              Analogously to a pie chart, we compute slices for each class label proportional to the number of samples
              from that class. Each sample is then assigned a random angle within their slice to minimize overplotting.
              The slice containing the samples of the same class as the investigated sample is colored in gray.
            </p>
            <p>
              Colored traces depict the change in euclidean distance between the samples from one representation to
              another. The length of each trace is proportional to the difference between the samples’ values in the
              min-max normalized distance ranges implied by the k nearest neighbors in both representations. A trace is
              plotted for each sample in the union of the k nearest neighbors in both representations.
            </p>

            Questions answered by this visualization:
            <ol>
              <li>Which samples does the network pull closer in Euclidean spaces and which samples are pushed away
                throughout the layers?
              </li>
            </ol>
          </div>

        </div>
      </div>
    </div>

    <div style="display: flex; justify-content: center;">
      <div class="citations">
        <span></span>
        <h3>References</h3>

        <template v-for="reference of references">
          <span>{{ '[' + references.findIndex(citation => citation.id === reference.id) + ']' }}</span>
          <p :id="reference.id">{{ reference.text }}</p>
        </template>
      </div>
    </div>

    <div class="links">
      <a href="https://github.com/moritzdueck/collaiborate" target="_blank">
        <img style="cursor:pointer; width: 30px;" src="/github-mark.svg"/>
      </a>
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
import ParallelLineStory from "./parallelLines/ParallelLineStory.vue";
import SimpleNeighborhood from "../reusables/SimpleNeighborhood.vue";
import ParallelLines from "../shared/ParallelLines.vue";
import SimpleNeighborhoodUnsorted from "../reusables/SimpleNeighborhoodUnsorted.vue";
import CnnLayersShapes from "../reusables/CnnLayersShapes.vue";
import Distances from "./distances/Distances.vue";
import SampleFocus from "./SampleFocus.vue";
import CnnLayersShapesPassive from "../reusables/CnnLayersShapesPassive.vue";
import {addCitations} from "../../citationHelper";

const props = defineProps({
  allImages: {} as any,
  lines: {} as any
})

const references = [
  {
    id: 'embeddingComparator',
    doi: '10.1145/3490099.3511122',
    text: 'Boggust, A., Carter, B., & Satyanarayan, A. (2022, March 22). Embedding Comparator: Visualizing Differences in Global Structure and Local Neighborhoods via Small Multiples. 27th International Conference on Intelligent User Interfaces. IUI ’22: 27th International Conference on Intelligent User Interfaces. https://doi.org/10.1145/3490099.3511122'
  },
  {
    id: 'latentSpaceCartography',
    doi: '10.1111/cgf.13672',
    text: 'Liu, Y., Jun, E., Li, Q., & Heer, J. (2019). Latent Space Cartography: Visual Analysis of Vector Space Embeddings. Computer Graphics Forum, 38(3), 67–78. https://doi.org/10.1111/cgf.13672'
  },
  {
    id: 'LMFingerprints',
    doi: '10.1111/cgf.14541',
    text: 'Sevastjanova, R., Kalouli, A., Beck, C., Hauptmann, H., & El‐Assady, M. (2022). LMFingerprints: Visual Explanations of Language Model Embedding Spaces through Layerwise Contextualization Scores. Computer Graphics Forum, 41(3), 295–307. https://doi.org/10.1111/cgf.14541'
  },
  {
    id: 'NeuralWordEmbeddings',
    doi: '10.1109/TVCG.2017.2745141',
    text: 'Liu, S., Bremer, P.-T., Thiagarajan, J. J., Srikumar, V., Wang, B., Livnat, Y., & Pascucci, V. (2018). Visual Exploration of Semantic Relationships in Neural Word Embeddings. IEEE Transactions on Visualization and Computer Graphics, 24(1), 553–562. https://doi.org/10.1109/tvcg.2017.2745141'
  },
  {
    id: 'dKNN',
    doi: '10.48550/arXiv.1803.04765',
    text: 'Papernot, N., & McDaniel, P. (2018). Deep k-Nearest Neighbors: Towards Confident, Interpretable and Robust Deep Learning (Version 1). arXiv. https://doi.org/10.48550/ARXIV.1803.04765'
  },
  {
    id: 'embComp',
    doi: '10.1109/TVCG.2020.3045918',
    text: 'Heimerl, F., Kralj, C., Moller, T., & Gleicher, M. (2022). embComp: Visual Interactive Comparison of Vector Embeddings. IEEE Transactions on Visualization and Computer Graphics, 28(8), 2953–2969. https://doi.org/10.1109/tvcg.2020.3045918'
  },
] as { id: string, doi: string, text: string }[];

defineEmits({
  showDemo: () => true
})

const activeText = ref("")
const textIndex = ref(0)
const currentDirection = ref("down" as 'down' | 'up')
const currentProgress = ref(0)
const scroller = scrollama();
const sample = ref(110635)
const layer = ref(0)
const lineLayer = ref(layers[1])
const overlapCount = ref(0)
const numSamples = ref(100)
const numSamples2 = ref(300)
const redGreenLayer = ref(0)
const topMenu = ref({
  showSample: true,
  showNetwork: true,
  showNumSamples: false,
  showPassiveNetwork: false,
})
const showBackground = ref(false)

onMounted(() => {
  scroller
      .setup({
        step: ".text-block",
        progress: true,
        offset: 0.3
      })
      .onStepEnter((e: any) => {
        activeText.value = e.element.id
        textIndex.value = e.index
        currentDirection.value = e.direction

        topMenu.value.showSample = [0, 1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 16, 17].includes(textIndex.value)
        topMenu.value.showNetwork = [0, 1, 2, 14, 15, 16, 17].includes(textIndex.value)
        topMenu.value.showNumSamples = [14, 15, 16, 17].includes(textIndex.value)

        if (textIndex.value === 1) {
          layer.value = 0
        }
        if (textIndex.value === 2) {
          layer.value = 13
        }

        if (textIndex.value === 14) {
          layer.value = 0
        }
        if (textIndex.value === 15) {
          layer.value = 0
        }
        if (textIndex.value === 16) {
          layer.value = 1
        }
        if (textIndex.value === 17) {
          layer.value = 13
        }

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


const getCitation = (id: string): string => {
  return '<a href=\"#' + id + '\">' + references.findIndex(citation => citation.id === id) + '</a>'
}

const getRightColor = (layer: number) => {
  return layers[layer].color
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

.text-layer-highlight {
  color: var(--red);
  font-weight: bold;
}

.story-illustration-container {
  height: 100%;
  width: 100%;
  border: 30px solid rgba(0, 0, 0, 0);
  position: relative;
}

.story-container {
  position: sticky;
  top: 0;
  height: 100vh;
  width: 60vw;
  background-color: rgba(255, 255, 255, 0.5);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  margin-right: 50px;
  align-items: center;
}

.story-menu {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: flex-start;
  justify-content: center;
  z-index: 999;
  backdrop-filter: blur(30px);
  background-color: #ffffff7d;
  width: 100%;
  max-width: 800px;
}

.story-menu > div {
  overflow: auto;
  width: 100%;
}

.story-menu > div:first-of-type {
  padding-top: 15px;
}

.story-menu > div:last-of-type {
  padding-bottom: 15px;
  border-bottom: 3px solid var(--gray);
}

.citations {
  display: grid;
  grid-template-columns: auto 1fr;
  padding: 20px;
  align-items: baseline;
  column-gap: 10px;
  max-width: 1280px;
  margin-bottom: 100px;
}

.links {
  display: flex;
  justify-content: center;
  margin-bottom: 50px;
}

.display-visualization {
  background-color: white;
  padding: 30px;
  display: grid;
  grid-template-columns: 50% 50%;
  margin-bottom: 70px;
  column-gap: 10px;
  border-radius: 5px;
  max-width: calc(100vw - 60px);
}

.display-visualization > img, .display-visualization > div > img {
  width: 100%;
  max-height: 600px;
  max-width: 100%;
}

.background-toggle {
  cursor: pointer;
  -webkit-user-select: none; /* Safari */
  -ms-user-select: none; /* IE 10 and IE 11 */
  user-select: none; /* Standard syntax */
}

.background-toggle:hover {
}

.background-toggle > img {
  transform: rotate(0deg);
  transition: all 0.3s ease;
  pointer-events: none;
  -webkit-user-select: none; /* Safari */
  -ms-user-select: none; /* IE 10 and IE 11 */
  user-select: none; /* Standard syntax */
}

.background-toggle > img.rotated {
  transform: rotate(45deg);
}

.gradient-opacity {
  position: relative;
  height: 150px;
  overflow: hidden;
}

.gradient-opacity:after {
  position: absolute;
  bottom: 0;
  height: 100%;
  width: 100%;
  content: "";
  background: linear-gradient(to top,
  rgba(239, 239, 239, 1) 20%,
  rgba(239, 239, 239, 0) 80%
  );
  pointer-events: none;

}
</style>