<template>
<div :style="{backgroundColor : bgcolor}">
  <div class=" min-vh-100 py-5">
    <div class="container">
      <div class="card shadow-lg border-0 rounded-4 p-4">
        <!-- Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h4 class="fw-bold text-primary">Welcome {{ userName }}</h4>
          <div>
            <router-link :to="`/patient/edit/profile/${this.userId}`" class="text-decoration-none text-secondary me-3">Edit Profile</router-link>
            <router-link :to="`/patient/${this.userId}/treatment`" class="text-decoration-none text-secondary me-3">History</router-link>
            <button @click="logout" class="btn btn-outline-danger btn-sm">Logout</button>
          </div>
        </div>

        <!-- Departments -->
        <h5 class="fw-semibold text-dark mb-3">Departments</h5>
        <div class="row g-3 mb-4">
          <div v-for="dept in departments" :key="dept.id" class="col-md-4">
  <div class="border rounded-3 p-3 d-flex justify-content-between align-items-center bg-white shadow-sm">
    <span class="fw-semibold text-capitalize">{{ dept.name }}</span>
    <button
      class="btn btn-outline-primary btn-sm"
      @click="goToDepartment(dept.id)"
    >
      View Details
    </button>
  </div>
</div>

        </div>

        <!-- Appointments -->
        <h5 class="fw-semibold text-dark mb-3">Upcoming Appointments</h5>
        <div class="table-responsive">
          <table class="table align-middle text-center">
            <thead class="table-primary text-dark">
              <tr>
                <th>Sr No.</th>
                <th>Doctor Name</th>
                <th>Dept</th>
                <th>Date</th>
                <th>Time</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(appt, index) in appointments" :key="appt.id">
                <td>{{ index + 1 }}</td>
                <td>{{ appt.doctor }}</td>
                <td>{{ appt.department }}</td>
                <td>{{ appt.date }}</td>
                <td>{{ appt.time }}</td>
                <td>
                  <button @click="cancelAppointment(appt.id)" class="btn btn-outline-danger btn-sm">Cancel</button>
                </td>
              </tr>
              <tr v-if="appointments.length === 0">
                <td colspan="6" class="text-muted">No appointments found</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axiosInstance from "../plugins/axios";
export default {
  name: "PatientDashboard",
  data() {
    return {
      userName: "",
      departments: [],
      appointments: [],
      bgcolor: "lightblue",
      userId: "",

    };
  },
  async mounted() {
    await this.loadDashboard();
  },
  methods: {
    async loadDashboard() {
      try {
        const res = await axiosInstance.get("/patient/dashboard", { withCredentials: true });
        this.userName = res.data.user_name;
        this.departments = res.data.departments;
        this.appointments = res.data.appointments;
        this.userId = res.data.user_id
      } catch (err) {
        console.error(err);
        alert("Failed to load dashboard");
      }
    },
     goToDepartment(deptid) {
      // Convert deptName to lowercase and replace spaces if needed
      const dept_id = deptid

      // Navigate to the route with the department name
      this.$router.push({ path: `/patient/department/${dept_id}` });
    },
    async cancelAppointment(id) {
      if (!confirm("Cancel this appointment?")) return;
      try {
        const res = await axiosInstance.post(`/patient/cancel/${id}`);
        if (res.data.success) {
          this.appointments = this.appointments.filter((a) => a.id !== id);
        }
      } catch (err) {
        alert("Error cancelling appointment");
      }
    },
    async logout() {
      await this.$store.dispatch("auth/logout");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Segoe UI", sans-serif;
}
.table th {
  background-color: #dbeafe !important; /* soft blue */
}
.btn-outline-danger:hover {
  background-color: #dc3545 !important;
  color: #fff !important;
}
</style>
