<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h4 class="fw-bold text-primary">Edit Profile</h4>
            <button class="btn btn-outline-secondary btn-sm" @click="$router.back()">Back</button>
          </div>
          <form @submit.prevent="updateProfile">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Full Name</label>
                <input v-model="patient.name" type="text" class="form-control" required />
              </div>

              <div class="col-md-3">
                <label class="form-label">Age</label>
                <input v-model="patient.age" type="number" class="form-control" required />
              </div>

              <div class="col-md-3">
                <label class="form-label">Gender</label>
                <select v-model="patient.gender" class="form-select" required>
                  <option disabled value="">Select gender</option>
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                  <option value="O">Other</option>
                </select>
              </div>

              <div class="col-md-6">
                <label class="form-label">Email</label>
                <input v-model="patient.email" type="email" class="form-control" required />
              </div>

              <div class="col-md-6">
                <label class="form-label">Phone</label>
                <input v-model="patient.phone" type="text" class="form-control" />
              </div>

              <div class="col-12">
                <label class="form-label">Address</label>
                <textarea v-model="patient.address" rows="2" class="form-control"></textarea>
              </div>
            </div>

            <div class="text-end mt-4">
              <button class="btn btn-primary px-4" type="submit">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "PatientEditProfile",
  data() {
    return {
      bgcolor: "lightblue",
      patient: {
        id: "",
        name: "",
        age: "",
        gender: "",
        email: "",
        phone: "",
        address: "",
      },
    };
  },
  async created() {
    const id = this.$route.params.id;
    await this.fetchPatientProfile(id);
  },
  methods: {
    async fetchPatientProfile(id) {
      try {
        const res = await axiosInstance.get(`/patient/${id}/profile`);
        this.patient = res.data;
        console.log(res.data);
      } catch (err) {
        console.error("Error loading profile:", err);
      }
    },
    async updateProfile() {
      try {
        await axiosInstance.put(`/patient/${this.patient.id}/profile`, this.patient);
        alert("Profile updated successfully!");
        this.$router.push(`/patient/${this.patient.id}/profile`);
      } catch (err) {
        console.error("Error updating profile:", err);
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

.form-label {
  font-weight: 600;
  color: #0d6efd;
}

.form-control,
.form-select {
  border-radius: 10px;
  border: 1px solid #cfe2ff;
}

.btn {
  border-radius: 20px;
}

.btn-primary {
  background-color: #0d6efd;
  border: none;
}

.btn-primary:hover {
  background-color: #0b5ed7;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  color: white;
}
</style>
