<template>
  <div class="login-container text-center">
    <div class="row login-row justify-content-md-center">
      <CCol class="login-form">
        <CCard>
          <CCardHeader>Login to Hutech Management</CCardHeader>
          <CCardBody>
            <CForm>
              <v-form v-on:submit.prevent="login" v-model="valid" lazy-validation>
                <v-container>
                  <CInput placeholder="Username" v-model="username" required>
                    <template #prepend-content>
                      <CIcon name="cil-user" />
                    </template>
                  </CInput>
                  <CInput
                    placeholder="Password"
                    type="password"
                    autocomplete="current-password"
                    v-model="password"
                    required
                  >
                    <template #prepend-content>
                      <CIcon name="cil-shield-alt" />
                    </template>
                  </CInput>
                  <div class="form-group form-actions">
                    <CButton type="submit" size="sm" color="success">Submit</CButton>
                  </div>
                </v-container>
              </v-form>
            </CForm>
          </CCardBody>
        </CCard>
      </CCol>
    </div>
  </div>
</template>

<script>
import swal from "sweetalert2";
import router from "../../router";
export default {
  name: "login",
  data: () => ({
    username: "",
    password: "",
    valid: true,
    loading: false
  }),
  methods: {
    login() {
      // call login action
      this.$store
        .dispatch("login", {
          username: this.username,
          password: this.password
        })
        .then(() => {
          console.log(this.username);
          swal.fire({
            toast: true,
            position: "top-end",
            icon: "success",
            title: "  Login success",
            showConfirmButton: false,
            showCloseButton: false,
            timer: 1500
          });
          this.$router.go("/dashboard");
        })
        .catch(e => {
          this.loading = false;
          swal.fire({
            toast: true,
            position: "top-end",
            icon: "warning",
            title: "Error",
            text: e.message,
            showConfirmButton: false,
            showCloseButton: false,
            timer: 2000
          });
        });
    }
  }
};
</script>