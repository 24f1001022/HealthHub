<template>
  <div :style="{ backgroundColor: bgcolor }" class="min-vh-100 d-flex align-items-center justify-content-center">
    <div class="card shadow-lg border-0 rounded-5 overflow-hidden" style="max-width: 700px; width: 100%">
      
      <!-- Icon and Header -->
      <div class="text-center mt-4">
        <div class="bg-danger bg-opacity-10 d-inline-flex align-items-center justify-content-center rounded-circle p-3">
          <i class="bi bi-person-dash-fill text-danger fs-2"></i>
        </div>
        <h3 class="mt-3 fw-bold text-dark">Delete Doctor</h3>
        <p class="text-muted">Permanently remove this doctor from the system</p>
      </div>

      <div v-if="doctor" class="px-5 py-4">
        <div class="alert alert-warning">
          ⚠️ You are about to permanently delete the following doctor:
          <ul class="mt-3 mb-0">
            <li><strong>Name:</strong> {{ doctor.name }}</li>
            <li><strong>Email:</strong> {{ doctor.email }}</li>
            <li><strong>Specialization:</strong> {{ doctor.specialization }}</li>
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
        <p class="mt-3 text-muted">Loading doctor details...</p>
      </div>

    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "DeleteDoctor",
  data() {
    return {
      bgcolor: "lightblue",
      doctor: null,
      loading: false,
    };
  },
  async created() {
    const doctorId = this.$route.params.id;
    if (doctorId) {
      await this.fetchDoctor(doctorId);
    } else {
      alert("No doctor ID provided.");
      this.$router.push("/admin");
    }
  },
  methods: {
    async fetchDoctor(id) {
      try {
        const res = await axiosInstance.get(`/admin/get_doctor/${id}`);
        if (res.data && res.data.doctor) {
          this.doctor = res.data.doctor;
        } else {
          alert("Doctor not found.");
          this.$router.push("/admin");
        }
      } catch (err) {
        console.error(err);
        alert("Failed to fetch doctor details.");
        this.$router.push("/admin");
      }
    },
    async handleDelete() {
  if (!confirm(`Are you sure you want to permanently delete Dr. ${this.doctor.name}?`)) return;

  this.loading = true;
  try {
    const res = await axiosInstance.delete(`/admin/delete_doctor/${this.doctor.id}`);

    if (res.data.success) {
      alert("Doctor deleted successfully.");
      this.$router.push("/admin");
    } else {
      // ⚠️ Show backend message:
      alert(res.data.message || "Failed to delete doctor.");
    }

  } catch (err) {
    console.error(err);

    // If backend returns 400, show its message:
    if (err.response && err.response.data && err.response.data.message) {
      alert(err.response.data.message);
    } else {
      alert("Error deleting doctor.");
    }

  } finally {
    this.loading = false;
  }
}
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
