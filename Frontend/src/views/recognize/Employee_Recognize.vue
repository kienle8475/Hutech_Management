<template>
  <div>
    <div v-if="loading">
      <ring-loader class="loading" :loading="loading" :size="40" color="#4A90E2"></ring-loader>
    </div>
    <div v-show="!loading" class="recognize">
      <CRow></CRow>
      <CRow>
        <CCol sm="8" class="recognize-form">
          <div class="recognize-block">
            <div class="recognize-header">
              <section id="app" class="section">
                <p class="time" v-text="currentTime"></p>
              </section>
            </div>
            <div>
              <img style="width:90%; margin:20px" v-bind:src="Url+'video_feed_recognize'" />
              <!-- <canvas style="height:75vh; width:90%;  margin: 20px;  background:white"></canvas> -->
            </div>
          </div>
        </CCol>
        <CCol sm="4" class="recognize-form">
          <div class="recognize-block">
            <div class="recognize-header">
              <section id="app" class="section">
                <p class="location">HUTECH MANPOWER TRAINING CENTER</p>
              </section>
            </div>
            <div>
              <img style="width:90%; margin:20px" v-bind:src="Media+EmployeeProfile.ProfileImage" />
              <!-- <canvas style="height:425px; width:90%; margin: 20px; background:white"></canvas> -->
              <div class="recognize-employee">
                <table class="table table-sm table-light">
                  <thead>
                    <tr>
                      <th scope="row">Check-in Image</th>
                      <th scope="row">Employee Info</th>
                    </tr>
                  </thead>
                  <tbody class="recognize-employee-table">
                    <tr>
                      <td rowspan="4" style="text-align:center">
                        <!-- <canvas style="height:125px; width:165px;  background:white"></canvas> -->
                        <img
                          style="width:200px; margin:5px"
                          v-bind:src="Media+EmployeeProfile.CheckinImage"
                        />
                      </td>
                    </tr>
                    <tr>
                      <td>{{EmployeeProfile.EmployeeID}}</td>
                    </tr>
                    <tr>
                      <td>{{EmployeeProfile.EmployeeName}}</td>
                    </tr>
                    <tr>
                      <td>{{EmployeeProfile.CheckinTime}}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="recoginze-button">
                <CButton color="success" @click="saveCheckin">CHECK-IN</CButton>
                <CButton color="info" @click="clearResult">CHECK-OUT</CButton>
                <CButton color="danger" @click="clearResult">CANCEL</CButton>
              </div>
            </div>
          </div>
        </CCol>
      </CRow>
    </div>
  </div>
</template>

<script>
import { getAPI, BackendUrl } from "../../api/axios-base";
import { BackendMedia } from "../../api/axios-base";
import { RingLoader } from "@saeris/vue-spinners";
import { EmployeeAttendanceRef } from "./firebase";
import swal from "sweetalert2";
var moment = require("moment");
export default {
  name: "Department",
  data() {
    return {
      Url: "",
      Media: "",
      loading: true,
      checked: " ",
      currentTime: null,
      checkinImage: "",
      checkinTime: "",
      profileImage: "",
      employeeId: "",
      employeeName: "",
      location: "4",
      EmployeeProfile: ""
    };
  },
  firebase: {
    EmployeeProfile: EmployeeAttendanceRef
  },
  methods: {
    updateCurrentTime() {
      this.currentTime = moment().format("LLLL");
      this.checkinTime = moment().format("YYYY-MM-DD hh:mm");
    },
    saveCheckin() {
      var data = {
        Employee: this.EmployeeProfile.EmployeeID,
        TimeIn: this.EmployeeProfile.CheckinTime,
        Location_id: this.location
      };
      console.log(data);
      getAPI
        .post("/checkin-employee/", data)
        .then(response => {
          console.log(response.data);
          this.clearResult();
          swal.fire({
            toast: true,
            position: "top-end",
            icon: "success",
            title: "Success",
            text: "Create Employee",
            showConfirmButton: false,
            timer: 1500
          });
        })
        .catch(e => {
          console.log(e);
          swal.fire({
            toast: true,
            position: "top-end",
            icon: "error",
            title: "Error",
            text: e.message,
            timer: 2000,
            showConfirmButton: false
          });
        });
    },
    saveCheckout() {},
    clearResult() {
      getAPI.post(`clear_result`);
    }
  },
  created() {
    setTimeout(() => {
      this.loading = false;
    }, 1000);
    setInterval(() => this.updateCurrentTime(), 1 * 1000);
    (this.Media = BackendMedia), (this.Url = BackendUrl);
  }
};
</script>
