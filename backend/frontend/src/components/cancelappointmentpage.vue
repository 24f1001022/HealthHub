<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4">

          <!-- Header -->
          <div class="d-flex justify-content-between align-items-center border-bottom pb-3 mb-4">
            <h4 class="fw-bold text-primary">Cancel Appointment</h4>
            <button class="btn btn-outline-secondary btn-sm" @click="goBack">Back</button>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="text-muted text-center py-4">
            Loading appointment details...
          </div>

          <!-- Appointment Details -->
          <div v-else-if="appointment">
            <!-- Patient Information -->
            <section class="mb-4">
              <h5 class="fw-semibold text-dark border-bottom pb-2">Patient Information</h5>
              <ul class="list-group shadow-sm">
                <li class="list-group-item"><strong>Name:</strong> {{ appointment.patient_name }}</li>
                <li class="list-group-item"><strong>Email:</strong> {{ appointment.patient_email }}</li>
                <li class="list-group-item"><strong>Age:</strong> {{ appointment.patient_age }}</li>
                <li class="list-group-item"><strong>Gender:</strong> {{ appointment.patient_gender }}</li>
              </ul>
            </section>

            <!-- Appointment Details -->
            <section class="mb-4">
              <h5 class="fw-semibold text-dark border-bottom pb-2">Appointment Details</h5>
              <ul class="list-group shadow-sm">
                <li class="list-group-item"><strong>Date:</strong> {{ appointment.date }}</li>
                <li class="list-group-item"><strong>Time Slot:</strong> {{ appointment.start_time }} - {{ appointment.end_time }}</li>
                <li class="list-group-item">
                  <strong>Status:</strong>
                  <span :class="statusClass(appointment.status)">
                    {{ appointment.status }}
                  </span>
                </li>
              </ul>
            </section>

            <!-- Actions -->
            <div class="text-end">
              <button class="btn btn-outline-danger px-4" @click="cancelAppointment">
                Cancel Appointment
              </button>
            </div>
          </div>

          <!-- Not Found -->
          <div v-else class="text-danger text-center py-4">
            Appointment not found.
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "CancelAppointment",
  data() {
    return {
      appointment: null,
      loading: true,
      bgcolor: "lightblue", // matches Admin Dashboard theme
    };
  },
  async created() {
    const slotId = this.$route.params.id;
    try {
      const res = await axiosInstance.get(`/doctor/appointment-details/${slotId}`);
      this.appointment = res.data;
    } catch (err) {
      console.error("Error fetching appointment:", err);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async cancelAppointment() {
      if (!this.appointment?.id) return;

      const confirmed = confirm("Are you sure you want to cancel this appointment?");
      if (!confirmed) return;

      try {
        await axiosInstance.post(`/doctor/cancel-appointment/${this.appointment.id}`);
        alert("Appointment cancelled successfully.");
        this.$router.push("/doctor/dashboard");
      } catch (err) {
        console.error("Cancellation failed:", err);
        alert("Error cancelling appointment.");
      }
    },
    goBack() {
      this.$router.back();
    },
    statusClass(status) {
      if (status === "booked") return "text-success fw-bold";
      if (status === "cancelled") return "text-danger fw-bold";
      return "text-muted";
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Segoe UI", sans-serif;
}
.card {
  max-width: 700px;
  margin: 0 auto;
  background-color: #ffffff;
}
.list-group-item {
  background-color: #f9fafb;
}
.btn-outline-danger {
  border-color: #dc3545;
  color: #dc3545;
}
.btn-outline-danger:hover {
  background-color: #dc3545 !important;
  color: white !important;
}
.border-bottom {
  border-color: #dbeafe !important; /* soft blue underline */
}
</style>
