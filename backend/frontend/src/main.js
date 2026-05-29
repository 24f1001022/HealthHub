import { createApp } from 'vue';
import App from './App.vue';
import store from './store/store';
import router from './router/router';

const app = createApp(App);

app.use(store);

// First, try loading the user
store.dispatch('auth/loadUser').finally(() => {
  app.use(router); // Use router only after user is (possibly) loaded
  app.mount('#app');
});
