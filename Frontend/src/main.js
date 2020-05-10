import "core-js/stable";
import "core-js/stable";
import "regenerator-runtime/runtime";
import './views/recognize/firebase'
import Vue from "vue";
import App from "./App";
import router from "./router";
import CoreuiVue from "@coreui/vue";
import { iconsSet as icons } from "./assets/icons/icons.js";
import store from "./store";
import VueSession from "vue-session";
import IdleVue from "idle-vue";
import Vuetify from "vuetify";
import { rtdbPlugin } from 'vuefire'
import { VueSpinners } from "@saeris/vue-spinners";

Vue.config.productionTip = false;
Vue.config.performance = true;
Vue.prototype.$log = console.log.bind(console);
Vue.use(CoreuiVue);
Vue.use(VueSession);
Vue.use(Vuetify);
Vue.use(rtdbPlugin);
Vue.use(VueSpinners);

const eventsHub = new Vue();
Vue.use(IdleVue, {
  eventEmitter: eventsHub,
  idleTime: 720000
}); // sets up the idle time,i.e. time left to logout the user on no activity

router.beforeEach((to, from, next) => {
  // if any of the routes in ./router.js has a meta named 'requiresAuth: true'
  // then check if the user is logged in before routing to this path:
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.loggedIn) {
      next({ name: "Login" });
    } else {
      next();
    }
  }
  // else if any of the routes in ./router.js has a meta named 'requiresLogged: true'
  // then check if the user is logged in; if true continue to home page else continue routing to the destination path
  // this comes to play if the user is logged in and tries to access the login/register page
  else if (to.matched.some(record => record.meta.requiresLogged)) {
    if (store.getters.loggedIn) {
      next({ name: "Dashboard" });
    } else {
      next();
    }
  } else {
    next();
  }
});

new Vue({
  el: "#app",
  router,
  store,
  icons,
  template: "<App/>",
  components: {
    App
  }
});
