import { createStore } from 'vuex';
import axiosInstance from "../plugins/axios"

const store = createStore({
  modules: {
    auth: {
      namespaced: true,
      state: () => ({
        user: null,
        isAuthenticated: false,
      }),
      mutations: {
        SET_USER(state, user) {
          state.user = user;
          state.isAuthenticated = !!user;
        },
        LOGOUT(state) {
          state.user = null;
          state.isAuthenticated = false;
        }
      },
      actions: {
        async login({ commit }, credentials) {
          try {
            const res = await axiosInstance.post('/login', credentials, {withCredentials: true});
          if (res.data.success) {commit('SET_USER', res.data.user);
            return {success: true,user: res.data.user};}
          return {success: false,message: res.data.message || "Login failed."};
        } catch (error) {
    // Handle 4xx/5xx responses gracefully
    const message = error.response?.data?.message || "Login failed. Please try again.";
    return {
      success: false,
      message
    };
  }
},

        async signup(_, credentials) {
          try {
            const res = await axiosInstance.post('/signup', credentials, { withCredentials: true });
            return res.data;
          } catch (error) {
            const status = error.response?.status;
            const message =
              error.response?.data?.message ||
              (status === 502
                ? 'Server is waking up. Wait 30 seconds and try again.'
                : 'Signup failed. Please try again.');
            return { success: false, message };
          }
        },
        async logout({ commit }) {
          await axiosInstance.post('/logout', {}, { withCredentials: true });
          commit('LOGOUT');
        },
        async loadUser({ commit }) {
          const res = await axiosInstance.get('/me', { withCredentials: true });
          commit('SET_USER', res.data.user);
        }
      }
    }
  }
});

export default store;
