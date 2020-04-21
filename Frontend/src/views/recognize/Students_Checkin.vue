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
                <Input class="mb-0 form-control recognize-input" placeholder="Input Your ID" />
                <CButtonGroup class="mb-0 recognize-button">
                  <CButton color="success" class="recognize-button">Submit</CButton>
                </CButtonGroup>
              </CButtonToolbar>
            </div>
            <div>
              <img class="recognize-camera" src="/imgs/camera_background.jpg" />
            </div>
            <div class="recognize-footer">
              <td>
                <span class="display-4">Student Attendance System</span>
              </td>
            </div>
          </div>
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
