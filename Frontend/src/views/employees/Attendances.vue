<template>
  <div>
    <div v-if="loading">
      <ring-loader class="loading" :loading="loading" :size="40" color="#4A90E2"></ring-loader>
    </div>
    <div v-show="!loading">
      <CCol class="employee-table">
        <CCardHeader>
          <h4>Attendance Manage</h4>
        </CCardHeader>
        <div class="my-container">
          <div class="row">
            <div class="col-lg-2 col-sm-1 col-md-1">
              <CInput label="Start Day" type="date"></CInput>
            </div>
            <div class="col-lg-2 col-sm-1 col-md-1">
              <CInput label="End Day" type="date"></CInput>
            </div>
            <div class="col-lg-2 col-sm-1 col-md-1">
              <CInput label="Employee Name" type="text"></CInput>
            </div>
            <div class="col-lg-2 col-sm-1 col-md-1">
              <CInput label="Location" type="text"></CInput>
            </div>
            <div class="col-lg-3 col-sm-1 col-md-1 filter-taskbar">
              <CButton color="info">Apply</CButton>
              <CButton class="mx-1" color="success" variant="outline">
                <JsonCSV :data="items" :name="dataFile">Export</JsonCSV>
              </CButton>
            </div>
          </div>
        </div>
        <hr class="d-sm-down-none" />
        <CCardBody>
          <CDataTable
            :items="items"
            :fields="fields"
            column-filter
            items-per-page-select
            :items-per-page="5"
            sorter
            pagination
            class="attendance-table table table-bordered"
            id="dataTable"
          >
            <template #TimeIn="{item}">
              <td class="py-2">
                <span>{{new Date(item.TimeIn).toLocaleString('en-GB', { timeZone: 'UTC' })}}</span>
              </td>
            </template>
            <template #TimeOut>
              <td class="py-2">
                <!-- <span>{{new Date(item.TimeOut).toLocaleString('en-GB', { timeZone: 'UTC' })}}</span> -->
              </td>
            </template>
            <template #Imagein="{item}">
              <td class="py-2">
                <img
                  height="85"
                  v-bind:src="'http://127.0.0.1:8000' + item.ImageIn"
                  onclick="window.open(this.src)"
                  style="cursor: pointer;"
                />
              </td>
            </template>
            <template #Imageout>
              <td class="py-2">
                <!-- <img
                  height="65"
                  v-bind:src="'http://127.0.0.1:8000' + item.ImageOut"
                  onclick="window.open(this.src)"
                  style="cursor: pointer;"
                />-->
              </td>
            </template>
            <template #Delete="{item}">
              <td class="py-2">
                <CButton
                  @click="deleteAttendance(item)"
                  color="danger"
                  square
                  size="sm"
                  variant="outline"
                >Delete</CButton>
              </td>
            </template>
          </CDataTable>
        </CCardBody>
      </CCol>
    </div>
  </div>
</template>

<script>
import { getAPI } from "../../api/axios-base";
import { mapState } from "vuex";
import swal from "sweetalert2";
import JsonCSV from "vue-json-csv";
var items = [];
const fields = [
  { key: "id", label: "#", sorter: false, _style: "width: 4%" },
  { key: "Employee", label: "Employee ID", sorter: false },
  { key: "EmployeeName", label: "Name", sorter: true },
  { key: "Status", label: "Status", sorter: true, _style: "width: 7%" },
  { key: "LocationName", label: "Location", sorter: true, _style: "width: 7%" },
  { key: "TimeIn", label: "Time In", sorter: false },
  { key: "TimeOut", label: "Time Out", sorter: false },
  {
    key: "Imagein",
    label: "Image In",
    sorter: false,
    _style: "width: 9%"
  },
  {
    key: "Imageout",
    label: "Image Out",
    sorter: false,
    _style: "width: 9%"
  },
  { key: "Delete", sorter: false, _style: "width:4%" }
];
export default {
  name: "Attendance",
  data() {
    return {
      items: items.map((item, id) => {
        return { ...item, id };
      }),
      fields,
      loading: true,
      dataFile: "Report_Attendance.csv"
    };
  },
  components: {
    JsonCSV: JsonCSV
  },
  methods: {
    getAttendance() {
      getAPI
        .get("attendance/", {
          headers: { Authorization: `Bearer ${this.$store.state.accessToken}` }
        })
        .then(response => {
          this.items = response.data;
          console.log("Data loading success");
          console.log(this.items);
        })
        .catch(err => {
          console.log(err);
          swal.fire({
            toast: true,
            position: "top-end",
            icon: "error",
            title: "Error",
            text: "Network error",
            showConfirmButton: false,
            timer: 3000
          });
        });
    },
    deleteAttendance(item) {
      console.log(item.id);
      swal
        .fire({
          toast: true,
          position: "top",
          icon: "warning",
          title: "Delete",
          text: "Delete this record",
          showCancelButton: true,
          showConfirmButton: true
        })
        .then(result => {
          if (result.value) {
            var deleteIndex = this.items.findIndex(
              index => index.id == item.id
            );
            this.items.splice(deleteIndex, 1);
            getAPI
              .delete(`delete-attendance/${item.id}`)
              .then(response => {
                // this.getAttendance();
                swal.fire({
                  toast: true,
                  position: "top-end",
                  icon: "success",
                  title: "Success",
                  text: "Delete record",
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
                  text: "Something wrong!",
                  timer: 2000,
                  showConfirmButton: false
                });
              });
          }
        });
    }
  },
  created() {
    this.getAttendance();
    setTimeout(() => {
      this.loading = false;
    }, 1000);
  }
};
</script>