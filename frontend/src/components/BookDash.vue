<template>
  <div>
    <UserNav v-if="isAuthenticated && isUser" />
    <div class="booking-dashboard" v-if="isAuthenticated && isUser">
     
      <div class="booking-cards">
        <div v-for="booking in userBookings" :key="booking.booking_id" class="booking-card">
          <p><strong>Show:</strong> {{ booking.show_name }}</p>
          <p><strong>Venue:</strong> {{ booking.venue_name }}</p>
          <p><strong>Time:</strong> {{ booking.show_time }}</p>
          <p><strong>Seats:</strong> {{ booking.seats_booked }}</p>
          <p><strong>Cost:</strong> ₹{{ booking.booked_cost }}</p>
        </div>
        <div v-if="userBookings.length === 0" class="no-bookings">
          <p>You have not made any bookings yet.</p>
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
  name: 'BookingDashboard',
  components: {
    UserNav,
  },
  data() {
    return {
      isAuthenticated: false,
      userBookings: [], 
      isUser: false
    };
  },
  created() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
      this.fetchUserBookings(); 
    } else {
      this.isAuthenticated = false;
    }
  },
  methods: {
    fetchUserBookings() {
      axios
        .get('http://127.0.0.1:5000/api/user/bookings', {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
        })
        .then((response) => {
          this.userBookings = response.data; 
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
.booking-dashboard {
  margin: 20px;
  text-align: center;
}

.bookings-heading {
  margin-top: 20px;
}

.booking-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 70px; 
}

.booking-card {
  width: 220px; 
  background-color: #9c8e8e; 
  color: #0a0000; 
  padding: 20px;
  margin: 10px; 
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>


