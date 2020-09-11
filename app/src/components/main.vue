<template>
  <section>
    <UrlInput v-on:submit="submitUrl"></UrlInput>
    <Progress v-if="status" :status="status" :progressTotal="progressTotal" :progress="progress"></Progress>
    <b-tabs v-if="status === 'finished'">
      <b-tab-item label="gif">
        <img :src="result_gif" alt="result gif"/>
        <p>
        <a :href="result_gif" download>Download</a>
        </p>
      </b-tab-item>
      <b-tab-item label="mp4">
        <video controls>
          <source :src="result_mp4" type="video/mp4">
        </video>
        <p>
          <a :href="result_mp4" download>Download</a>
        </p>
      </b-tab-item>
    </b-tabs>
  </section>
</template>

<script lang="js">
import UrlInput from "./url-input.vue"
import Progress from "./progress.vue"

export default {
  data() {
    return { 
      url: "", 
      status: "", 
      id: "", 
      progress: "", 
      progressTotal:"",
      result_gif: "",
      result_mp4: ""      
    }
  },
  components: {
    UrlInput,
    Progress
  },
  methods: {
    submitUrl: function(url) {
      this.url = url
      fetch(process.env.VUE_APP_API_BASE_URL, {
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
        this.progress = 0
        this.checkStatus(r.id)
      })
    },
    checkStatus: function(id) {
      setTimeout(() => {
        if (this.status === "finished" || this.status === "error" || this.id != id)
        {
          return;
        }

        fetch(`${process.env.VUE_APP_API_BASE_URL}/${this.id}/status`, {
          headers: { 'Accept': 'application/json' }
        })
        .then(r => r.json())
        .then(r =>{
          this.status = r.status
          this.progress = r.progress
          this.progressTotal = r.progress_total
          if (this.status === "finished") {
            this.result_mp4 = r.mp4_url
            this.result_gif = r.gif_url
          }
        })

        this.checkStatus(id)
      }, 1000);

    }
  }
}
</script>
