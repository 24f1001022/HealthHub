<template>
  <div :style="{ backgroundColor: bgcolor }" class="min-vh-100 py-5">
    <div class="d-flex justify-content-center align-items-center h-100">
      <div class="card shadow-lg border-0 rounded-4 px-5 py-4" style="max-width: 850px; width: 100%; background-color: white;">
        <!-- Header Icon and Title -->
        <div class="text-center mb-4">
          <div class="bg-primary bg-opacity-10 d-inline-flex align-items-center justify-content-center rounded-circle p-3">
            <i class="bi bi-person-vcard text-primary fs-2"></i>
          </div>
          <h3 class="mt-3 fw-bold text-dark">Doctor Profile</h3>
          <p class="text-muted">Detailed information about the doctor</p>
        </div>

        <!-- Doctor Info -->
        <div class="row align-items-center">
          <!-- Left Column: Info -->
          <div class="col-md-8">
            <h4 class="fw-bold text-primary mb-1">Dr. {{ doctor.name }}</h4>
            <p class="text-muted mb-2">
              ({{ doctor.department_name }} Specialist)
            </p>
            <p class="text-secondary lh-lg">
              Dr. {{ doctor.name }} is a specialist in the {{ doctor.department_name }} department at HealthHub. With over {{ doctor.experience }} years of experience, they are known for their compassionate care and accurate diagnoses. Patients trust Dr. {{ doctor.name }} for tailored treatment plans and a commitment to modern medical advancements.
            </p>
          </div>

          <!-- Right Column: Image -->
          <div class="col-md-4 text-center">
            <img
              v-if="doctor.gender === 'Male'"
              :src="'http://localhost:5000/static/images/doctor-character-illustration_863013-49092.jpg'"
              alt="Doctor"
              class="rounded-circle border"
              style="width: 120px; height: 120px; object-fit: cover;"
            />
            <img
              v-else-if="doctor.gender === 'Female'"
              src="http://localhost:5000/static/images/female_doc.jpg"
              alt="Female Doctor"
              class="rounded-circle border"
              style="width: 120px; height: 120px; object-fit: cover;"
            />
            <div v-else class="text-center">
              <i class="bi bi-person-circle text-secondary" style="font-size: 6rem;"></i>
            </div>
          </div>
        </div>

        <!-- Buttons -->
        <div class="d-flex justify-content-end mt-4 gap-2">
          <button class="btn btn-outline-primary btn-lg rounded-pill px-4" @click="checkAvailability">
            Check Availability
          </button>
          <button class="btn btn-outline-secondary btn-lg rounded-pill px-4" @click="goBack">
            Go Back
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "DoctorDetails",
  data() {
    return {
      bgcolor: "lightblue",
      doctor: {
        name: "",
        department_name: "",
        experience: "",
        gender: "",
        email: "",
        id: ""
      },
    };
  },
  async created() {
    const id = this.$route.params.docid;
    if (!id) {
      alert("Doctor ID not found!");
      this.$router.push("/patient");
      return;
    }
    this.id = id; 
    await this.fetchDoctorDetails(id);
  },
  methods: {
    async fetchDoctorDetails(id) {
      try {
        const res = await axiosInstance.get(`/doctor/${id}`);
        this.doctor = res.data;
      } catch (err) {
        console.error(err);
        alert("Failed to load doctor details.");
      }
    },
    checkAvailability() {
      this.$router.push(`/patient/appointment/${this.id}`);
    },
    goBack() {
      this.$router.push("/patients");
    },
  },
};
</script>

<style scoped>
.card {
  border: 1px solid #e2e8f0 !important;
}

.btn-outline-primary,
.btn-outline-secondary {
  border-radius: 20px;
  padding: 10px 20px;
}

.bg-lightblue {
  background-color: lightblue;
}

h4, h3 {
  font-family: "Segoe UI", sans-serif;
}
</style>
