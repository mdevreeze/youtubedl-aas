<template>
  <section class="section">
    <b-field label="URL:">
      <b-input 
        placeholder="Enter full video URL here" 
        icon="magnify"
        v-model="url"
        rounded>
        </b-input>
    </b-field>
    <b-button @click="submit">Submit</b-button>
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
      submit() {
          this.$emit('submit', this.url)
      }
    }
  }
</script>
