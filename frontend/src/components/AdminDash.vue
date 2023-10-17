<template>
  <div>
    <AdminNav v-if="isAdmin" />
    <div v-if="isAdmin" class="container mt-4">
      <div class="position-fixed top-50 start-50 translate-middle">
        <router-link to="/addvenue" class="btn btn-primary circular-button">
          +
        </router-link>
        <h1 v-if="venues.length === 0" class="connect-text">Happy To Connect!</h1>
      </div>
      <div v-if="venues.length > 0" class="myvenue-container mt-2">
        <div class="card-group">
          <div class="row">
            <div v-for="venue in venues" :key="venue.id" class="col-md-9 mb-4">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">{{ venue.name }}</h5>
                  <h10 class="card-title">{{ venue.location }}</h10>
                  <div class="d-grid gap-2">
                    <button class="btn btn-secondary mt-2" @click="removeVenue(venue.id)">
                      Remove
                    </button>
                    <router-link
                      :to="{ name: 'EditVenue', params: { venue_id: venue.id }, props: { venue: venue }}"
                      class="btn btn-secondary mt-2"
                    >
                      Update
                    </router-link>
                    <router-link
                      :to="{ name: 'ShowDash', params: { venue_id: venue.id } }"
                      class="btn btn-secondary mt-2"
                    >
                      🍿
                    </router-link>
                    <button class="btn btn-secondary mt-2" @click="exportCSV(venue.id)">
                      Export
                    </button>
                  </div>
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
  </div>
</template>

<script>
import axios from "axios";
import AdminNav from './AdminNav.vue';

export default {
  name: 'AdminDash',
  components: {
    AdminNav
  },
  data() {
    return {
      venues: [],
      isAdmin: false,
    };
  },
  mounted() {
    this.fetchVenues();
  },
  methods: {
    fetchVenues() {
      const token = localStorage.getItem('access_token');
      axios.get('http://127.0.0.1:5000/api/admin/venue', {
        headers: { 'Authorization': 'Bearer ' + token }
      })
        .then(response => {
          this.venues = response.data;
          this.isAdmin = true;
        })
        .catch(error => {
          console.error(error);
          this.isAdmin = false;
        });
    },
    removeVenue(venueId) {
      const token = localStorage.getItem('access_token');
      axios.delete(`http://127.0.0.1:5000/api/admin/venue/${venueId}`, {
        headers: { 'Authorization': 'Bearer ' + token }
      })
        .then(response => {
          this.venues = this.venues.filter(venue => venue.id !== venueId);
          console.log(response.data.message);
          window.alert('Venue deleted successfully');
          this.$router.push('/admindash');
        })
        .catch(error => {
          console.error(error);
          window.alert('Failed to delete venue');
        });
    },
    exportCSV(venue_id) {
      const token = localStorage.getItem('access_token');

      axios.get(`http://127.0.0.1:5000/api/trigger/${venue_id}`, {
        headers: { 'Authorization': 'Bearer ' + token },
      })
      .then(response => {
        setTimeout(()=>{window.open("http://127.0.0.1:5000/api/download")}, 6000)
        
      })
      .catch(error => {
        console.error(error);
        window.alert('Failed to export CSV file');
      });
    }

  }
};
</script>


<style>
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css");

.container {
  margin-top: 50px;
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
.connect-text {
  position: fixed;
  top: 50%;
  left: 30%;
  font-size: 35px;
  font-weight: auto;
}

.card {
  width: 100%;
  margin-bottom: 2px;
  margin-top: 50px;
  margin-left: 10px;
  background-color: bisque;
}

.btn-danger,
.btn-secondary {
  width: 50%;
}

.btn-secondary {
  background-color: #0c0007;
}

.btn-danger:hover,
.btn-secondary:hover {
  background-color: #e94b0d;
}

.card-group {
  text-align: center;
  margin-right: 17px;
}

.row {
  margin-left: 0;
  margin-right: -10px;
}

.col-md-9 {
  padding: 0 2px;
}

.myvenue-container {
  max-height: 1000px;
  overflow-y: auto;
  margin-left: 0px;
  margin-right: 0;
}
</style>
