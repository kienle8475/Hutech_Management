<template>
  <CCol>
    <CCol class="location-input">
      <CCardBody>
        <CCard>
          <CCardHeader>
            <h4>Location</h4>
          </CCardHeader>
          <CCardBody>
            <CForm>
              <CInput placeholder="Name" v-model="locationname" required>
                <template #prepend-content></template>
              </CInput>
              <CInput placeholder="Address" v-model="address" required>
                <template #prepend-content></template>
              </CInput>
              <div class="form-group form-actions">
                <CButton @click="createLocation" size="sm" color="success">Submit</CButton>
              </div>
            </CForm>
          </CCardBody>
        </CCard>
      </CCardBody>
    </CCol>
    <CCol lg="12" class="location-table">
      <CCardBody>
        <CDataTable
          :items="items"
          :fields="fields"
          table-filter
          items-per-page-select
          :items-per-page="10"
          sorter
          pagination
        >
          <template #Edit="{item}">
            <td class="py-2">
              <CButton
                @click="(toggled = true), getLocationDetail(item)"
                color="info"
                square
                size="sm"
                variant="outline"
              >Edit</CButton>
            </td>
          </template>
          <template #Delete="{item}">
            <td class="py-2">
              <CButton
                @click="deleteLocation(item)"
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
  </CCol>
</template>

<script>
import { getAPI, axiosBase, axiosData } from "../../api/axios-base";
import swal from "sweetalert2";
var items = [];
const fields = [
  { key: "LocationName", label: "Name", _style: "width:25%" },
  { key: "Address", _style: "width:55%" },
  { key: "Edit", _style: "width:10%", sorter: false },
  { key: "Delete", _style: "width:10%", sorter: false }
];
export default {
  name: "ComLocation",
  data() {
    return {
      items: items.map(item => {
        return { ...item };
      }),
      fields,
      toggled: false,
      locationname: "",
      address: "",
      locationname_update: "",
      address_update: ""
    };
  },
  methods: {
    getLocation() {
      getAPI
        .get("location/", {
          headers: { Authorization: `Bearer ${this.$store.state.accessToken}` }
        })
        .then(response => {
          this.items = response.data;
          console.log("Data loading success");
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
    getLocationDetail(item) {
      console.log(item.DepartmentId);
      (this.departmentid_update = item.DepartmentId),
        (this.departmentname_update = item.DepartmentName);
    },
    createLocation() {
      var data = {
        DepartmentId: this.departmentid,
        DepartmentName: this.departmentname
      };
      getAPI
        .post("/create-department/", data)
        .then(response => {
          this.getDepartment();
          this.resetInputForm();
          console.log(response.data);
          swal.fire({
            toast: true,
            position: "top-end",
            icon: "success",
            title: "Success",
            text: "Create department",
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
            text: "Department invalid or already exists",
            timer: 2000,
            showConfirmButton: false
          });
        });
    },
    updateLocation() {
      var data = {
        DepartmentId: this.departmentid_update,
        DepartmentName: this.departmentname_update
      };
      getAPI
        .post(`update-department/${data.DepartmentId}`, data)
        .then(response => {
          this.getDepartment();
          swal.fire({
            toast: true,
            position: "top-end",
            icon: "success",
            title: "Success",
            text: "Update department",
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
    },
    deleteLocation(item) {
      console.log(item.DepartmentId);
      swal
        .fire({
          toast: true,
          position: "top",
          icon: "warning",
          title: "Delete",
          text: `"${item.DepartmentName}"`,
          showCancelButton: true,
          showConfirmButton: true
        })
        .then(result => {
          if (result.value) {
            getAPI
              .delete(`delete-department/${item.DepartmentId}`)
              .then(response => {
                this.getDepartment();
                swal.fire({
                  toast: true,
                  position: "top-end",
                  icon: "success",
                  title: "Success",
                  text: "Delete department",
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
    },
    resetInputForm() {
      (this.departmentid = ""), (this.departmentname = "");
    }
  },
  created() {
    this.getLocation();
  }
};
</script>
