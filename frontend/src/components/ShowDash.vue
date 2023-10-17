<template>
  <div v-if="isAdmin">
    <AdminNav />
    <div class="container mt-4">
      <div class="position-fixed top-50 start-50 translate-middle">
        <p v-if="shows.length === 0" class="connect-text">Please Add Shows!</p>
        <router-link v-if="isAdmin" :to="{ name: 'AddShow', params: { venue_id: venue_id } }" class="btn btn-primary circular-button">
          +
        </router-link>
      </div>
      <div v-if="shows.length > 0" class="myvenue-container mt-5">
        <div class="show-grid">
          <div v-for="(show, index) in shows" :key="show.id" class="show-card">
            <div class="show-details">
              <h3>{{ show.name }}</h3>
              <p>Rating: {{ show.rating }}</p>
              <p>{{ show.tags }}</p>
              <div class="button-container">
                <router-link v-if="isAdmin" :to="{ name: 'EditShow', params: { venue_id: venue_id, show_id: show.id } }" class="btn btn-secondary">
                  UPDATE
                </router-link>
                <button v-if="isAdmin" class="btn btn-danger" @click="removeShow(show.id)" style="margin-left: 10px;">REMOVE</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <h1>You need to log in as an admin to access this page.</h1>
  </div>
</template>

<script>
import axios from "axios";
import AdminNav from './AdminNav.vue';

export default { 
  name: 'ShowDash',
  components: {
    AdminNav
  },
  props: ['venue_id'],
  data() {
    return {
      isAdmin: false,
      shows: []
    };
  },
  mounted() {
    this.fetchShows()
  },
  methods: {
    fetchShows() {
      const token = localStorage.getItem('access_token');

      axios.get(`http://127.0.0.1:5000/api/admin/shows/${this.venue_id}`, {
        headers: { 'Authorization': 'Bearer ' + token }
      })
        .then(response => {
          this.shows = response.data.shows;
          this.isAdmin=true;
        })
        .catch(error => {
          console.error(error);
          this.isAdmin=false;
        });
    },
    removeShow(showId) {
      axios.delete(`http://127.0.0.1:5000/api/admin/shows/${this.venue_id}/${showId}`, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
        .then(response => {
          this.shows = this.shows.filter(show => show.id !== showId);
          console.log('Show removed:', response.data);
        })
        .catch(error => {
          console.error('Failed to remove show:', error);
        });
    }
  }
};
</script>

<style>
.show-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}
.circular-button {
  width: 100px;
  height: 100px;
  border-radius: 70%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  background-color: #007bff;
  color: #ffffff;
  cursor: pointer;
  position: fixed;
  top: 55%;
  left: 75%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  transition: 0.3s;
}

.show-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #ccc;
  background-color: antiquewhite;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.show-image {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 5px;
}

.show-details {
  margin-top: 10px;
  text-align: center;
}

.show-details h3 {
  font-size: 20px;
  margin-bottom: 5px;
}

.show-details p {
  margin: 0;
  font-size: 16px;
}

.button-container {
  margin-top: 10px;
}

.button-container button {
  margin-right: 10px;
}

.myvenue-container {
  padding-top: 40px;
  padding-bottom: 10px;
}
</style>
