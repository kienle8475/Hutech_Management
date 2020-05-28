<template>
  <div>
    <div v-if="loading">
      <ring-loader class="loading" :loading="loading" :size="40" color="#4A90E2"></ring-loader>
    </div>
    <div v-show="!loading">
      <CCol class="employee-table">
        <CCardHeader>
          <h4>Employees Manager</h4>
        </CCardHeader>
        <CButtonToolbar class="button-toolbar">
          <CButtonGroup size="sm" class="mx-1">
            <td>
              <CButton color="success" @click="toggled_add = true">New Staff</CButton>
              <CButton class="mx-1" color="success" variant="outline">
                <JsonCSV :data="items" :name="dataFile" :fiels="export_fields">Export</JsonCSV>
              </CButton>
            </td>
          </CButtonGroup>
        </CButtonToolbar>
        <CCardBody>
          <CDataTable
            :items="items"
            :fields="fields"
            table-filter
            items-per-page-select
            :items-per-page="5"
            sorter
            pagination
            class="employee-table"
          >
            <template #Image="{item}">
              <td class="py-2">
                <img
                  height="65"
                  v-bind:src="'http://127.0.0.1:8000' + item.Image"
                  onclick="window.open(this.src)"
                  style="cursor: pointer;"
                />
              </td>
            </template>
            <template #Edit="{item}">
              <td class="py-2">
                <CButton
                  @click="(toggled_update = true), getEmployeeDetail(item)"
                  color="info"
                  square
                  size="sm"
                  variant="outline"
                >Edit</CButton>
              </td>
            </template>
            <template #Disable="{item}">
              <td class="py-2">
                <CButton
                  @click="deleteEmployee(item)"
                  color="warning"
                  square
                  size="sm"
                  variant="outline"
                >Disable</CButton>
              </td>
            </template>
            <template #Delete="{item}">
              <td class="py-2">
                <CButton
                  @click="deleteEmployee(item)"
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
      <!--Create -->
      <CModal
        title="Create Employees"
        color="secondary"
        :closeOnBackdrop="false"
        :show.sync="toggled_add"
      >
        <CForm>
          <CInput placeholder="ID" v-model="employeeid">
            <template #prepend-content></template>
          </CInput>
          <CInput placeholder="First Name" v-model="firstname">
            <template #prepend-content></template>
          </CInput>
          <CInput placeholder="Last Name" v-model="lastname">
            <template #prepend-content></template>
          </CInput>
          <CInput placeholder="Birthday" v-model="dateofbirth" type="date">
            <template #prepend-content></template>
          </CInput>
          <select class="custom-select custom-select-md mb-3" v-model="gender" placeholder="Gender">
            <option value disabled selected>Gender</option>
            <option
              v-for="option in genders"
              v-bind:value="option.value"
              v-bind:key="option.value"
            >{{ option.label }}</option>
          </select>
          <select
            class="custom-select custom-select-md mb-3"
            v-model="departmentid"
            placeholder="Department"
          >
            <option value disabled selected>Department</option>
            <option
              v-for="option in Departments"
              v-bind:value="option.DepartmentId"
              v-bind:key="option.DepartmentId"
            >{{ option.DepartmentName }}</option>
          </select>
          <CInput placeholder="Phone Number" v-model="phone" type="text">
            <template #prepend-content></template>
          </CInput>
          <CInput placeholder="Email" v-model="email" type="Email">
            <template #prepend-content></template>
          </CInput>
          <CButton
            block
            class="button-add-image"
            color="secondary"
            variant="outline"
            @click="toggle_image"
          >Choose profile image</CButton>
          <my-upload
            field="img"
            @crop-success="cropSuccess"
            @crop-upload-success="cropUploadSuccess"
            @crop-upload-fail="cropUploadFail"
            v-model="toggled_image"
            :width="800"
            :height="800"
            img-format="png"
            lang-type="en"
            :noCircle="true"
          ></my-upload>
          <div v-if="loading_api">
            <ring-loader class="loading" :loading="loading_api" :size="40" color="#4A90E2"></ring-loader>
          </div>
          <div v-show="!loading_api">
            <img id="profile_image" class="image_profile_upload" :src="imgDataUrl" />
          </div>
        </CForm>
        <template #footer>
          <CButton @click="(toggled_add = false), resetInputForm()" color="secondary">Cancel</CButton>
          <CButton
            @click="(toggled_add = false), createEmployee()"
            color="success"
            v-bind:disabled="!profile_isvalid"
          >Submit</CButton>
        </template>
      </CModal>
      <!--Update -->
      <CModal
        title="Update Employees"
        color="success"
        :closeOnBackdrop="false"
        :show.sync="toggled_update"
      >
        <CForm>
          <CInput placeholder="ID" v-model="employeeid_update" disabled>
            <template #prepend-content></template>
          </CInput>
          <CInput placeholder="First Name" v-model="firstname_update">
            <template #prepend-content></template>
          </CInput>
          <CInput placeholder="Last Name" v-model="lastname_update">
            <template #prepend-content></template>
          </CInput>
          <CInput placeholder="Birthday" v-model="dateofbirth_update" type="date">
            <template #prepend-content></template>
          </CInput>
          <select
            class="custom-select custom-select-md mb-3"
            v-model="gender_update"
            placeholder="Gender"
          >
            <option value disabled selected>Gender</option>
            <option
              v-for="option in genders"
              v-bind:value="option.value"
              v-bind:key="option.value"
            >{{ option.label }}</option>
          </select>
          <select
            class="custom-select custom-select-md mb-3"
            v-model="departmentid_update"
            placeholder="Department"
          >
            <option value disabled selected>Department</option>
            <option
              v-for="option in Departments"
              v-bind:value="option.DepartmentId"
              v-bind:key="option.DepartmentId"
            >{{ option.DepartmentName }}</option>
          </select>
          <CInput placeholder="Phone Number" v-model="phone_update" type="text">
            <template #prepend-content></template>
          </CInput>
          <CInput placeholder="Email" v-model="email_update" type="Email">
            <template #prepend-content></template>
          </CInput>
          <CButton
            disabled
            block
            class="button-add-image"
            color="secondary"
            variant="outline"
            @click="toggle_image"
          >Choose profile image</CButton>
        </CForm>
        <template #footer>
          <CButton @click="toggled_update = false" color="secondary">Cancel</CButton>
          <CButton @click="(toggled_update = false), updateEmployee()" color="success">Submit</CButton>
        </template>
      </CModal>
    </div>
  </div>
</template>

<script>
import { getAPI } from "../../api/axios-base";
import { mapState } from "vuex";
import swal from "sweetalert2";
import Vue from "vue";
import myUpload from "vue-image-crop-upload/upload-2.vue";
import JsonCSV from "vue-json-csv";
import "babel-polyfill"; // es6 shim
import * as faceapi from "face-api.js";

var items = [];
var Departments = [];
const fields = [
  { key: "EmployeeId", label: "ID" },
  { key: "FirstName", label: "First Name", _style: "max width:5%" },
  { key: "LastName", label: "Last Name" },
  { key: "DateOfBirth", label: "Birth", sorter: false },
  { key: "Gender", label: "Gender", sorter: false },
  {
    key: "DepartmentName",
    label: "Department",
    sorter: false
  },
  { key: "Phone", label: "Phone", sorter: false },
  { key: "Email", label: "Email", sorter: false },
  { key: "Image", label: "Image", sorter: false },
  { key: "Edit", sorter: false, _style: "width:2%" },
  { key: "Disable", sorter: false, _style: "width:3%" },
  { key: "Delete", sorter: false, _style: "width:2%" }
];
const export_fields = [
  "EmployeeId",
  "FirstName",
  "LastName",
  "DepartmentName",
  "Gender",
  "Image"
];
const genders = [
  { value: "Female", label: "Female" },
  { value: "Male", label: "Male" }
];
export default {
  name: "Employee",
  data() {
    return {
      items: items.map(item => {
        return { ...item };
      }),
      Departments: Departments.map(Department => {
        return { ...Department };
      }),
      fields,
      export_fields,
      genders,
      Departments,
      loading: true,
      loading_api: false,
      toggled_add: false,
      toggled_update: false,
      toggled_image: false,
      profile_isvalid: false,
      imgDataUrl: "",
      employeeid: "",
      firstname: "",
      lastname: "",
      dateofbirth: "",
      gender: "",
      departmentid: "",
      phone: "",
      email: "",
      image: "",
      employeeid_update: "",
      firstname_update: "",
      lastname_update: "",
      dateofbirth_update: "",
      gender_update: "",
      departmentid_update: "",
      phone_update: "",
      email_update: "",
      image_update: "",
      // facedescription: "",
      dataFile: "Employees.csv"
    };
  },
  components: {
    "my-upload": myUpload,
    JsonCSV: JsonCSV
  },
  methods: {
    getEmployee() {
      getAPI
        .get("employee/", {
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
    getEmployeeDetail(item) {
      console.log(item.EmployeeId);
      (this.employeeid_update = item.EmployeeId),
        (this.firstname_update = item.FirstName),
        (this.lastname_update = item.LastName),
        (this.dateofbirth_update = item.DateOfBirth),
        (this.gender_update = item.Gender),
        (this.departmentid_update = item.Department),
        (this.phone_update = item.Phone),
        (this.email_update = item.Email),
        (this.image_update = item.Image);
    },
    createEmployee() {
      var data = {
        EmployeeId: this.employeeid,
        FirstName: this.firstname,
        LastName: this.lastname,
        DateOfBirth: this.dateofbirth,
        Gender: this.gender,
        Department: this.departmentid,
        Phone: this.phone,
        Email: this.email,
        Image: this.imgDataUrl
      };
      // var facedata = {
      //   Employee: this.employeeid,
      //   Encoding: this.facedescription
      // };
      // getAPI.post("/save-encode/", facedata)
      getAPI
        .post("/create-employee/", data)
        .then(response => {
          this.getEmployee();
          console.log(response.data);
          swal.fire({
            toast: true,
            position: "top-end",
            icon: "success",
            title: "Success",
            text: "Create Employee",
            showConfirmButton: false,
            timer: 1500
          });
          this.encodeFace();
          this.resetInputForm();
          this.profile_isvalid = false;
        })
        .catch(e => {
          console.log(e);
          swal.fire({
            toast: true,
            position: "top-end",
            icon: "error",
            title: "Error",
            text: "Employee ID invalid or already exists",
            timer: 2000,
            showConfirmButton: false
          });
        });
    },
    updateEmployee() {
      var data = {
        EmployeeId: this.employeeid_update,
        FirstName: this.firstname_update,
        LastName: this.lastname_update,
        DateOfBirth: this.dateofbirth_update,
        Gender: this.gender_update,
        Department: this.departmentid_update,
        Phone: this.phone_update,
        Email: this.email_update
      };
      getAPI
        .post(`update-employee/${data.EmployeeId}`, data)
        .then(response => {
          console.log(response.data);
          this.getEmployee();
          swal.fire({
            toast: true,
            position: "top-end",
            icon: "success",
            title: "Success",
            text: "Update employee",
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
    deleteEmployee(item) {
      console.log(item.EmployeeId);
      swal
        .fire({
          toast: true,
          position: "top",
          icon: "warning",
          title: "Delete",
          text: `"${item.FirstName} ${item.LastName}"`,
          showCancelButton: true,
          showConfirmButton: true
        })
        .then(result => {
          if (result.value) {
            var deleteIndex = this.items.findIndex(
              index => index.EmployeeId == item.EmployeeId
            );
            this.items.splice(deleteIndex, 1);
            getAPI
              .delete(`delete-employee/${item.EmployeeId}`)
              .then(response => {
                // this.getEmployee();
                swal.fire({
                  toast: true,
                  position: "top-end",
                  icon: "success",
                  title: "Success",
                  text: "Delete employee",
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
    getDepartment() {
      getAPI
        .get("department/", {
          headers: { Authorization: `Bearer ${this.$store.state.accessToken}` }
        })
        .then(response => {
          this.Departments = response.data;
          console.log(Departments);
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
            showConfirmButton: false
          });
        });
    },
    resetInputForm() {
      (this.imgDataUrl = ""),
        (this.employeeid = ""),
        (this.firstname = ""),
        (this.lastname = ""),
        (this.dateofbirth = ""),
        (this.gender = ""),
        (this.departmentid = ""),
        (this.phone = ""),
        (this.email = ""),
        (this.image = "");
    },
    toggle_image() {
      this.toggled_image = !this.toggled_image;
    },
    cropSuccess(imgDataUrl, field) {
      console.log("-------- crop success --------");
      this.imgDataUrl = imgDataUrl;
      this.checkImage();
    },
    cropUploadSuccess(jsonData, field) {
      console.log("-------- upload success --------");
      console.log(jsonData);
      console.log("field: " + field);
    },
    cropUploadFail(status, field) {
      console.log("-------- upload fail --------");
      console.log(status);
      console.log("field: " + field);
    },
    async checkImage() {
      this.loading_api = true;
      var detection_score = 0;
      const input = document.getElementById("profile_image");
      console.log(input);
      await faceapi.nets.ssdMobilenetv1.loadFromUri(
        "models/ssd_mobilenetv1_model-weights_manifest.json"
      );
      const detection = await faceapi.detectSingleFace(input);
      // const detection = await faceapi.detectSingleFace(
      //   input,
      //   new faceapi.SsdMobilenetv1Options()
      // );
      // .withFaceLandmarks()
      // .withFaceDescriptor();

      if (detection != null && detection._score > 0.98) {
        detection_score = Math.floor(detection._score * 100);
        this.loading_api = false;
        this.profile_isvalid = true;
        // this.facedescription = detection.descriptor.toString();
        // const arr = str.split(",");
        // const farr = new Float32Array(arr);
        // console.log(farr);
        swal.fire({
          toast: true,
          position: "top-end",
          icon: "success",
          title: `Detect a face with score: ${detection_score}%`,
          timer: 2000,
          showConfirmButton: false
        });
      } else {
        this.profile_isvalid = false;
        this.loading_api = false;
        swal.fire({
          toast: true,
          position: "top",
          icon: "error",
          title: "No face detection",
          timer: 1500,
          showConfirmButton: false
        });
      }
    },
    async encodeFace() {
      var data = {
        EmployeeId: this.employeeid,
        Image: this.imgDataUrl
      };
      console.log(data);
      getAPI.post(`encode-face/`, data).then(response => {
        console.log(response.data);
      });
    }
  },
  created() {
    this.getEmployee();
    this.getDepartment();
    setTimeout(() => {
      this.loading = false;
    }, 3000);
    // Promise.all([
    //   faceapi.nets.ssdMobilenetv1.loadFromUri("/models"),
    //   faceapi.nets.faceLandmark68Net.loadFromUri("/models"),
    //   faceapi.nets.faceRecognitionNet.loadFromUri("/models")
    // ]);
  }
};
</script>
