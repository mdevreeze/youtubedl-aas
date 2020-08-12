<template>
  <section>
    <UrlInput v-on:submit="submitUrl"></UrlInput>
    <p>{{ url }}</p>
  </section>
</template>

<script lang="js">
import UrlInput from "./url-input.vue"
export default {
  data() {
    return { url: "", status: "none" }
  },
  components: {
    UrlInput
  },
  methods: {
    submitUrl: function(url) {
      this.url = url
      fetch('https://8000-c83fa473-6d1c-4b18-8f0b-aab8d4e1eb58.ws-us02.gitpod.io/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          url
        })
      })
      .then(r => r.json())
      .then(r =>{
        alert(r)
        this.status = r.status
      })
    }
  }
}
</script>
