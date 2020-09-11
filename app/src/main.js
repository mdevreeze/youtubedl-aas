import Vue from 'vue'
import App from './App.vue'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import { ApplicationInsights } from '@microsoft/applicationinsights-web'

Vue.config.productionTip = false
Vue.use(Buefy)

new Vue({
  render: h => h(App),
}).$mount('#app')

var appInsights = new ApplicationInsights({ config: {
  samplingPercentage: 20, 
  instrumentationKey: process.env.VUE_APP_INSTRUMENTATION_KEY
}}); 
appInsights.loadAppInsights();

window.appInsights = appInsights; 
appInsights.trackPageView(); 
