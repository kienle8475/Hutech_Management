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
                  <p class="text-header">{{EmployeeInfo.DepartmentName}}</p>
                </div>
                <div class="col-4">
                  <p class="text-header">{{EmployeeInfo.FirstName}} {{EmployeeInfo.LastName}}</p>
                </div>
                <div class="col-4">
                  <p class="text-header">{{EmployeeInfo.EmployeeId}}</p>
                </div>
              </div>
            </div>
            <div>
              <!-- --------------------------------------------------------------------------------->
              <div id="app">
                <div class="camera-stream">
                  <video
                    ref="video"
                    id="video"
                    width="1450"
                    height="1115"
                    autoplay
                    v-on:play="detectFace"
                  ></video>
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

            <div>
              <div>
                <!-- <img style="width:90%; margin:20px" /> -->
                <template v-if="EmployeeInfo.Image!=''">
                  <img
                    id="profileImage"
                    style="height:650px; width:650px; padding: 23px; background:#ffffff3b; margin-top:20px"
                    v-bind:src="Media+EmployeeInfo.Image"
                  />
                </template>
                <template v-else>
                  <img
                    id="profileImage"
                    style="height:650px; width:650px; padding: 23px; background:#ffffff3b; margin-top:20px"
                    src="https://dummyimage.com/650x650/fff/fff.jpg"
                  />
                </template>

                <img
                  id="checkinImage"
                  style="height:470px; width:650px; padding: 23px; background:#ffffff3b; margin-top:20px"
                />
                <div class="recoginze-button">
                  <CButton color="success">SAVE</CButton>
                  <CButton @click="clearResults" color="danger">CANCEL</CButton>
                </div>
              </div>
              <!-- <img style="width:90%; margin:20px" v-bind:src="Media+EmployeeProfile.ProfileImage" /> -->
              <!-- <canvas style="height:75vh; width:90%; margin: 20px; background:white"></canvas> -->
            </div>
          </div>
        </CCol>
      </CRow>
      <CRow>
        <div class="checkin-footer">
          <span class="ml-auto">Hutech Management</span>
          <span class="mr-1">&copy; {{ new Date().getFullYear() }} by</span>
          <a href="https://mypeaga.xyz" target="_blank">Peaga inc.</a>
        </div>
      </CRow>
    </div>
  </div>
</template>
<script>
import { getAPI, BackendUrl } from "../../api/axios-base";
import { RingLoader } from "@saeris/vue-spinners";
import { EmployeeAttendanceRef, StudentCheckinRef } from "./firebase";
import * as canvas from "canvas";
import * as faceapi from "face-api.js";
var facedescriptions = [];
var facelabels = [];
var validEmployees = [];
var labeledFaceDescriptors = [];
var isCheckin = [];
var processingFace = "";
var moment = require("moment");
export default {
  name: "Department",
  data() {
    return {
      Media: "",
      loading: true,
      currentTime: null,
      EmployeeInfo: {
        EmployeeId: "EMPLOYEE ID",
        DepartmentName: "DEPARTMENT",
        Image: "",
        FirstName: "EMPLOYEE",
        LastName: "NAME"
      }
    };
  },

  methods: {
    updateCurrentTime() {
      this.currentTime = moment().format("LLLL");
    },
    // Get data label and face descriptions
    // Return LabeledFaceDescription (assign face descriptions for face ID)
    async getLabelData() {
      return Promise.all(
        facelabels.map(async (label, i, facelabels) => {
          var descriptions = [];
          var strdescription = facedescriptions[i];
          var arrdescription = strdescription.split(",");
          descriptions.push(new Float32Array(arrdescription));
          return new faceapi.LabeledFaceDescriptors(label, descriptions);
        })
      );
    },
    loadDataLabelAndDescription() {
      getAPI
        .get("face-encoding/", {
          headers: { Authorization: `Bearer ${this.$store.state.accessToken}` }
        })
        .then(async response => {
          console.log(response.data);
          for (var i = 0; i < response.data.length; i++) {
            facelabels.push(response.data[i].Employee);
            facedescriptions.push(response.data[i].Encoding);
            validEmployees.push(response.data[i].Employee);
          }
          labeledFaceDescriptors = await this.getLabelData();
          console.log(labeledFaceDescriptors);
        });
    },
    detectFace() {
      let self = this;
      const video = document.getElementById("video");
      const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.4);
      video.onloadeddata = function() {
        const canvas = document.getElementById("overlay");
        const displaySize = { width: video.width, height: video.height };
        faceapi.matchDimensions(canvas, displaySize);
        setInterval(async () => {
          const detections = await faceapi
            .detectSingleFace(video, new faceapi.SsdMobilenetv1Options())
            .withFaceLandmarks()
            .withFaceDescriptor();
          if (typeof detections !== "undefined") {
            const bestMatch = faceMatcher.findBestMatch(detections.descriptor);
            console.log(bestMatch);
            if (
              bestMatch.label != "unknown" &&
              bestMatch.label != processingFace
            ) {
              const url = "employee/".concat(bestMatch.label);
              getAPI.get(url).then(response => {
                self.EmployeeInfo = response.data;
              });
              const video = document.getElementById("video");
              const imgwidth = 604;
              const imgheight = 424;
              const canvas = document.createElement("canvas");
              canvas.width = imgwidth;
              canvas.height = imgheight;
              canvas
                .getContext("2d")
                .drawImage(video, 0, 0, imgwidth, imgheight);
              var checkinImg = document.getElementById("checkinImage");
              checkinImg.src = canvas.toDataURL();
              processingFace = bestMatch.label;
            }
            const resizedDetections = faceapi.resizeResults(
              detections,
              displaySize
            );
            canvas
              .getContext("2d")
              .clearRect(0, 0, canvas.width, canvas.height);
            faceapi.draw.drawDetections(canvas, resizedDetections);
          } else {
            processingFace = "";
            self.clearResults();
            canvas
              .getContext("2d")
              .clearRect(0, 0, canvas.width, canvas.height);
          }
        }, 1000);
      };
    },
    clearResults() {
      var checkinImg = document.getElementById("checkinImage");
      checkinImg.src = "https://dummyimage.com/650x470/fff/fff.jpg";
      this.EmployeeInfo = {
        EmployeeId: "EMPLOYEE ID",
        DepartmentName: "DEPARTMENT",
        Image: "",
        FirstName: "EMPLOYEE",
        LastName: "NAME"
      };
    }
  },
  // Start webcam when component mounted
  // mounted() {
  //   this.video = this.$refs.video;
  //   if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  //     navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
  //       this.video.srcObject = stream;
  //       this.video.play();
  //     });
  //   }
  // },
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
    this.loadDataLabelAndDescription();
    this.Media = BackendUrl;
  }
};
</script>
