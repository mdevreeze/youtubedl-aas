<template>
  <section>
    <UrlInput v-on:submit="submitUrl"></UrlInput>
    <p>{{ url }}</p>
  </section>
</template>

<script lang="js">
import UrlInput from "./url-input.vue"
import * as config from "@/config"

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
      fetch(config.API_BASE_URL, {
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
