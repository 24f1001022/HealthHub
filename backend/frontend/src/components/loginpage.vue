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
            class="col-md-6 d-flex flex-column justify-content-center align-items-center text-white p-5"
            style="background: linear-gradient(135deg, #0d6efd 0%, #6610f2 100%); min-height: 320px;"
          >
            <i class="bi bi-hospital fs-1 mb-3"></i>
            <h4 class="fw-bold text-center">HealthHub</h4>
            <p class="text-center opacity-75 mb-0">Hospital management made simple</p>
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
export default {
  name: "LoginPage",
  data() {
    return {
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

<style>
body {
  font-family: "Segoe UI", sans-serif;
}
</style>
