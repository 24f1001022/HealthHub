<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4">
          <!-- Header -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="fw-bold text-primary">Patient History</h4>
            <div>
              <router-link
                to="/patient/dashboard"
                class="text-decoration-none text-secondary me-3"
              >
                Dashboard
              </router-link>
              <button class="btn btn-outline-secondary btn-sm" @click="$router.back()">Back</button>
            </div>
          </div>

          <!-- Patient Info -->
          <div class="bg-light rounded-3 p-3 mb-4 shadow-sm">
            <p class="mb-1"><strong>Patient Name:</strong> {{ history.patient_name }}</p>
            <p class="mb-1"><strong>Doctor's Name:</strong> {{ history.doctor_name }}</p>
            <p class="mb-0"><strong>Department:</strong> {{ history.department }}</p>
          </div>

          <!-- Table -->
          <div v-if="filteredRecords.length > 0" class="table-responsive">
            <table class="table align-middle text-center">
              <thead class="table-primary text-dark">
                <tr>
                  <th>Visit Type</th>
                  <th>Tests Done</th>
                  <th>Diagnosis</th>
                  <th>Prescription</th>
                  <th>Medicines</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(rec, index) in filteredRecords" :key="index">
                  <td>{{ rec.visit_type }}</td>
                  <td>{{ rec.tests_done }}</td>
                  <td>{{ rec.diagnosis }}</td>
                  <td>{{ rec.prescription }}</td>
                  <td>{{ rec.medicines }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="text-center text-muted py-4">
            No patient history found.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "PatientHistory",
  data() {
    return {
      history: {
        patient_name: "",
        doctor_name: "",
        department: "",
        records: [],
      },
      bgcolor: "lightblue", // same theme background
    };
  },
  async created() {
    const id = this.$route.params.id;
    await this.fetchHistory(id);
  },
  computed: {
    // Only show records that have a valid visit_type
    filteredRecords() {
      if (!this.history.records) return [];
      return this.history.records.filter(
        (r) => r.visit_type && r.visit_type.trim() !== ""
      );
    },
  },
  methods: {
    async fetchHistory(id) {
      try {
        const res = await axiosInstance.get(`/patient/${id}/history`);
        this.history = res.data;
      } catch (err) {
        console.error(err);
      }
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Segoe UI", sans-serif;
}

.card {
  background: #fff;
}

.bg-light {
  background-color: #f8fafc !important;
}

.table th {
  background-color: #dbeafe !important;
  font-weight: 600;
}

.table {
  border-radius: 10px;
  overflow: hidden;
}

.btn {
  border-radius: 20px;
}

.btn-outline-secondary:hover {
  background-color: #6c757d !important;
  color: #fff !important;
}

.text-primary {
  color: #0d6efd !important;
}
</style>
