<template>
  <section>
    <UrlInput v-on:submit="submitUrl"></UrlInput>
    <Progress v-if="status" :status="status" :progressTotal="progressTotal" :progress="progress"></Progress>
  </section>
</template>

<script lang="js">
import UrlInput from "./url-input.vue"
import Progress from "./progress.vue"
import * as config from "@/config"

export default {
  data() {
    return { 
      url: "", 
      status: "", 
      id: "", 
      progress: "", 
      progressTotal:"" 
    }
  },
  components: {
    UrlInput,
    Progress
  },
  methods: {
    submitUrl: function(url) {
      this.url = url
      fetch(config.API_BASE_URL, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          url
        })
      })
      .then(r => r.json())
      .then(r =>{
        this.id = r.id
        this.status = r.status
        this.checkStatus()
      })
    },
    checkStatus: function() {
      setTimeout(() => {
        if (this.status === "finished" || this.status === "error")
        {
          return;
        }

        fetch(`${config.API_BASE_URL}/${this.id}/status`, {
          headers: {
            'Accept': 'application/json'
          }
        })
        .then(r => r.json())
        .then(r =>{
          this.status = r.status
          this.progress = r.progress
          this.progressTotal = r.progress_total
        })

        this.checkStatus()
      }, 1000);

    }
  }
}
</script>
