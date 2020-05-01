<template>
  <div>
    <div v-if="loading">
      <ring-loader class="loading" :loading="loading" :size="40" color="#4A90E2"></ring-loader>
    </div>
    <div v-show="!loading" class="checkin">
      <CRow></CRow>
      <CRow>
        <CCol sm="8" class="recognize-form">
          <div class="checkin-block">
            <div class="recognize-header">
              <section class="section">
                <p class="text-header" v-text="currentTime"></p>
              </section>
            </div>
            <div class="checkin-status container">
              <div class="row status-bar">
                <div class="col-4">
                  <p class="text-header">HỆ THỐNG THÔNG TIN</p>
                </div>
                <div class="col-6">
                  <p class="text-header">1711062340</p>
                </div>
                <div class="col-2">
                  <p class="text-header">00:30:00</p>
                </div>
              </div>
            </div>
            <div>
              <!-- --------------------------------------------------------------------------------->
              <div id="app">
                <div>
                  <video ref="video" id="video" width="100%" style="padding: 60px" autoplay></video>
                  <br />
                </div>
              </div>
              <!-- --------------------------------------------------------------------------------->
            </div>
          </div>
        </CCol>
        <CCol sm="4" class="recognize-form">
          <div class="checkin-block">
            <div class="recognize-header">
              <section class="section">
                <p class="text-header">HUTECH MANPOWER TRAINING CENTER</p>
              </section>
            </div>
            <div class="checkin-status container">
              <div class="row status-bar">
                <div class="col-6">
                  <p class="text-header">E-01-01</p>
                </div>
                <div class="col-6">
                  <p class="text-header">20 / 30</p>
                </div>
              </div>
            </div>
            <div>
              <!-- <img style="width:90%; margin:20px" v-bind:src="Media+EmployeeProfile.ProfileImage" /> -->
              <!-- <canvas style="height:75vh; width:90%; margin: 20px; background:white"></canvas> -->
            </div>
          </div>
        </CCol>
      </CRow>
    </div>
  </div>
</template>
<script>
import { getAPI } from "../../api/axios-base";
import { RingLoader } from "@saeris/vue-spinners";
import { EmployeeAttendanceRef } from "./firebase";
import * as canvas from "canvas";
import * as faceapi from "face-api.js";
var moment = require("moment");
export default {
  name: "Department",
  data() {
    return {
      loading: true,
      currentTime: null,
      timeLeft: "00:00:30"
    };
  },
  firebase: {
    EmployeeProfile: EmployeeAttendanceRef
  },
  methods: {
    updateCurrentTime() {
      this.currentTime = moment().format("LLLL");
    }
  },
  loadModel() {
    Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri("/models"),
      faceapi.nets.faceLandmark68Net.loadFromUri("/models"),
      faceapi.nets.faceRecognitionNet.loadFromUri("/models"),
      faceapi.nets.faceExpressionNet.loadFromUri("/models")
    ]).then(startVideo);
  },
  mounted() {
    this.video = this.$refs.video;
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
        this.video.srcObject = stream;
        this.video.play();
      });
    }
  },
  created() {
    setTimeout(() => {
      this.loading = false;
    }, 1000);
    setInterval(() => this.updateCurrentTime(), 1 * 1000);
  }
};
</script>
