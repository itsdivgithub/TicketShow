<template>
  <div v-if="isAuthenticated">
    <AdminNav />
    <br />
    <div class="Showadd">
      <h2>Edit Show</h2>
      <form @submit.prevent="saveShow">
        <div class="addshow-form">
          <input v-model="showData.name" type="text" placeholder="Show" />
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
import AdminNav from './AdminNav.vue'
import axios from "axios";

export default {
  name: 'EditShow',
  components: {
    AdminNav
  },
  props: ['venue_id', 'show_id'],
  data() {
    return {
      isAuthenticated: false,
      showData: {
        name: ''
      }
    };
  },
  mounted() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.isAuthenticated = true;
      this.fetchShowData();
    } else {
      this.isAuthenticated = false;
    }
  },
  methods: {
    fetchShowData() {
      axios.get(`http://127.0.0.1:5000/api/admin/shows/${this.venue_id}/${this.show_id}`)
        .then(response => {
          this.showData = response.data.show;
        })
        .catch(error => {
          console.error('Failed to fetch show data:', error);
        });
    },
    saveShow() {
      if (!this.isAuthenticated) {
        window.alert('Please log in as an admin to edit the show.');
        return;
      }

      axios.put(`http://127.0.0.1:5000/api/admin/shows/${this.venue_id}/${this.show_id}`, this.showData, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access_token') }
      })
      .then(response => {
        console.log('Show updated:', response.data);
        this.$router.push({ name: 'ShowDash', params: { venue_id: this.venue_id } });
      })
      .catch(error => {
        console.error('Failed to update show:', error);
      });
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
</style>
