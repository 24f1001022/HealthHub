<template>
  <div :style="{ backgroundColor: bgcolor }" class="min-vh-100 d-flex align-items-center justify-content-center">
    <div class="card shadow-lg border-0 rounded-5 overflow-hidden" style="max-width: 700px; width: 100%">
      
      <!-- Icon and Header -->
      <div class="text-center mt-4">
        <div class="bg-danger bg-opacity-10 d-inline-flex align-items-center justify-content-center rounded-circle p-3">
          <i class="bi bi-person-dash-fill text-danger fs-2"></i>
        </div>
        <h3 class="mt-3 fw-bold text-dark">Delete Patient</h3>
        <p class="text-muted">Permanently remove this patient from the system</p>
      </div>

      <div v-if="patient" class="px-5 py-4">
        <div class="alert alert-warning">
          ⚠️ You are about to permanently delete the following patient:
          <ul class="mt-3 mb-0">
            <li><strong>Name:</strong> {{ patient.name }}</li>
            <li><strong>Email:</strong> {{ patient.email }}</li>
            <li><strong>Phone:</strong> {{ patient.phone }}</li>
          </ul>
        </div>

        <div class="d-flex justify-content-center mt-4">
          <button
            class="btn btn-danger btn-lg shadow-lg w-50"
            @click="handleDelete"
            :disabled="loading"
          >
            {{ loading ? "Deleting..." : "Confirm Delete" }}
          </button>
        </div>
      </div>

      <div v-else class="text-center py-5">
        <div class="spinner-border text-danger" role="status"></div>
        <p class="mt-3 text-muted">Loading patient details...</p>
      </div>

    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "DeletePatient",
  data() {
    return {
      bgcolor: "lightblue",
      patient: null,
      loading: false,
    };
  },
  async created() {
    const patientId = this.$route.params.id;
    if (patientId) {
      await this.fetchPatient(patientId);
    } else {
      alert("No patient ID provided.");
      this.$router.push("/admin");
    }
  },
  methods: {
    async fetchPatient(id) {
      try {
        const res = await axiosInstance.get(`/patient/${id}/profile`);
        this.patient = res.data;
      } catch (err) {
        console.error(err);
        alert("Failed to fetch patient details.");
        this.$router.push("/admin");
      }
    },
    async handleDelete() {
      if (!confirm(`Are you sure you want to permanently delete ${this.patient.name}?`)) return;

      this.loading = true;
      try {
        const res = await axiosInstance.delete(`/admin/delete_patient/${this.patient.id}`);
        if (res.data.success) {
          alert("Patient deleted successfully.");
          this.$router.push("/admin");
        } else {
          alert(res.data.message || "Failed to delete patient.");
        }
      } catch (err) {
        console.error(err);
        alert("Error deleting patient.");
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Segoe UI", sans-serif;
}
button {
  border-radius: 20px;
}
</style>
