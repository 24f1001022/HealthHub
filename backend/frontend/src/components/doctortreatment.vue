<template>
  <div :style="{ backgroundColor: bgcolor }" class="min-vh-100 py-5">
    <div class="container">
      <div class="card shadow-lg border-0 rounded-4 p-4">

        <h4 class="fw-bold text-primary mb-3">Update Patient History</h4>
        <p><strong>Patient Name:</strong> {{ patient.name }}</p>
        <p><strong>Gender:</strong> {{ patient.gender }}</p>

        <form @submit.prevent="saveTreatment">
          <div class="row g-3">
            <!-- Visit Type -->
            <div class="col-md-6">
              <label class="form-label">Visit Type</label>
              <select v-model="form.visit_type" class="form-select" required>
                <option disabled value="">Select Visit Type</option>
                <option value="Online">Online</option>
                <option value="In-Person">In-Person</option>
              </select>
            </div>

            <!-- Test Done -->
            <div class="col-md-6">
              <label class="form-label">Test Done</label>
              <input
                type="text"
                v-model="form.test_done"
                class="form-control"
                placeholder="Enter test name or N/A"
              />
            </div>

            <!-- Diagnosis -->
            <div class="col-md-12">
              <label class="form-label">Diagnosis</label>
              <textarea
                v-model="form.diagnosis"
                class="form-control"
                rows="2"
                placeholder="Enter diagnosis details"
              ></textarea>
            </div>

            <!-- Prescription -->
            <div class="col-md-12">
              <label class="form-label">Prescription</label>
              <textarea
                v-model="form.prescription"
                class="form-control"
                rows="2"
                placeholder="Enter prescription details"
              ></textarea>
            </div>

            <!-- Medicines -->
            <div class="col-md-12">
              <label class="form-label d-flex justify-content-between align-items-center">
                <span>Medicines</span>
                <button
                  type="button"
                  class="btn btn-sm btn-outline-success"
                  @click="addMedicine"
                >
                  + Add
                </button>
              </label>
              <div
                v-for="(med, index) in form.medicines"
                :key="index"
                class="d-flex mb-2 align-items-center"
              >
                <input
                  v-model="med.name"
                  placeholder="Medicine Name"
                  class="form-control me-2"
                />
                <input
                  v-model="med.dosage"
                  placeholder="Dosage (e.g. 1-0-1)"
                  class="form-control me-2"
                />
                <button
                  type="button"
                  class="btn btn-outline-danger btn-sm"
                  @click="removeMedicine(index)"
                >
                  x
                </button>
              </div>
            </div>
          </div>

          <!-- Save Button -->
          <div class="text-end mt-4">
            <button type="submit" class="btn btn-success px-4">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "DoctorTreatment",
  data() {
    return {
      bgcolor: "lightblue", 
      patient: {},
      form: {
        visit_type: "",
        test_done: "",
        diagnosis: "",
        prescription: "",
        medicines: [],
        appointment_id: "",
      },
    };
  },
  async created() {
    await this.fetchdetails();
  },
  methods: {
    async fetchdetails() {
      try {
        const patientId = this.$route.params.id;
        const response = await axiosInstance.get(`/patient/${patientId}`);
        const data = response.data;

        this.patient = {
          name: data.name || "Unknown",
          gender: data.gender || "N/A",
        };

        this.form.visit_type = data.visit_type || "";
        this.form.test_done = data.test_done || "";
        this.form.diagnosis = data.diagnosis || "";
        this.form.prescription = data.prescription || "";
        this.form.appointment_id = data.appointment_id;

        if (Array.isArray(data.medicines)) {
          this.form.medicines =
            data.medicines.length > 0
              ? data.medicines
              : [{ name: "", dosage: "" }];
        } else if (
          typeof data.medicines === "string" &&
          data.medicines.trim() !== ""
        ) {
          try {
            this.form.medicines = JSON.parse(data.medicines);
          } catch {
            this.form.medicines = [{ name: data.medicines, dosage: "" }];
          }
        } else {
          this.form.medicines = [{ name: "", dosage: "" }];
        }
      } catch (error) {
        console.error("Error fetching patient details:", error);
        alert("Failed to load patient details");
      }
    },

    addMedicine() {
      this.form.medicines.push({ name: "", dosage: "" });
    },

    removeMedicine(index) {
      this.form.medicines.splice(index, 1);
    },

    async saveTreatment() {
      try {
        const patientId = this.$route.params.id;
        await axiosInstance.post(`/patient/${patientId}/treatment`, this.form);
        alert("Treatment saved successfully!");
        this.$router.push("/doctor/dashboard");
      } catch (err) {
        console.error(err);
        alert("Error saving treatment");
      }
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Segoe UI", sans-serif;
}

label {
  font-weight: 600;
  color: #0d47a1;
}

textarea,
input,
select {
  border-radius: 10px;
}

.card {
  background-color: #ffffff;
}

.btn-success {
  border-radius: 20px;
  background-color: #198754;
}

.btn-outline-success {
  border-radius: 20px;
}

.btn-outline-danger {
  border-radius: 20px;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: #fff;
}

.form-control,
.form-select {
  border: 1px solid #d0d7de;
}

.text-primary {
  color: #0d47a1 !important;
}
</style>
