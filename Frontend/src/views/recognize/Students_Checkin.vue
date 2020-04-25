<template>
  <div>
    <div v-if="loading">
      <ring-loader class="loading" :loading="loading" :size="40" color="#4A90E2"></ring-loader>
    </div>
    <div v-show="!loading" class="compare">
      <CRow>
        <CCol sm="6" class="compare-form"></CCol>
        <CCol sm="5" class="compare-form">
          <div class="compare-block">
            <div class="compare-header"></div>
            <div>
              <CButtonToolbar class="compare-toolbar">
                <input
                  class="mb-0 form-control compare-input"
                  placeholder="Input Your ID"
                  v-model="StudentID"
                />
                <CButtonGroup class="mb-0 compare-button">
                  <CButton color="success" class="compare-button" @click="setStudentID">Submit</CButton>
                </CButtonGroup>
              </CButtonToolbar>
            </div>
            <div>
              <img class="compare-camera" src="/imgs/camera_background.jpg" />
            </div>
            <div class="compare-footer"></div>
          </div>
        </CCol>
        <CCol sm="1" class="compare-form"></CCol>
      </CRow>
    </div>
  </div>
</template>

<script>
import { RingLoader } from "@saeris/vue-spinners";
import { StudentRef } from "./firebase";
export default {
  name: "Department",
  data() {
    return {
      loading: true,
      StudentID: ""
    };
  },
  methods: {
    setStudentID() {
      var data = { ID: this.StudentID };
      console.log(this.StudentID);
      StudentRef.update(data);
    }
  },
  created() {
    setTimeout(() => {
      this.loading = false;
    }, 1000);
  }
};
</script>
