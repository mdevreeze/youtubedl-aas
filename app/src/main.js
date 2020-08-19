import Vue from 'vue'
import App from './App.vue'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import * as config from "./config"

Vue.config.productionTip = false
Vue.use(Buefy)

new Vue({
  render: h => h(App),
}).$mount('#app')

var appInsights = // ... 
({ 
  samplingPercentage: 20, 
  instrumentationKey: config.INSTRUMENTATION_KEY
}); 

window.appInsights = appInsights; 
appInsights.trackPageView(); 
