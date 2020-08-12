<template>
  <section>
    <b-field label="URL:">
      <b-input 
        placeholder="Enter full video URL here" 
        icon="magnify"
        v-model="url"
        rounded>
        </b-input>
    </b-field>
    <b-button @click="clickMe">Click Me</b-button>
  </section>
</template>

<script lang="js">
  export default {
    data() {
      return {
        url: ''
      }
    },
    methods: {
      clickMe() {
          this.$emit('submit', this.url)
      }
    }
  }
</script>
