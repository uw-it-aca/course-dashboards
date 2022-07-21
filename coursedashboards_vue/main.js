import { createApp } from "vue";
import App from "./app.vue";
import router from "./router";
import store from "./store";

import VueGtag from "vue-gtag-next";
import { Vue3Mq } from "vue3-mq";

import "@popperjs/core";

// bootstrap js
import "bootstrap";

// custom bootstrap theming
import "./css/custom.scss";

const app = createApp(App);

// MARK: google analytics data stream measurement_id
const gaCode = document.body.getAttribute("data-google-analytics");
const debugMode = document.body.getAttribute("data-django-debug");

// Set csrftoken for all subsequent axios requests
// Probably a better way to do this with axios.create()
import axios from "axios";
const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
axios.defaults.headers.common["X-CSRFToken"] = csrftoken;

app.config.productionTip = false;

// vue-gtag-next
app.use(VueGtag, {
  isEnabled: debugMode == "false",
  property: {
    id: gaCode,
    params: {
      anonymize_ip: true,
    },
  },
});

// vue-mq (media queries)
app.use(Vue3Mq, {
  breakpoints: {
    // preset: 'bootstrap5'
    // xs: 0,
    // breakpoints == min-widths of next size
    mobile: 0, // tablet begins 768px
    tablet: 768, // desktop begins 992px
    desktop: 992,
  },
});
app.use(router);
app.use(store);

app.mount("#app");
