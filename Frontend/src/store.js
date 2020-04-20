import Vue from 'vue'
import Vuex from 'vuex'
import { axiosBase } from "./api/axios-base";
import qs from "qs";
Vue.use(Vuex)

const state = {
  sidebarShow: 'responsive',
  sidebarMinimize: false,
  accessToken: localStorage.getItem("access_token") || null, // makes sure the user is logged in even after
  // refreshing the page
  refreshToken: localStorage.getItem("refresh_token") || null,
  APIData: "" // received data from the backend API is stored here.
}

const mutations = {
  toggleSidebarDesktop (state) {
    const sidebarOpened = [true, 'responsive'].includes(state.sidebarShow)
    state.sidebarShow = sidebarOpened ? false : 'responsive'
  },
  toggleSidebarMobile (state) {
    const sidebarClosed = [false, 'responsive'].includes(state.sidebarShow)
    state.sidebarShow = sidebarClosed ? true : 'responsive'
  },
  set (state, [variable, value]) {
    state[variable] = value
  },
  updateLocalStorage(state, { access, refresh }) {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    state.accessToken = access;
    state.refreshToken = refresh;
  },
  updateAccess(state, access) {
    state.accessToken = access;
  },
  destroyToken(state) {
    state.accessToken = null;
    state.refreshToken = null;
  }
}

const getters = {
  loggedIn(state) {
    return state.accessToken != null;
  }
};

const actions = {
  // run the below action to get a new access token on expiration
  refreshToken(context) {
    return new Promise((resolve, reject) => {
      axiosBase
        .post("/token/refresh/", {
          refresh: context.state.refreshToken
        }) // send the stored refresh token to the backend API
        .then(response => {
          // if API sends back new access and refresh token update the store
          console.log("New access successfully generated");
          context.commit("updateAccess", response.data.access);
          resolve(response.data.access);
        })
        .catch(err => {
          console.log("error in refreshToken Task");
          reject(err); // error generating new access and refresh token because refresh token has expired
        });
    });
  },
  logout(context) {
    if (context.getters.loggedIn) {
      return new Promise((resolve, reject) => {
        axiosBase
          .post("/token/logout/")
          .then(response => {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            context.commit("destroyToken");
          })
          .catch(err => {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            context.commit("destroyToken");
            resolve(err);
          });
      });
    }
  },
  login(context, credentials) {
    return new Promise((resolve, reject) => {
      console.log(credentials)
      // send the username and password to the backend API:
      axiosBase
        .post(
          "/auth/token/",credentials
        )
        //if successful update local storage:
        .then(response => {
          context.commit("updateLocalStorage", {
            access: response.data.access,
            refresh: response.data.refresh
          },
          ); // store the access and refresh token in localstorage
          resolve();
        })
        .catch(err => {
          console.log(err)
          reject(err);
        });
    });
  }
};

export default new Vuex.Store({
  state,
  mutations,
  getters,
  actions
})