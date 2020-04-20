<template>
  <div>
    <div v-if="loading">
      <ring-loader class="loading" :loading="loading" :size="40" color="#4A90E2"></ring-loader>
    </div>
    <div v-show="!loading">
      <CRow>
        <CCol sm="7" class="recognize-form"></CCol>
        <CCol sm="4" class="recognize-form">
          <CCard>
            <CCardHeader>Employee Attendance System</CCardHeader>
            <CCardBody>
              <!--<img src="http://127.0.0.1:8000/video_feed_recognize"/> -->
            </CCardBody>
          </CCard>
        </CCol>
        <CCol sm="1" class="recognize-form"></CCol>
      </CRow>
    </div>
  </div>
</template>

<script>
import { RingLoader } from "@saeris/vue-spinners";
import { mapState } from "vuex";

export default {
  name: "Department",
  data() {
    return {
      loading: true
    };
  },
  methods: {},
  created() {
    setTimeout(() => {
      this.loading = false;
    }, 1000);
  }
};
</script>
