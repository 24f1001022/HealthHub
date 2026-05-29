<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4">

          <!-- Header -->
          <div class="d-flex justify-content-between align-items-center border-bottom pb-3 mb-4">
            <h4 class="fw-bold text-primary">Welcome Admin</h4>
            <div class="d-flex">
              <button class="btn btn-outline-success btn-sm me-2" @click="gotoadddepartment">Add Department</button>
              <button class="btn btn-outline-success btn-sm me-2" @click="gotoadddoctor">Add Doctor</button>
              <button type="button" @click="logout" class="btn btn-outline-danger btn-sm">Logout</button>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-3 text-muted">Loading dashboard data...</p>
          </div>

          <!-- Dashboard Content -->
          <div v-else>
            <!-- Registered Doctors -->
<section class="mb-4">
  <h5 class="fw-semibold text-dark border-bottom pb-2">Registered Doctors</h5>
  <div v-if="dashboard.doctors && dashboard.doctors.length > 0">
    <div
      v-for="doc in dashboard.doctors.slice(0, 3)"
      :key="doc.id"
      class="d-flex justify-content-between align-items-center border p-2 rounded mb-2 bg-white shadow-sm"
    >
      <span>{{ doc.name }}</span>
      <div>
        <button class="btn btn-outline-warning btn-sm me-2" @click="gotoeditItemdoc(doc.id)">Edit</button>
        <button class="btn btn-outline-danger btn-sm me-2" @click="gotodeletedoctorpage(doc.id)">Delete</button>
      </div>
    </div>
    <div class="text-end">
      <button class="btn btn-outline-primary btn-sm" @click="goToAllDoctors">View More</button>
    </div>
  </div>
  <div v-else class="text-muted py-2">No doctors registered yet.</div>
</section>

<!-- Registered Patients -->
<section class="mb-4">
  <h5 class="fw-semibold text-dark border-bottom pb-2">Registered Patients</h5>
  <div v-if="dashboard.patients && dashboard.patients.length > 0">
    <div
      v-for="pat in dashboard.patients.slice(0, 3)"
      :key="pat.id"
      class="d-flex justify-content-between align-items-center border p-2 rounded mb-2 bg-white shadow-sm"
    >
      <span>{{ pat.name}}</span>
      <div>
        <button class="btn btn-outline-warning btn-sm me-2" @click="gotoeditItem(pat.id)">Edit</button>
        <button class="btn btn-outline-danger btn-sm me-2" @click="gotodeletepatient(pat.id)">Delete</button>
      </div>
    </div>
    <div class="text-end">
      <button class="btn btn-outline-primary btn-sm" @click="goToAllPatients">View More</button>
    </div>
  </div>
  <div v-else class="text-muted py-2">No patients registered yet.</div>
</section>
            <section>
              <h5 class="fw-semibold text-dark border-bottom pb-2">Upcoming Appointments</h5>
              <div class="table-responsive">
                <table class="table align-middle text-center">
                  <thead class="table-primary text-dark">
                    <tr>
                      <th>Sr No.</th>
                      <th>Patient Name</th>
                      <th>Doctor Name</th>
                      <th>Department</th>
                      <th>Patient History</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-if="dashboard.appointments.length > 0"
                      v-for="(appt, index) in dashboard.appointments"
                      :key="appt.id"
                    >
                      <td>{{ index + 1 }}</td>
                      <td>{{ appt.patient }}</td>
                      <td>{{ appt.doctor }}</td>
                      <td>{{ appt.department }}</td>
                      <td>
                        <button class="btn btn-outline-primary btn-sm" @click="viewHistory(appt)">View</button>
                      </td>
                    </tr>
                    <tr v-else>
                      <td colspan="5" class="text-muted py-3">No appointments available.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </section>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "AdminDashboard",
  data() {
    return {
      bgcolor: "lightblue",
      loading: true,
      dashboard: {
        doctors: [],
        patients: [],
        appointments: [],
      },
    };
  },
  async mounted() {
    await this.loadDashboard();
  },
  methods: {
    async loadDashboard() {
      try {
        const res = await axiosInstance.get("/admin/dashboard");
        this.dashboard = res.data;
      } catch (err) {
        console.error(err);
        alert("Error loading admin dashboard.");
      } finally {
        this.loading = false;
      }
    },
    gotoadddoctor() {
      this.$router.push({ path: "/admin/add-doctor" });
    },
    gotodeletepatient(id){
      this.$router.push({path:`/admin/delete-patient/${id}`})
    },
    gotoadddepartment() {
      this.$router.push({ path: "/admin/add-department" });
    },
    gotodeletedoctorpage(id) {
      this.$router.push({ path: `/admin/delete-doctor/${id}` });
    },
    goToAllDoctors() {
      this.$router.push({ path: "/admin/all-doctors" });
    },
    goToAllPatients() {
      this.$router.push({ path: "/admin/all-patients" });
    },
    gotoeditItem(id) {
      this.$router.push({ path: `/admin/patient/${id}/edit` });
    },
    gotoeditItemdoc(id) {
      this.$router.push({ path: `/admin/doctor/${id}/edit` });
    },
    async logout() {
      await this.$store.dispatch("auth/logout");
      this.$router.push({path: "/login"});
    },
    viewHistory(appt) {
      alert(`Patient history: ${appt.history}`);
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Segoe UI", sans-serif;
}
.table th {
  background-color: #dbeafe !important;
}
.btn-outline-danger:hover {
  background-color: #dc3545 !important;
  color: #fff !important;
}
</style>
