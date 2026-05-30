<template>
  <div :style="{ backgroundColor: bgcolor }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4">

          <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="fw-bold text-primary">Welcome {{ doctorName }}</h4>
            <div>
              <router-link :to="`/doctor/edit/profile/${this.doctor_id}`" class="text-decoration-none text-secondary me-3">Edit Profile</router-link>
              <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
            </div>
          </div>

          <section class="mb-5">
            <h5 class="fw-semibold text-dark mb-3">Upcoming Appointments</h5>
            <div class="table-responsive">
              <table class="table align-middle text-center">
                <thead class="table-primary text-dark">
                  <tr>
                    <th>Sr No.</th>
                    <th>Patient Name</th>
                    <th>Patient History</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
  v-for="(appt, index) in appointments.filter(a => a.status === 'booked')"
  :key="appt.id"
>
  <td>{{ index + 1 }}</td>
  <td>{{ appt.patient_name }}</td>
  <td>
    <button class="btn btn-outline-primary btn-sm me-2" @click="updateHistorypage(appt.patient_id)">
      Update
    </button>
  </td>
    <td>
      <button class="btn btn-outline-success btn-sm me-2" @click="markComplete(appt.id)">
        Mark Complete
      </button>
      <button class="btn btn-outline-danger btn-sm" @click="cancelAppointment(appt.id)">
        Cancel
      </button>
    </td>
  </tr>

                  <tr v-if="appointments.filter(a => a.status === 'booked').length === 0">
                  <td colspan="4" class="text-muted">No upcoming appointments</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <section class="mb-4">
            <h5 class="fw-semibold text-dark mb-3">Assigned Patients</h5>
            <ul class="list-group">
              <li
                v-for="patient in patients"
                :key="patient.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <span class="text-capitalize">{{ patient.name }}</span>
                <button @click="gotopatienthistory(patient.id)" class="btn btn-outline-primary btn-sm">View</button>
              </li>
              <li v-if="patients.length === 0" class="list-group-item text-muted">No assigned patients</li>
            </ul>
          </section>
          <div class="text-end mt-4">
            <button class="btn btn-success px-4" @click="gotoavailabilitypage(doctor_id)">Provide Availability</button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "DoctorDashboard",
  data() {
    return {
      doctorName: "",
      appointments: [],
      patients: [],
      doctor_id:"",
      bgcolor: "lightblue", 
    };
  },
  async created() {
    await this.fetchDashboard();
  },
  methods: {
    async fetchDashboard() {
      try {
        const res = await axiosInstance.get("/doctor/dashboard");
        this.doctorName = res.data.doctor_name;
        this.appointments = res.data.appointments;
        this.patients = res.data.patients;
        this.doctor_id = res.data.doctor_id;
      } catch (err) {
        console.error(err);
      }
    },
    gotoavailabilitypage(docid){
        const doc_id = docid
      this.$router.push({ path: `/doctor/availability/${doc_id}` });
    },
    gotopatienthistory(patient_id){
      this.$router.push({ path: `/doctor/patient/${patient_id}/history` });
    },
    updateHistorypage(id){
      this.$router.push({path:`/doctor/patient/${id}/treatment`})
    },
    async markComplete(id) {
      if (!confirm("Mark this appointment as complete?")) return;
      try {
        await axiosInstance.post(`/doctor/mark_complete/${id}`);
        alert("Appointment marked complete!");
        await this.fetchDashboard(); 
      } catch (err) {
        console.error("Error marking complete", err);
      }
    },
    async cancelAppointment(id) {
      this.$router.push({path:`/doctor/cancel_appointment/${id}`})
    },
    updateHistory(id) {
      alert(`Open patient history for appointment ${id}`);
    },
    logout() {
      this.$store.dispatch("auth/logout");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Segoe UI", sans-serif;
}
.table th {
  background-color: #dbeafe !important; /* soft blue */
}
button {
  border-radius: 18px;
}
.btn-outline-danger:hover {
  background-color: #dc3545 !important;
  color: #fff !important;
}
</style>
