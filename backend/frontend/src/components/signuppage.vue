<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="d-flex justify-content-center align-items-center p-4">
      <div
        class="card shadow-lg border-0 rounded-4"
        style="max-width: 900px; width: 100%"
      >
        <!-- Logo + Welcome Text -->
        <div class="text-center mt-4">
          <div
            class="bg-primary bg-opacity-10 d-inline-flex align-items-center justify-content-center rounded-circle p-3"
          >
            <i class="bi bi-heart-pulse-fill text-primary fs-2"></i>
          </div>
          <h3 class="mt-3 fw-bold text-dark">Create Your Account</h3>
          <p class="text-muted">Please Signup to continue</p>
        </div>
        <form @submit.prevent="handleSignup">
          <div class="row g-0">
            <!-- Left Side -->
            <div
              class="col-md-6 bg-white d-flex flex-column justify-content-center p-5"
            >
              <!-- Form -->
              <div class="mb-3">
                <label for="email" class="form-label fw-semibold">Email</label>
                <input
                  type="email"
                  id="email"
                  v-model="email"
                  class="form-control form-control-lg"
                  placeholder="Enter your email"
                  required
                />
              </div>
              <div class="mb-4">
                <label for="Full_name" class="form-label fw-semibold"
                  >Full Name</label
                >
                <input
                  type="text"
                  id="Full_name"
                  v-model="Full_name"
                  class="form-control form-control-lg"
                  placeholder="Enter your Full Name"
                  required
                />
              </div>
              <div class="mb-4">
                <label for="PhoneNo" class="form-label fw-semibold"
                  >Phone No</label
                >
                <input
                  type="text"
                  id="PhoneNo"
                  v-model="PhoneNo"
                  class="form-control form-control-lg"
                  placeholder="Enter your Phone No"
                  required
                />
              </div>
              <div class="mb-4">
                <label for="Gender" class="form-label fw-semibold d-block"
                  >Gender</label
                >
                <select
                  id="Gender"
                  name="Gender"
                  v-model="Gender"
                  class="form-select form-select-lg"
                  required
                >
                  <option value="">Select</option>
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                </select>
              </div>
            </div>
            <!-- Right Side:Form -->
            <div
              class="col-md-6 bg-white d-flex flex-column justify-content-center p-5"
            >
              <div class="mb-3">
                <label for="Address" class="form-label fw-semibold"
                  >Address</label
                >
                <input
                  type="text"
                  id="Address"
                  v-model="Address"
                  class="form-control form-control-lg"
                  placeholder="Enter your Address"
                  required
                />
              </div>
              <div class="mb-4">
                <label for="Age" class="form-label fw-semibold">Age</label>
                <input
                  type="number"
                  id="Age"
                  min="0"
                  v-model="Age"
                  class="form-control form-control-lg"
                  placeholder="Enter your Age"
                  required
                />
              </div>
              <div class="mb-4">
                <label for="password" class="form-label fw-semibold"
                  >Password</label
                >
                <input
                  type="password"
                  id="password"
                  v-model="password"
                  class="form-control form-control-lg"
                  placeholder="Enter your password"
                  required
                />
              </div>
              <div class="mb-4">
                <label for="confirm_password" class="form-label fw-semibold"
                  >Confirm Password</label
                >
                <input
                  type="password"
                  id="confirm_password"
                  v-model="confirm_password"
                  class="form-control form-control-lg"
                  placeholder="Enter your Confirm password"
                  required
                />
              </div>
            </div>
            <div class="d-flex align-items-center justify-content-center">
              <button
                type="submit"
                class="btn btn-primary btn-lg mb-4 d-flex align-items-center justify-content-center shadow-lg w-50"
              >
                Signup
              </button>
            </div>
            <div class="d-flex justify-content-center">
              <p class="mt-0">
                Already have an account?
                <router-link to="/login">Login here</router-link>
              </p>
            </div>
          </div>
          </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignupPage",
  data() {
    return {
      email: "",
      password: "",
      bgcolor: "lightblue",
      Full_name: "",
      Age: null,
      Gender:"",
      Address:"",
      confirm_password:"", 
      PhoneNo:""
    };
  },
  methods: {
  async handleSignup() {
    const res = await this.$store.dispatch('auth/signup', {
      email: this.email,
      password: this.password,
      confirm_password: this.confirm_password,
      Address: this.Address,
      Full_name: this.Full_name,
      Age: this.Age,
      PhoneNo: this.PhoneNo,
      Gender: this.Gender
    });

    if (res.success) {
      this.$router.push('/login');
    } else {
      alert(res.message || 'Signup failed');
    }
  }
}
};
</script>

<style>
body {
  font-family: "Segoe UI", sans-serif;
}
</style>
