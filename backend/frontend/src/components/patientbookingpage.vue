<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4">

          <!-- Header -->
          <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-2">
            <h4 class="fw-bold text-primary">Doctor's Availability</h4>
            <button @click="back" class="btn btn-outline-danger btn-sm">Back</button>
          </div>

          <!-- Availability Slots -->
          <div v-if="Object.keys(availability).length">
            <div v-for="(slots, date) in availability" :key="date" class="mb-4">
              <h5 class="text-dark fw-semibold mb-3">{{ date }}</h5>
              <div class="row g-2">
                <div v-for="slot in slots" :key="slot.id" class="col-6 col-md-3">
                  <button
                    class="btn w-100"
                    :class="getSlotClass(slot)"
                    :disabled="slot.status !== 'available'"
                    @click="selectSlot(slot)"
                  >
                    {{ slot.start_time }} - {{ slot.end_time }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- No Slots -->
          <div v-else class="text-center text-muted my-5">
            No availability data found.
          </div>

          <!-- Book Button -->
          <div class="d-flex justify-content-end mt-4">
            <button @click="bookSlot" class="btn btn-outline-success px-4">Book</button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  data() {
    return {
      doctorId: this.$route.params.docid,
      availability: {},
      selectedSlot: null,
      bgcolor: "lightblue",
    };
  },
  async mounted() {
    await this.fetchAvailability(); // Load availability on page load
  },
  methods: {
    async fetchAvailability() {
      try {
        const res = await axiosInstance.get(`/doctor/${this.doctorId}/availability`);
        this.availability = res.data;
      } catch (err) {
        console.error("Error fetching availability:", err);
        alert("Failed to fetch availability");
      }
    },
    getSlotClass(slot) {
      if (this.selectedSlot?.id === slot.id) return "btn-primary";
      if (slot.status === "booked") return "btn-danger";
      if (slot.status === "unavailable") return "btn-secondary";
      if (slot.status === "available") return "btn-success";
      return "btn-outline-dark";
    },
    selectSlot(slot) {
      if (slot.status === "available") {
        this.selectedSlot = slot;
      }
    },
    async bookSlot() {
      if (!this.selectedSlot) {
        alert("Please select an available slot first.");
        return;
      }

      try {
        const res = await axiosInstance.post("/book-slot", {
          slot_id: this.selectedSlot.id,
        });

        alert(res.data.message);

        // Refresh slots
        await this.fetchAvailability();
        this.selectedSlot = null;
      } catch (err) {
        console.error("Booking error:", err);
        alert("Failed to book slot.");
      }
    },
    back() {
      this.$router.push("/patient");
    },
  },
};
</script>

<style scoped>
button {
  border-radius: 18px;
  min-width: 120px;
}

/* Colors */
.btn-success {
  background-color: #28a745;
  color: white;
}
.btn-danger {
  background-color: #dc3545;
  color: white;
}
.btn-secondary {
  background-color: #d6d8db;
  color: #6c757d;
  cursor: not-allowed;
}
.btn-primary {
  background-color: #0d6efd;
  color: white;
}
</style>
