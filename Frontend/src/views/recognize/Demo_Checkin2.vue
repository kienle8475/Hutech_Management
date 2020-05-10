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
                  <p class="text-header">{{Student.StudentID}}</p>
                </div>
                <div class="col-2">
                  <CButton
                    class="text-header"
                    color="success"
                    variant="outline"
                    @click="takePicture()"
                  >Checkin</CButton>
                </div>
              </div>
            </div>
            <div>
              <!-- --------------------------------------------------------------------------------->
              <div id="app">
                <div class="camera-stream">
                  <video ref="video" id="video" width="1450" height="1115" autoplay></video>
                  <canvas id="overlay" width="1450" height="1115" />
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
              <img
                id="img"
                style="height:470px; width:650px; padding: 23px; background:#ffffff3b; margin-top:20px"
              />
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
import { EmployeeAttendanceRef, StudentCheckinRef } from "./firebase";
import * as canvas from "canvas";
import * as faceapi from "face-api.js";
var validEmployees = [];
var isCheckin = [];
var moment = require("moment");

export default {
  name: "Department",
  data() {
    return {
      loading: true,
      currentTime: null,
      timeLeft: "00:00:30",
      Student: ""
    };
  },
  firebase: {
    Student: StudentCheckinRef
  },
  methods: {
    updateCurrentTime() {
      this.currentTime = moment().format("LLLL");
    },
    // Using for get ID from barscan or qrcode scan
    // Return Student/Employee ID
    getInputID() {
      StudentCheckinRef.on("value", snap => {
        var Student = snap.val();
        if (this.Student != null) {
          console.log(validEmployees);
          if (validEmployees.includes(this.Student["StudentID"])) {
            console.log(Student["StudentID"]);
            return Student;
          } else {
            console.log(false);
            return false;
          }
        }
      });
    },
    // Get data label and face descriptions
    // Return LabeledFaceDescription (assign face descriptions for face ID)
    // detectFace() {
    //   const video = document.getElementById("video");
    //   video.onloadeddata = function() {
    //     const canvas = document.getElementById("overlay");
    //     console.log(canvas.width, canvas.height);
    //     const displaySize = { width: video.width, height: video.height };
    //     faceapi.matchDimensions(canvas, displaySize);
    //     setInterval(async () => {
    //       const detections = await faceapi.detectSingleFace(
    //         video,
    //         new faceapi.SsdMobilenetv1Options()
    //       );
    //       if (typeof detections !== "undefined") {
    //         const resizedDetections = faceapi.resizeResults(
    //           detections,
    //           displaySize
    //         );
    //         canvas
    //           .getContext("2d")
    //           .clearRect(0, 0, canvas.width, canvas.height);
    //         faceapi.draw.drawDetections(canvas, resizedDetections);
    //       } else {
    //         canvas
    //           .getContext("2d")
    //           .clearRect(0, 0, canvas.width, canvas.height);
    //       }
    //     }, 1000);
    //   };
    // },
    takePicture() {
      var video = document.getElementById("video");
      var canvas = document.createElement("canvas");
      console.log(video.width, video.height);
      canvas.width = 604;
      canvas.height = 424;
      var context = canvas.getContext("2d");
      context.drawImage(video, 0, 0, 604, 424);
      var img = document.getElementById("img");
      img.src = canvas.toDataURL();
    }
  },
  // Start webcam when component mounted
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
    setInterval(() => this.updateCurrentTime(), 1 * 1000);
    Promise.all([
      faceapi.nets.ssdMobilenetv1.loadFromUri("/models"),
      faceapi.nets.faceLandmark68Net.loadFromUri("/models"),
      faceapi.nets.faceRecognitionNet.loadFromUri("/models")
    ]).then(() => {
      setTimeout(() => {
        this.loading = false;
      }, 100);
    });
    // this.getInputID();
  }
};
</script>
