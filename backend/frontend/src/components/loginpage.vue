<template>
  <div :style="{ backgroundColor: bgcolor }">
     <div v-if="error" class="alert alert-danger text-center" role="alert">
            {{ message }}
            </div>
    <div class="d-flex justify-content-center align-items-center vh-100">
      <div
        class="card shadow-lg border-0 rounded-4 overflow-hidden"
        style="max-width: 900px; width: 100%"
      >
        <div class="row g-0">
          <!-- Left Side: Doctor Illustration -->
          <div
            class="col-md-6 d-flex align-items-end justify-content-center login-hero"
          >
            <img
              :src="loginDoctorImg"
              alt="HealthHub doctor"
              class="login-doctor-img"
            />
          </div>

          <!-- Right Side: Login Form -->
          <div class="col-md-6 bg-white d-flex flex-column justify-content-center p-5">
            <div class="text-center mb-4">
              <div
                class="bg-primary bg-opacity-10 d-inline-flex align-items-center justify-content-center rounded-circle p-3"
              >
                <i class="bi bi-heart-pulse-fill text-primary fs-2"></i>
              </div>
              <h3 class="mt-3 fw-bold text-dark">Welcome Back</h3>
              <p class="text-muted">Please login to continue</p>
            </div>

            <form @submit.prevent="handleLogin">
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
                <label for="password" class="form-label fw-semibold">Password</label>
                <input
                  type="password"
                  id="password"
                  v-model="password"
                  class="form-control form-control-lg"
                  placeholder="Enter your password"
                  required
                />
              </div>

              <button type="submit" class="btn btn-primary btn-lg w-100">LOGIN</button>
            </form>

            <div class="d-flex justify-content-center">
              <p class="mt-3">
                Don't have an account?
                <router-link to="/signup">Sign up here</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import loginDoctorImg from "../assets/login-doctor.png";

export default {
  name: "LoginPage",
  data() {
    return {
      loginDoctorImg,
      email: "",
      password: "",
      message: "",
      error: false,
      bgcolor: "lightblue",
    };
  },
 methods: {
    async handleLogin() {
    try {
    const res = await this.$store.dispatch('auth/login', {
    email: this.email,
    password: this.password,
  });

  if (res.success) {
    this.error = false;
    this.message = "";
    if (res.user.role === 'patient') this.$router.push('/patient');
    else if (res.user.role === 'doctor') this.$router.push('/doctor');
    else if (res.user.role === 'admin') this.$router.push('/admin');
  } else {
    this.error = true;
    this.message = res.message || "Login failed. Please try again.";
  }
    } catch (e) {
      this.error = true;
      this.message = "Cannot reach server. Wait 30s (Render cold start) and try again.";
    }
  }
  }
};
</script>

<style scoped>
.login-hero {
  background: linear-gradient(160deg, #e8f4ff 0%, #cfe8ff 45%, #b8daff 100%);
  min-height: 420px;
  padding: 1.5rem 1rem 0;
}

.login-doctor-img {
  max-width: 100%;
  max-height: 380px;
  object-fit: contain;
  filter: drop-shadow(0 12px 24px rgba(13, 110, 253, 0.15));
}

body {
  font-family: "Segoe UI", sans-serif;
}
</style>
