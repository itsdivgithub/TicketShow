<template>
  <div v-if="isAuthenticated">
    <AdminNav />
    <br />
    <div class="venue-edit">
      <h2>Edit Venue</h2>
      <form @submit.prevent="saveVenue">
        <div class="editvenue-form">
          <label for="venue">Venue</label>
          <input v-model="updatedVenue.name" type="text" placeholder="Venue" />
          <label for="location">Location</label>
          <input v-model="updatedVenue.location" type="text" placeholder="Location" />
          <div class="button-container">
            <button type="submit">Save</button>
          </div>
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
import AdminNav from "./AdminNav.vue";

export default {
  name: "EditVenue",
  components: {
    AdminNav,
  },
  props: ['venue'],
  data() {
    return {
      isAuthenticated: false,
      updatedVenue: {
        id: null,
        name: "",
        location: "",
      },
    };
  },
  mounted() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
      this.updatedVenue = { ...this.venue };
    } else {
      this.isAuthenticated = false;
    }
  },
  methods: {
    saveVenue() {
      const venueId = this.$route.params.venue_id;
      axios.put(`http://127.0.0.1:5000/api/admin/venue/${venueId}`, this.updatedVenue, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
      .then((response) => {
        console.log(response.data);
        window.alert("Venue updated successfully");
        this.$router.push("/admindash");
      })
      .catch((error) => {
        console.error(error);
        window.alert("Failed to update venue");
      });
    },
  }
};
</script>

<style>
.venue-edit {
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
  background-color: #ddaeae;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.editvenue-form input {
  width: 300px;
  height: 40px;
  padding-left: 20px;
  display: block;
  margin-bottom: 30px;
  margin-left: auto;
  margin-right: auto;
  border: 1px solid black;
}

.editvenue-form button {
  align-self: center;
  width: 200px;
  height: 40px;
  border: none;
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
