<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4">

          <!-- Header -->
          <div class="d-flex justify-content-between align-items-center border-bottom pb-3 mb-4">
            <h4 class="fw-bold text-primary">All Registered Patients</h4>
            <div class="d-flex">
              <input
                type="text"
                v-model="searchTerm"
                placeholder="Search patients..."
                class="form-control form-control-sm me-2"
                style="width: 250px"
              />
            </div>
          </div>

          <!-- Patient List -->
          <div v-if="filteredPatients.length">
            <div
              v-for="pat in filteredPatients"
              :key="pat.id"
              class="d-flex justify-content-between align-items-center border p-2 rounded mb-2 bg-white shadow-sm"
            >
              <span>{{ pat.name }}</span>
              <div>
                <button class="btn btn-outline-warning btn-sm me-2" @click="gotoeditPatient(pat.id)">Edit</button>
                <button class="btn btn-outline-danger btn-sm me-2" @click="gotodeletePatient(pat.id)">Delete</button>
              </div>
            </div>
          </div>
          <div v-else class="text-center text-muted">No patients found.</div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "AllPatients",
  data() {
    return {
      patients: [],
      searchTerm: "",
      bgcolor: "lightblue",
    };
  },
  computed: {
    filteredPatients() {
      if (!this.searchTerm) return this.patients;
      const term = this.searchTerm.toLowerCase();
      return this.patients.filter((pat) =>
        pat.name.toLowerCase().includes(term)
      );
    },
  },
  async created() {
    await this.loadPatients();
  },
  methods: {
    async loadPatients() {
      try {
        const res = await axiosInstance.get("/get_patients"); 
        this.patients = res.data;
      } catch (err) {
        console.error(err);
        alert("Error loading patients.");
      }
    },
    gotoeditPatient(id) {
      this.$router.push({ path: `/admin/patient/${id}/edit`})
    },
    gotodeletePatient(id) {
      this.$router.push({path:`/admin/delete-patient/${id}`})
      }
  },
};
</script>

<style scoped>
body {
  font-family: "Segoe UI", sans-serif;
}
.btn-outline-danger:hover {
  background-color: #dc3545 !important;
  color: #fff !important;
}
</style>
