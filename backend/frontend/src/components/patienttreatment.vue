<template>
  <div :style="{ background: gradientBg }">
    <div class="min-vh-100 py-5">
      <div class="container">
        <div class="card shadow-lg border-0 rounded-4 p-4 glass-card">

          <!-- Header -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="fw-bold text-primary d-flex align-items-center">
              <i class="bi bi-clipboard2-heart me-2"></i>
              My Treatment History
            </h4>
            <div>
              <button
                :disabled="exporting"
                @click="exportcsv"
                class="btn btn-outline-success btn-sm me-3"
              >
                <span v-if="!exporting">
                  <i class="bi bi-download me-1"></i> Export CSV
                </span>
                <span v-else>
                  <i class="spinner-border spinner-border-sm me-1"></i> Exporting...
                </span>
              </button>

              <button @click="logout" class="btn btn-outline-danger btn-sm">
                Logout
              </button>
            </div>
          </div>

          <hr class="mb-4" />

          <!-- Show message if no valid treatments -->
          <div v-if="filteredTreatments.length === 0" class="text-center py-5">
            <i class="bi bi-emoji-frown fs-1 text-muted"></i>
            <p class="text-muted mt-2">No treatment records found.</p>
          </div>

          <!-- Show treatments -->
          <div v-else>
            <transition-group name="fade" tag="div">
              <div
                v-for="(t, i) in filteredTreatments"
                :key="i"
                class="border rounded-4 p-4 mb-4 bg-white shadow-sm treatment-card"
              >
                <h5 class="fw-bold text-secondary mb-3 d-flex align-items-center">
                  <i class="bi bi-hospital me-2 text-primary"></i>
                  {{ t.visit_type }}
                </h5>

                <div class="row">
                  <div class="col-md-6 mb-2">
                    <p><strong>🧪 Test Done:</strong> {{ t.test_done }}</p>
                  </div>
                  <div class="col-md-6 mb-2">
                    <p><strong>💊 Prescription:</strong> {{ t.prescription }}</p>
                  </div>
                </div>

                <p><strong>🩺 Diagnosis:</strong> {{ t.diagnosis }}</p>

                <div v-if="t.medicines && t.medicines.length" class="mt-3">
                  <p class="fw-bold mb-1 text-dark">
                    <i class="bi bi-capsule me-1 text-primary"></i> Medicines:
                  </p>
                  <ul class="list-unstyled ps-3">
                    <li v-for="(m, j) in t.medicines" :key="j" class="mb-1 text-muted">
                      • {{ m.name }} — {{ m.dosage }}
                    </li>
                  </ul>
                </div>

                <div class="text-end mt-3">
                  <span class="badge bg-light text-secondary border small">
                    Updated on: {{ t.created_at }}
                  </span>
                </div>
              </div>
            </transition-group>
          </div>

          <!-- Back Button -->
          <div class="text-center mt-4">
            <router-link
              to="/patient/dashboard"
              class="btn btn-outline-primary px-4 rounded-pill hover-up"
            >
              <i class="bi bi-arrow-left-circle me-2"></i> Back to Dashboard
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance, { apiOrigin } from "../plugins/axios";

export default {
  name: "PatientTreatmentView",
  data() {
    return {
      treatments: [],
      exporting: false,
      pollInterval: null,
      email:"",
      gradientBg: "linear-gradient(135deg, #d0e7ff 0%, #a6c8ff 100%)", 
    };
  },
  computed: {
    filteredTreatments() {
      return this.treatments.filter(
        (t) => t.visit_type && t.visit_type.trim() !== ""
      );
    },
  },
  async created() {
    const id = this.$route.params.id;
    await this.fetchTreatments(id);
    await this.getemail(id)
  },
  methods: {
    async fetchTreatments(id) {
      try {
        const res = await axiosInstance.get(`/patient/${id}/treatment`);
        this.treatments = res.data || [];
      } catch (err) {
        console.error(err);
      }
    },
    async getemail(id){
      try {
        const res = await axiosInstance.get(`/patient/${id}/profile`);
        this.email=res.data.email
      } catch (err) {
        console.error(err);
      }
    },
    async logout() {
      await this.$store.dispatch("auth/logout");
      this.$router.push("/login");
    },

    downloadExportFile(filepath) {
      const filename = filepath.split(/[/\\]/).pop();
      const link = document.createElement("a");
      link.href = `${apiOrigin}/exports/${filename}`;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },

    async exportcsv() {
      const id = this.$route.params.id;
      this.exporting = true;

      try {
        // Step 1: trigger export
        const res = await axiosInstance.post(
          `/patient/${id}/export-treatments`,
          { email: this.email }
        );

        const taskId = res.data.task_id;

        if (res.data.status === "finished" && res.data.filepath) {
          this.downloadExportFile(res.data.filepath);
          this.exporting = false;
          return;
        }

        // Step 2: poll task status (Celery mode)
        const poll = async () => {
          try {
            const statusRes = await axiosInstance.get(
              `/patient/${id}/export-status/${taskId}`
            );

            const data = statusRes.data;

            if (data.status === "finished" && data.filepath) {
              clearInterval(this.pollInterval);
              this.pollInterval = null;
              this.downloadExportFile(data.filepath);
              this.exporting = false;
            } else if (data.status === "failed") {
              clearInterval(this.pollInterval);
              this.exporting = false;
              alert("Export failed: " + (data.error || "Unknown error"));
            }
          } catch (e) {
            console.error(e);
          }
        };
        this.pollInterval = setInterval(poll, 3000);
      } catch (err) {
        console.error(err);
        this.exporting = false;
        alert("Failed to trigger export.");
      }
    },
  },
  beforeUnmount() {
    if (this.pollInterval) clearInterval(this.pollInterval);
  },
};
</script>

<style scoped>
body {
  font-family: "Segoe UI", sans-serif;
}


.glass-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
}

/* Treatment card hover */
.treatment-card {
  transition: all 0.25s ease;
}
.treatment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

/* Button hover animation */
.hover-up {
  transition: transform 0.2s ease;
}
.hover-up:hover {
  transform: translateY(-2px);
}

/* Link hover */
.hover-link:hover {
  color: #0d6efd !important;
}

/* Fade animation for list items */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
