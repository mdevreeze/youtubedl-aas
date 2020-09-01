import Vue from 'vue'
import App from './App.vue'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'

Vue.config.productionTip = false
Vue.use(Buefy)

new Vue({
  render: h => h(App),
}).$mount('#app')

var appInsights = // ... 
({ 
  samplingPercentage: 20, 
  instrumentationKey: process.env.INSTRUMENTATION_KEY
}); 

window.appInsights = appInsights; 
appInsights.trackPageView(); 
