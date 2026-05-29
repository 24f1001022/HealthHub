<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4">

          <!-- Header -->
          <div class="d-flex justify-content-between align-items-center border-bottom pb-3 mb-4">
            <h4 class="fw-bold text-primary">All Registered Doctors</h4>
            <div class="d-flex">
              <input
                type="text"
                v-model="searchTerm"
                placeholder="Search doctors..."
                class="form-control form-control-sm me-2"
                style="width: 250px"
              />
            </div>
          </div>

          <!-- Doctor List -->
          <div v-if="filteredDoctors.length">
            <div
              v-for="doc in filteredDoctors"
              :key="doc.id"
              class="d-flex justify-content-between align-items-center border p-2 rounded mb-2 bg-white shadow-sm"
            >
              <span>{{ doc.name }}</span>
              <div>
                <button class="btn btn-outline-warning btn-sm me-2" @click="gotoeditDoctor(doc.id)">Edit</button>
                <button class="btn btn-outline-danger btn-sm me-2" @click="gotodeleteDoctor(doc.id)">Delete</button>
              </div>
            </div>
          </div>
          <div v-else class="text-center text-muted">No doctors found.</div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "AllDoctors",
  data() {
    return {
      doctors: [],
      searchTerm: "",
      bgcolor: "lightblue",
    };
  },
  computed: {
    filteredDoctors() {
      if (!this.searchTerm) return this.doctors;
      const term = this.searchTerm.toLowerCase();
      return this.doctors.filter((doc) =>
        doc.name.toLowerCase().includes(term)
      );
    },
  },
  async created() {
    await this.loadDoctors();
  },
  methods: {
    async loadDoctors() {
      try {
        const res = await axiosInstance.get("/admin/get_doctors");
        this.doctors = res.data;
      } catch (err) {
        console.error(err);
        alert("Error loading doctors.");
      }
    },
    gotoeditDoctor(id) {
      this.$router.push({ path: `/admin/doctor/${id}/edit`})
    },
    gotodeleteDoctor(id) {
      this.$router.push({path: `/admin/delete-doctor/${id}`})
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
