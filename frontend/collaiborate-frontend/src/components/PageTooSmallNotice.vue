<template>

  <div style="margin: 30px">
    <h2 style="word-wrap: break-word; font-size: 32px">Neighborhood traces: When your neighborhood changes one layer at a time</h2>
    <p style="font-size: 20px">A Journey into CNNs for Sketch Classification</p>

    <p>Unfortunately, our website isn't currently optimized for smaller screens. We invite you to enjoy the story on a Desktop or Tablet for the best reading experience!</p>
  </div>

  <div style="width: 100%; height: 100px; display: flex; justify-content: center; align-items: center">
  <img  style="width: 70px;" :src="'/face'+Math.floor(Math.random()*8)+'.png'"/>
  <img  style="width: 70px;" src="/phone.png"/>
  </div>
</template>

<script>
export default {
  name: "PageTooSmallNotice"
}
</script>

<style scoped>

</style>