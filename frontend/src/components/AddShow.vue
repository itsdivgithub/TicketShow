<template>
  <div>
    <AdminNav v-if="isAuthenticated" />
    <br />
    <div v-if="isAuthenticated">
      <form class="Showadd" @submit.prevent="saveShow">
        <h2>Create New Show</h2>
        <div class="addshow-form">
          <input v-model="showData.name" type="text" placeholder="Show" required />

          <input
            v-model.number="showData.rating"
            type="number"
            placeholder="Ratings"
            min="1"
            max="10"
            step="0.1"
            required
          />

          <label for="Timing">Timing</label>
          <input v-model="showData.timings" type="text" @blur="convertTo12HourFormat" placeholder="Timings" required />

          <input v-model="showData.tags" type="text" placeholder="Tags" required />

          <input v-model.number="showData.ticket_price" type="number" placeholder="Price" required />

          <div class="button-container">
            <button type="submit">Save</button>
          </div>
        </div>
      </form>
    </div>
    <div v-else>
      <h1>You need to log in as an admin to access this page..</h1>
    </div>
  </div>
</template>

<script>
import AdminNav from './AdminNav.vue';
import axios from 'axios';

export default {
  name: 'AddShow',
  components: {
    AdminNav,
  },
  props: ['venue_id'], 
  data() {
    return {
      isAuthenticated: false,
      showData: {
        name: '',
        rating: '',
        timings: '', 
        tags: '',
        ticket_price: '',
      },
    };
  },
  mounted() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
    } else {
      this.isAuthenticated = false;
    }
  },
  methods: {
    saveShow() { 

      axios
        .post(`http://127.0.0.1:5000/api/admin/shows/${this.venue_id}`, {
          ...this.showData,
          venue_id: this.venue_id, 
        },{
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
        .then(response => {
          console.log('Show data saved:', response.data);
          window.alert('Show created successfully!');
          this.$router.push({ name: 'ShowDash', params: { venue_id: this.venue_id } });
        })
        .catch(error => {
          console.error('Failed to save show data:', error);
        });
    },
    convertTo12HourFormat() {
      if (this.showData.timings) {
        const [hours, minutes] = this.showData.timings.split(':');
        let formattedHours = parseInt(hours);
        let period = 'AM';

        if (formattedHours === 0) {
          formattedHours = 12;
        } else if (formattedHours > 12) {
          formattedHours -= 12;
          period = 'PM';
        }

        this.showData.timings = `${formattedHours.toString().padStart(2, '0')}:${minutes} ${period}`;
      }
    }
  }
};
</script>

<style>
.Showadd {
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
.addshow-form input {
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-bottom: 30px;
  margin-left: auto;
  margin-right: auto;
  border: 1px solid black;
}
.addshow-form button {
  align-self: center;
  width: 200px;
  height: 40px;
  border: blue;
  color: gainsboro;
  background-color: black;
  cursor: pointer;
}
.button-container {
  display: flex;
  justify-content: center;
  width: 100%;
}
.connect-text {
  position: fixed;
  top: 50%;
  left: 30%;
  font-size: 35px;
  font-weight: auto;
}
</style>
