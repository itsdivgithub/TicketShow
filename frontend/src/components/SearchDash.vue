<template>
  <div>
    <UserNav v-if="isAuthenticated && isUser" />
    <div class="venue-search" v-if="isAuthenticated && isUser">
      <h2>Search Venues</h2>
      <div class="search-input">
        <input type="text" v-model="searchQuery" @keyup.enter="searchVenues" />
        <button class="btn btn-primary" @click="searchVenues">Search</button>
      </div>
      <div class="venue-cards">
        <div v-if="showNoVenuesMessage" class="no-venues">
          <p>No venues found.</p>
        </div>
        <div v-else v-for="venue in venues" :key="venue.id" class="venue-card">
          <p><strong>Name:</strong> {{ venue.name }}</p>
          <p><strong>Place:</strong> {{ venue.place }}</p>
          <p><strong>Location:</strong> {{ venue.location }}</p>
          <router-link :to="`/postedshows/${venue.id}/shows`" class="btn btn-secondary mt-2">Get Shows</router-link>
        </div>
      </div>
    </div>
    <div v-else>
      <h1>Login as a user to access this page!</h1>
    </div>
  </div>
</template>

<script>
import UserNav from './UserNav.vue';
import axios from 'axios';

export default {
  name: 'VenueSearch',
  components: {
    UserNav,
  },
  data() {
    return {
      isAuthenticated: false,
      searchQuery: '',
      venues: [],
      showNoVenuesMessage: false, 
      isUser: false
    };
  },
  created() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
      this.isUser=true;
    } else {
      this.isAuthenticated = false;
      this.isUser = false;
    }
  },
  methods: {
    searchVenues() {
      axios
        .get(`http://127.0.0.1:5000/api/search?place=${this.searchQuery}`,{
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
        })
        .then((response) => {
          this.venues = response.data;
          this.showNoVenuesMessage = this.venues.length == 0; 
          this.isUser=true;
        })
        .catch((error) => {
          console.error(error);
          this.isUser=false;
        });
    },
  },
};
</script>

<style scoped>
.venue-search {
  margin: 70px auto 0;
  max-width: 800px; 
  text-align: center;
}

h2 {
  margin-top: 20px;
}

.btn-secondary {
  width: 60%;
}

.search-input {
  margin-top: 20px;
}

.search-input input {
  margin-right: 10px; 
}

.venue-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 30px;
}

.venue-card {
  width: 220px;
  background-color: #f2f2f2;
  color: #000;
  padding: 20px;
  margin: 10px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.no-venues {
  text-align: center;
  font-style: italic;
  color: #777;
  margin-top: 30px;
}
</style>
