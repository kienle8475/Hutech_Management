<template>
  <div>
    <div v-if="loading">
      <ring-loader class="loading" :loading="loading" :size="40" color="#4A90E2"></ring-loader>
    </div>
    <div v-show="!loading">
      <CRow>
        <CCol lg="6" class="department-form">
          <CDepartment></CDepartment>
        </CCol>
        <CCol lg="6" class="location-form">
          <CLocation></CLocation>
        </CCol>
      </CRow>
    </div>
  </div>
</template>

<script>
import { RingLoader } from "@saeris/vue-spinners";
import { mapState } from "vuex";
import ComLocation from "./ComLocation";
import ComDepartment from "./ComDepartment";

export default {
  name: "Department",
  components: {
    CLocation: ComLocation,
    CDepartment: ComDepartment
  },
  data() {
    return {
      loading: true
    };
  },
  created() {
    setTimeout(() => {
      this.loading = false;
    }, 1000);
  }
};
</script>
