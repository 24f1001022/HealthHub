<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4">
          <div v-if="department">
            <!-- Header -->
            <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-2">
              <h4 class="fw-bold text-primary">{{ department.name }}</h4>
              <div>
                <button class="btn btn-outline-danger btn-sm" @click="back">Back</button>
              </div>
            </div>

            <!-- Overview -->
            <h5 class="fw-semibold text-dark">Overview</h5>
            <p class="text-muted">{{ department.overview }}</p>

            <!-- Doctors List -->
            <h5 class="fw-semibold text-dark mt-4">Doctors' List</h5>
            <div
              v-for="doc in department.doctors"
              :key="doc.id"
              class="border rounded-3 p-3 d-flex justify-content-between align-items-center bg-white shadow-sm mb-3"
            >
              <span class="fw-semibold">{{ doc.name }}</span>
              <div>
                <button class="btn btn-outline-primary btn-sm me-2" @click="checkAvailability(doc.id)">
                  Check Availability
                </button>
                <button class="btn btn-outline-secondary btn-sm" @click="viewDetails(doc.id)">
                  View Details
                </button>
              </div>
            </div>
          </div>

          <!-- Loading Spinner -->
          <div v-else class="text-center mt-5">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-3 text-muted">Loading department info...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "PatientDepartment",
  data() {
    return {
      department: null,
      bgcolor: 'lightblue'
    };
  },
  async created() {
    const dept_id = this.$route.params.dept_id;
    console.log(dept_id)
    try {
      const res = await axiosInstance.get(`/patient/department/${dept_id}`);
      this.department = res.data;
    } catch (err) {
      console.error(err);
      alert("Error loading department info.");
    }
  },
  methods: {
    checkAvailability(id) {
      const doc_id = id
      this.$router.push({ path:`/patient/appointment/${doc_id}` });
    },
    viewDetails(id) {
      const doc_id = id
      this.$router.push({ path:`/patient/doctor_detais/${doc_id} `})
    },
    back() {
      this.$router.push("/patient");
    },
  },
};
</script>
<style scoped>
.container {
  max-width: 700px;
}

.card {
  background-color: #fff;
}

button {
  border-radius: 20px;
}

.btn-link:hover {
  text-decoration: underline;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
