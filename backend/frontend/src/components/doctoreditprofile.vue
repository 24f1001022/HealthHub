<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4">
          <!-- Header -->
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h4 class="fw-bold text-primary">Edit Doctor Profile</h4>
            <button class="btn btn-outline-secondary btn-sm" @click="$router.back()">Back</button>
          </div>
          <form @submit.prevent="updateProfile">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Full Name</label>
                <input v-model="doctor.name" type="text" class="form-control" required />
              </div>

              <div class="col-md-6">
                <label class="form-label">Department</label>
                <input v-model="doctor.department" type="text" class="form-control" required  disabled/>
              </div>
              <div class="col-md-6">
                <label class="form-label">Experience (Years)</label>
                <input v-model="doctor.experience" type="number" min="0" class="form-control" />
              </div>

              <div class="col-md-6">
                <label class="form-label">Gender</label>
                <select v-model="doctor.gender" class="form-select" required>
                  <option disabled value="">Select gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div class="col-md-6">
                <label class="form-label">Email</label>
                <input v-model="doctor.email" type="email" class="form-control" required />
              </div>

              <div class="col-md-6">
                <label class="form-label">Phone Number</label>
                <input v-model="doctor.phone" type="text" class="form-control" required />
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
  name: "DoctorEditProfile",
  data() {
    return {
      bgcolor: "lightblue",
      doctor: {
        id: "",
        name: "",
        department_name: "",
        experience: "",
        email: "",
        gender: "",
        phone_no: "",
      },
    };
  },
  async created() {
    const id = this.$route.params.id;
    await this.fetchDoctorProfile(id);
  },
  methods: {
    async fetchDoctorProfile(id) {
      try {
        const res = await axiosInstance.get(`/doctor/${id}/profile`);
        this.doctor = res.data;
        console.log("Doctor data:", res.data);
      } catch (err) {
        console.error("Error loading doctor profile:", err);
      }
    },
    async updateProfile() {
      try {
        await axiosInstance.put(`/doctor/${this.doctor.id}/profile`, this.doctor);
        alert("Profile updated successfully!");
        this.$router.push(`/doctor/${this.doctor.id}/profile`);
      } catch (err) {
        console.error("Error updating doctor profile:", err);
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
