<template>
  <div v-if="isAuthenticated">
    <UserNav />
    <div class="container mt-4">
      <template v-if="shows.length > 0">
        <div class="show-card-container">
          <div v-for="show in shows" :key="show.id" class="show-card">
            <h3>{{ show.name }}</h3>
            <p>Rating: {{ show.rating }}</p>
            <p>{{ show.tags }}</p>
            <router-link
            :to="{ name: 'Booking', params: { venue_id: venue_id, show_id: show.id } }"
          >
            <button class="grab-tickets-btn">Grab Tickets</button>
            </router-link>
          </div>
        </div>
      </template>
      <template v-else>
        <div class="no-shows-message">
          <p><u>Sorry! No Shows Available </u>😔</p>
        </div>
      </template>
    </div>
  </div>
  <div v-else>
    <h1>You need to login as a User to access this page</h1>
  </div>
</template>

<script>
import axios from 'axios';
import UserNav from '../components/UserNav.vue';

export default {
  name: 'PostedShows',
  components: {
    UserNav
  },
  props: ['venue_id'],
  data() {
    return {
      isAuthenticated: false,
      venue: {},
      shows: []
    };
  },
  created() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
      this.fetchVenue();
      this.fetchShows();
    } else {
      this.isAuthenticated = false;
    }
  },
  methods: {
    fetchVenue() {
      axios.get(`http://127.0.0.1:5000/api/user/venue/${this.venue_id}`, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
        .then(response => {
          this.venue = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchShows() {
      axios.get(`http://127.0.0.1:5000/api/user/venue/${this.venue_id}/shows`,  {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
        .then(response => {
          this.shows = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
  }
};
</script>

<style scoped>
.show-card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  margin-top: 20px;
}

.show-card {
  background-color: #b89797; 
  color: #000; 
  margin: 10px; 
}

.show-card h3 {
  font-size: 20px;
  margin-bottom: 10px;
}

.show-card p {
  font-size: 16px;
  margin-bottom: 5px;
}

.no-shows-message {
  text-align: center;
  font-size: 30px;
  color: #811212;
  margin-top: 50px;
}

.grab-tickets-btn {
  cursor: pointer;
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 8px 8px; 
  border-radius: 5px;
  transition: background-color 0.3s;
}

.grab-tickets-btn:hover {
  background-color: #0056b3;
}


.venue-container {
  max-height: calc(100vh - 120px); 
  overflow-y: auto;
  padding-left: 20px;
  padding-right: 20px;
}
</style>
