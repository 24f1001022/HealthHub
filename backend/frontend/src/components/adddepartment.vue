<template>
  <div :style="{ backgroundColor: bgcolor }" class="min-vh-100 py-5">
    <div class="container">
      <div class="card shadow-lg border-0 rounded-4 p-4 bg-white">
        <h4 class="fw-bold mb-4 text-primary">Add Department</h4>

        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label class="form-label fw-semibold">Department Name</label>
            <input
              v-model="form.dpt_name"
              type="text"
              class="form-control"
              placeholder="e.g. Cardiology"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label fw-semibold">Description</label>
            <textarea
              v-model="form.description"
              class="form-control"
              placeholder="Brief description of the department"
              rows="4"
            ></textarea>
          </div>

          <div class="text-end mt-3">
            <button class="btn btn-outline-primary px-5 rounded-pill" type="submit">
              Add Department
            </button>
          </div>
        </form>
        <div v-if="message" :class="['alert', alertClass]" class="mt-4" role="alert">
  {{ message }}
</div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "../plugins/axios";

export default {
  name: "AddDepartment",
  data() {
    return {
      bgcolor: "lightblue",
      form: {
        dpt_name: "",
        description: "",
      },
      message: "",
      alertClass: "",
    };
  },
methods: {
  async handleSubmit() {
    this.message = "";
    this.alertClass = "";

    try {
      const res = await axiosInstance.post("/admin/add_department", this.form);
      if (res.data.success) {
        this.message = res.data.message;
        this.alertClass = "alert-success";
        setTimeout(() => {
        this.message = "";
        }, 3000);

        // Optional: Wait a second, then redirect
        setTimeout(() => {
          this.$router.push("/admin/dashboard");
        }, 1500);
      } else {
        this.message = res.data.message;
        this.alertClass = "alert-warning";
      }
    } catch (err) {
      this.message = err.response?.data?.message || "Error adding department";
      this.alertClass = "alert-danger";
      setTimeout(() => {
        this.message = "";
        }, 3000);
    }
  }
}
};
</script>

<style scoped>
.container {
  max-width: 720px;
}

.card {
  background-color: #fff;
}

textarea {
  resize: none;
}

.alert {
  transition: all 0.3s ease-in-out;
}
</style>
