<template>
  <div>
    <div v-if="loading">
      <ring-loader class="loading" :loading="loading" :size="40" color="#4A90E2"></ring-loader>
    </div>
    <div v-show="!loading">
      <CCardHeader>
        <h4>Student Attendance System</h4>
      </CCardHeader>
      <CRow>
        <CCol sm="3" class="recognize-form">
          <CCard>
            <CCardBody>
              <CCarousel arrows indicators animate height="90vh">
                <CCarouselItem image="https://picsum.photos/1024/480/?image=52" />
                <CCarouselItem image="https://picsum.photos/1024/480/?image=52" />
              </CCarousel>
            </CCardBody>
          </CCard>
        </CCol>
        <CCol sm="6" class="recognize-form">
          <CCard>
            <CCardBody>
              <div>
                <CInput type="number"></CInput>
                <CButton color="success">Submit</CButton>
              </div>
              <img src="http://127.0.0.1:8000/video_feed_compare" />
            </CCardBody>
          </CCard>
        </CCol>
        <CCol sm="3" class="recognize-form">
          <CCard>
            <CCardBody></CCardBody>
          </CCard>
        </CCol>
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
