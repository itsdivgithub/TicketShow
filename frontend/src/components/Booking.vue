<template>
  <div>
    <UserNav v-if="isAuthenticated" />
    <div v-if="!loading">
      <div v-if="showCapacity > 0 && availableSeats > 0"> 
        <div class="bookingadd">
          <button v-if="show" v-text="`Available Seats: ${availableSeats !== undefined ? availableSeats : showCapacity}`"></button>
          <div class="addbooking-form" v-if="show">
            <label for="Number">Seats</label>
            <input type="number" v-model="seatsBooked" @input="calculateTotal" />
            <label for="Price">Price</label>
            <input type="text" :value="price" readonly />
            <label for="Total">Total</label>
            <input type="text" :value="total" readonly />
            <div class="button-container">
              <button @click="bookTickets">BOOK</button>
            </div>
            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          </div>
        </div>
      </div>
      <div v-else class="housefull-popup"> 
        <h5>Sorry! Show Is Housefull</h5>
        <button @click="goBack">Go Back</button>
      </div>
    </div>
  </div>
</template>

<script>
import UserNav from './UserNav.vue';
import axios from 'axios';

export default {
  name: 'Booking',
  components: {
    UserNav,
  },
  props: ['venue_id', 'show_id'],
  data() {
    return {
      isAuthenticated: false,
      venue: {},
      show: null,
      showCapacity: 0,
      seatsBooked: 0,
      availableSeats: undefined,
      price: 0,
      total: 0,
      errorMessage: '',
      loading: true, 
    };
  },
  created() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
      this.fetchData();
    } else {
      this.isAuthenticated = false;
    }
  },
  methods: {
    fetchData() {
      axios
        .get(`http://127.0.0.1:5000/api/book/venue/${this.venue_id}`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
        })
        .then((response) => {
          this.venue = response.data;
          this.showCapacity = this.venue.capacity;
          this.fetchShow();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    fetchShow() {
      axios
        .get(`http://127.0.0.1:5000/api/book/venue/${this.venue_id}/${this.show_id}`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
        })
        .then((response) => {
          this.show = response.data;
          this.getAvailableSeats(); 
          this.price = this.show.ticket_price;
          this.calculateTotal();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getAvailableSeats() {
      axios
        .get(`http://127.0.0.1:5000/api/book/venue/${this.venue_id}/show/${this.show_id}/seats`, {
          headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
        })
        .then((response) => {
          this.availableSeats = response.data.available_seats;
        })
        .catch((error) => {
          console.error(error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    calculateTotal() {
      this.total = this.seatsBooked * this.price;
    },
    bookTickets() {
      if (!this.isAuthenticated) {
        console.error('User not authenticated.');
        return;
      }

      const postData = {
        seats_booked: this.seatsBooked,
      };

      axios
        .post(
          `http://127.0.0.1:5000/api/book/venue/${this.venue_id}/show/${this.show_id}/bookings`,
          postData,
          {
            headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') },
          }
        )
        .then((response) => {
          console.log('Booking successful:', response.data.message);
          this.errorMessage = '';
          alert('Congratulations! See you at the Movie');
          this.fetchShow();
          this.$router.push(`/postedshows/${this.venue_id}/shows`);
        })
        .catch((error) => {
          console.error('Error booking show:', error);
          this.errorMessage = error.response.data.message || 'An error occurred during booking.';
        });
    },
    goBack() {
      this.$router.push(`/postedshows/${this.venue_id}/shows`);
    },
  },
  watch: {
    show: {
      handler() {
        this.getAvailableSeats(); 
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.bookingadd {
  position: fixed;
  top: 53%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 400px;
  padding: 20px;
  background-color: #ddaeae;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.addbooking-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.addbooking-form input {
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-bottom: 30px;
  margin-left: auto;
  margin-right: auto;
  border: 1px solid rgb(184, 17, 17);
}

.addbooking-form button {
  width: 200px;
  height: 40px;
  border: none;
  color: rgb(247, 242, 242);
  background-color: black;
  cursor: pointer;
}

.error-message {
  color: rgb(236, 111, 111);
}

.housefull-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 400px;
  padding: 20px;
  background-color: #bb9088;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(8, 0, 0, 0.815);
}

.housefull-popup h3 {
  margin-bottom: 20px;
}

.housefull-popup button {
  width: 150px;
  height: 40px;
  border: none;
  color: rgb(255, 253, 253);
  background-color: rgb(196, 47, 47);
  cursor: pointer;
}
</style>
