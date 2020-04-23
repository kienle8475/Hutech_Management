<template>
  <div>
    <div v-if="loading">
      <ring-loader class="loading" :loading="loading" :size="40" color="#4A90E2"></ring-loader>
    </div>
    <div v-show="!loading" class="recognize">
      <CRow>
        <CCol sm="6" class="recognize-form"></CCol>
        <CCol sm="5" class="recognize-form">
          <div class="recognize-block">
            <div class="recognize-header"></div>
            <div>
              <CButtonToolbar class="recognize-toolbar">
                <input
                  class="mb-0 form-control recognize-input"
                  placeholder="Input Your ID"
                  v-model="StudentID"
                />
                <CButtonGroup class="mb-0 recognize-button">
                  <CButton color="success" class="recognize-button" @click="setStudentID">Submit</CButton>
                </CButtonGroup>
              </CButtonToolbar>
            </div>
            <div>
              <img class="recognize-camera" src="http://127.0.0.1:8000/video_feed_recognize" />
            </div>
            <div class="recognize-footer"></div>
          </div>
        </CCol>
        <CCol sm="1" class="recognize-form"></CCol>
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
