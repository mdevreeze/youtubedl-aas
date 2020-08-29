<template>
  <section class="section">
    <h2 v-if="status">{{ capStatus }}...</h2>
    <b-progress :value="currentPercentage" show-value format="percent"></b-progress>
  </section>
</template>

<script>
export default {
  props: [ 'progress', 'progressTotal', 'status' ],
  computed: {
    currentPercentage: function() {
      var progress = (this.progress / this.progressTotal) * 100
      return progress
    },
    capStatus: function() {
      if (!this.status) return ''
      return this.status.charAt(0).toUpperCase() + this.status.slice(1)
    }
  },
  
}
</script>
