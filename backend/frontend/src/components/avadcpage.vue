<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4">
          <!-- Header -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="fw-bold text-primary m-0">Doctor's Availability</h4>
            <button class="btn btn-outline-danger btn-sm" @click="goBack">Back</button>
          </div>

          <!-- Availability Slots -->
          <div v-if="Object.keys(availability).length" class="mb-4">
            <div
              v-for="(slots, date) in availability"
              :key="date"
              class="border rounded-3 p-3 bg-white shadow-sm mb-3"
            >
              <h5 class="fw-semibold mb-3 text-dark">{{ date }}</h5>
              <div class="d-flex flex-wrap gap-2">
                <button
                  v-for="slot in slots"
                  :key="slot.id"
                  class="btn"
                  :class="getSlotClass(slot)"
                  :disabled="slot.status === 'booked'"
                  @click="toggleSlot(slot)"
                >
                  {{ slot.start_time }} - {{ slot.end_time }}
                </button>
              </div>
            </div>
          </div>

          <!-- No Slots -->
          <div v-else class="text-center text-muted my-5">
            No availability data found.
          </div>

          <!-- Save Button -->
          <div class="text-end mt-4">
            <button class="btn btn-primary px-4" @click="saveAvailability">Save</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "DoctorAvailability",
  data() {
    return {
      availability: {}, // now an object grouped by date
      doc_id: null,
      bgcolor: "lightblue",
    };
  },
  async created() {
    this.doc_id = this.$route.params.id;
    if (this.doc_id) {
      await this.fetchAvailability(this.doc_id);
    } else {
      alert("No doctor ID provided.");
      this.$router.push("/doctors");
    }
  },
  methods: {
    async fetchAvailability(id) {
      try {
        const res = await axiosInstance.get(`/doctor/availability/${id}`);
        this.availability = res.data;
      } catch (err) {
        console.error(err);
      }
    },
    getSlotClass(slot) {
      if (slot.status === "booked") return "btn-danger";
      if (slot.status === "available") return "btn-success";
      if (slot.status === "unavailable") return "btn-outline-secondary";
      return "btn-outline-dark";
    },
    toggleSlot(slot) {
  if (slot.status === "booked") {
    // Redirect to cancel appointment page with slot ID
    this.$router.push(`/doctor/cancel_appointment/${slot.id}`);
  } else {
    // Toggle between available and unavailable
    slot.status = slot.status === "available" ? "unavailable" : "available";
  }
},
    async saveAvailability() {
      try {
        const flatData = [];
        for (const [date, slots] of Object.entries(this.availability)) {
          for (const s of slots) {
            flatData.push({
              id: s.id,
              date,
              status: s.status,
            });
          }
        }
        await axiosInstance.post(`/doctor/availability/${this.doc_id}`, flatData);
        alert("Availability updated successfully!");
      } catch (err) {
        console.error(err);
        alert("Error saving availability");
      }
    },
    goBack() {
      this.$router.push("/doctor/dashboard");
    },
  },
};
</script>

<style scoped>
button {
  border-radius: 18px;
  min-width: 120px;
}
.btn-success {
  background-color: #28a745;
  color: white;
}
.btn-danger {
  background-color: #dc3545;
  color: white;
}
.table th {
  background-color: #dbeafe !important;
}
</style>
