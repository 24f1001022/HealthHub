<template>
  <div :style="{ backgroundColor: bgcolor }" class="min-vh-100 py-5">
    <div class="container">
      <div class="card shadow-lg border-0 rounded-4 p-4 bg-white">
        <h4 class="fw-bold mb-4 text-primary">Add a New Doctor</h4>

        <form @submit.prevent="handleSubmit">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label fw-semibold">Full Name</label>
              <input
                v-model="form.name"
                type="text"
                class="form-control"
                placeholder="Enter full name"
                required
              />
            </div>

            <div class="col-md-6">
              <label class="form-label fw-semibold">Specialization/Department</label>
              <select v-model="form.department" class="form-select" required>
                <option value="">Select Department</option>
                <option
                  v-for="dept in departments"
                  :key="dept.id"
                  :value="dept.dpt_name"
                >
                  {{ dept.dpt_name }}
                </option>
              </select>
            </div>

            <div class="col-md-6">
              <label class="form-label fw-semibold">Experience (years)</label>
              <input
                v-model="form.experience"
                type="number"
                class="form-control"
                placeholder="e.g. 5"
              />
            </div>

            <div class="col-md-6">
              <label class="form-label fw-semibold">Email</label>
              <input
                v-model="form.email"
                type="email"
                class="form-control"
                placeholder="Enter email"
                required
              />
            </div>

            <div class="col-md-6">
              <label class="form-label fw-semibold">Phone No</label>
              <input
                v-model="form.phone_no"
                type="text"
                class="form-control"
                placeholder="Enter phone number"
                maxlength="10"
                required
              />
            </div>

            <div class="col-md-6">
              <label class="form-label fw-semibold">Gender</label>
              <select v-model="form.gender" class="form-select" required>
                <option value="">Select</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div class="col-md-6">
              <label class="form-label fw-semibold">Password</label>
              <input
                v-model="form.password"
                type="password"
                class="form-control"
                placeholder="Enter password"
                required
              />
            </div>

            <div class="col-12 text-end mt-4">
              <button class="btn btn-outline-primary btn-lg px-5 rounded-pill" type="submit">
                Create
              </button>
            </div>
          </div>
        </form>
        <div v-if="message" :class="['alert', alertClass]" class="mt-4" role="alert">
  {{ message }}
</div>

      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "AddDoctor",
  data() {
  return {
    bgcolor: "lightblue",
    form: {
      name: "",
      specialization: "",
      experience: "",
      email: "",
      gender: "",
      phone_no: "",
      password: "",
      department: "",
    },
    departments: [],
    message: "",      
    alertClass: "",    
  };
},
  async created() {
    await this.loadDepartments();
  },
  methods: {
    async loadDepartments() {
      try {
        const res = await axiosInstance.get("/departments");
        this.departments = res.data;
      } catch (err) {
        console.error("Failed to load departments", err);
      }
    },
   async handleSubmit() {
  this.message = "";
  this.alertClass = "";

  try {
    const res = await axiosInstance.post("/admin/add_doctor", this.form);
    if (res.data.success) {
      this.message = res.data.message || "Doctor added successfully!";
      this.alertClass = "alert-success";

      // Optional delay before redirect
      setTimeout(() => {
        this.$router.push("/admin/dashboard");
      }, 2000);
    } else {
      this.message = res.data.message || "Failed to add doctor.";
      this.alertClass = "alert-warning";
    }
  } catch (err) {
    this.message = err.response?.data?.message || "Error submitting form.";
    this.alertClass = "alert-danger";
    setTimeout(() => {
    this.message = "";
    }, 3000);
  }
}
  },
};
</script>

<style scoped>
body {
  font-family: "Segoe UI", sans-serif;
}

.container {
  max-width: 720px;
}

.card {
  background-color: #ffffff;
}

button[type="submit"] {
  transition: all 0.2s ease;
}

button[type="submit"]:hover {
  background-color: #0d6efd;
  color: white;
}
</style>

