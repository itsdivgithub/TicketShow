<template>
  <div v-if="isAuthenticated">
    <AdminNav />
    <br />
    <div class="venueadd">
      <h2>Creating A New Venue</h2>
      <form class="addvenue-form" @submit.prevent="createVenue">
        <div class="form-group">
          <label for="Venue">Name</label>
          <input type="text" v-model="name" class="form-control" placeholder="Name" required />
        </div>
        <div class="form-group">
          <label for="Place">Place</label>
          <input type="text" v-model="place" class="form-control" placeholder="Place" required />
        </div>
        <div class="form-group">
          <label for="Location">Location</label>
          <input type="text" v-model="location" class="form-control" placeholder="Location" required />
        </div>
        <div class="form-group">
          <label for="Capacity">Capacity</label>
          <input type="text" v-model="capacity" class="form-control" placeholder="Capacity" required />
        </div>
        <div class="button-container">
          <button type="submit" class="btn btn-primary" @click.prevent="createVenue">
            Save
          </button>
        </div>
      </form>
    </div>
  </div>
    <div v-else>
      <h1>You need to log in as an admin to access this page.</h1>
    </div>
</template>

<script>
import axios from "axios";
import AdminNav from './AdminNav.vue'

export default {
  name: "AddVenue",
  components: {
    AdminNav
  },
  data() {
    return {
      isAuthenticated: false,
      name: "",
      place: "",
      location: "",
      capacity: ""
    };
  },
  mounted() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
    }
  },
  methods: {
    createVenue() {
      const venueData = {
        name: this.name,
        place: this.place,
        location: this.location,
        capacity: this.capacity
      };

      axios.post("http://127.0.0.1:5000/api/admin/venue", venueData, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
      .then(response => {
        console.log(response.data);
        alert("Venue Added Successfully");
        this.$router.push("/admindash");
      })
      .catch(error => {
        console.error(error);
        alert("Can't Add Venue! Try Again");
      });
    }
  }
};
</script>



  <style>
  .venueadd {
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
  
  .addvenue-form input {
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-left: auto;
    margin-right: auto;
    border: 1px solid black;
  }
  
  .addvenue-form button {
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
  </style>