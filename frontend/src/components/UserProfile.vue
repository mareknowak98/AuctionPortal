<template>
  <div class="container">
  <h1 class="title"> Profile Update </h1>
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">

  <div v-if="token != null">
    <b-list-group v-for="profile in profileData" :key="profile.id">
        {{ profile }}
    </b-list-group>
  <b-button variant="outline-primary" v-on:click="$goToAnotherPage('/message/' + profileData.profileUser.id + '/')">Write message</b-button>

  </div>




  <div v-else>
  <h1>Log in to see other's profiles</h1>
  </div>
  </b-jumbotron>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import {TokenService} from '../store/service';
import axios from 'axios';

  export default {
    name: "Profile",
    components:{
        Navbar,
    },
    computed: {

    },
    data() {
      return {
        userId: '',
        profileData: [],
        profileId: '',
      }
    },

    mounted: function () {
          this.profileId = this.$route.params.profileId;
          this.getProfile(this.profileId)
        },

    methods:{
      getProfile(id){
      let axiosConfig = {
          headers: {
          'Authorization': 'Token ' + this.token
          }
      };
      axios.get(`http://127.0.0.1:8000/api/profileUser/` + id + '/', axiosConfig)
      .then(res => this.profileData = res.data)
      .catch(err => console.log(err))
      },


    },
    created() {
      let token;
      this.token = TokenService.getToken();
      this.userId = this.$getUserId();
      this.getProfile();
    }
  }
</script>

<style scoped>
@media (min-width: 100px) {
    .container{
        max-width: 1400px;
    }
}
</style>
