import { createRouter, createWebHistory } from 'vue-router';
import store from '../store/store';
import signuppage from '../components/signuppage.vue'
import patientdashboard from '../components/patientdashboard.vue'
import doctordashboard from '../components/doctordashboard.vue'
import admindashboard from '../components/admindashboard.vue'
import loginpage from '../components/loginpage.vue'
import patientdeptdetails from '../components/patientdeptdetails.vue';
import adddoctorpage from '../components/adddoctorpage.vue';
import adddepartment from '../components/adddepartment.vue';
import deletedoctorpage from '../components/deletedoctorpage.vue';
import alldoctorpage from '../components/alldoctorpage.vue';
import allpatientspage from '../components/allpatientspage.vue';
import Avadcpage from '../components/avadcpage.vue';
import patientbookingpage from '../components/patientbookingpage.vue';
import patientdoctordetails from '../components/patientdoctordetails.vue';
import patienttreatment from '../components/patienttreatment.vue';
import doctortreatment from '../components/doctortreatment.vue';
import cancelappointmentpage from '../components/cancelappointmentpage.vue';
import Patienthistory from '../components/patienthistory.vue';
import Patientditprofilepage from '../components/patientditprofilepage.vue';
import Doctoreditprofile from '../components/doctoreditprofile.vue';
import Deletepatinets from '../components/deletepatinets.vue';
const routes = [
  { path: '/login', component: loginpage },
  { path: '/signup', component: signuppage },
  { path: '/patient', component: patientdashboard, meta: { requiresAuth: true, role: 'patient' } },
  { path: '/patient/appointment/:docid',component: patientbookingpage, meta: { requiresAuth: true, role: 'patient'}},
  { path: '/patient/:id/treatment',component: patienttreatment,meta:{ requiresAuth: true,role: 'patient'}},
  { path: '/patient/doctor_detais/:docid',component: patientdoctordetails,meta:{ requiresAuth: true,role:'patient'}},
  { path: "/patient/department/:dept_id", component: patientdeptdetails,  meta: { requiresAuth: true, role: 'patient' } },
  { path: "/patient/edit/profile/:id",component:Patientditprofilepage,meta:{requiresAuth:true,role:'patient'}},
  { path: '/doctor', component: doctordashboard, meta: { requiresAuth: true, role: 'doctor' } },
  { path: "/doctor/cancel_appointment/:id",component: cancelappointmentpage,meta:{requiresAuth:true , role: 'doctor'}},
  { path: '/doctor/availability/:id' ,component: Avadcpage,meta: { requiresAuth: true, role: 'doctor' }},
  { path: '/doctor/patient/:id/history',component:Patienthistory,meta:{requiresAuth: true,role: 'doctor'}},
  { path: '/doctor/edit/profile/:id',component:Doctoreditprofile,meta:{requiresAuth:true,role: 'doctor'}},
  { path: '/doctor/patient/:id/treatment',component: doctortreatment,meta:{ requiresAuth:true,role:'doctor'}},
  { path: "/admin/add-doctor", component: adddoctorpage ,meta: { requiresAuth: true, role: 'admin' } },
  { path: "/admin/delete-doctor/:id", component: deletedoctorpage, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin/delete-patient/:id',component: Deletepatinets,meta: {requiresAuth:true,role:'admin'}},
  { path: "/admin/doctor/:id/edit",component: Doctoreditprofile,meta: {requiresAuth:true,role :'admin'}},
  { path: '/admin/patient/:id/edit', component:Patientditprofilepage,meta: {requiresAuth: true,role: 'admin'}},
  { path: "/admin/all-doctors" ,component: alldoctorpage  ,meta: { requiresAuth: true, role: 'admin' }},
  { path: "/admin/all-patients" ,component: allpatientspage  ,meta: { requiresAuth: true, role: 'admin' }},
  { path: "/admin/add-department", component: adddepartment ,meta: { requiresAuth: true, role: 'admin' } },
  { path: '/admin', component: admindashboard, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/:pathMatch(.*)*', redirect: '/login' }
];

const router = createRouter({ history: createWebHistory(), routes });

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.auth.isAuthenticated;
  const user = store.state.auth.user;

  if ((to.path === '/login' || to.path === '/signup') && isAuthenticated) {
    // Redirect logged-in users to their dashboard
    if (user.role === 'patient') return next('/patient');
    if (user.role === 'doctor') return next('/doctor');
    if (user.role === 'admin') return next('/admin');
  }
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login');
  }
  

  if (to.meta.role && user?.role !== to.meta.role) {
    return next('/login');
  }

  next();
});

export default router;
