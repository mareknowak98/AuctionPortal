<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">
    <div v-if="token != null">
      <h1>Choose a converastions with user:</h1>
      <b-list-group v-for="user in users_with_messages" :key="user.usermessToUser__id">
        <b-list-group-item :to="$basePath + '/message/' + user.usermessToUser__id + '/'">
          <p>{{ user.usermessToUser__username }}</p>
        </b-list-group-item>
      </b-list-group>
    </div>




    <div v-else>
    <h1>Log in to see messages</h1>
    </div>
  </b-jumbotron>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import {TokenService} from '../store/service';
import axios from 'axios';

  export default {
    name: "UserManager",
    components:{
        Navbar,
    },
    computed: {

    },
    data() {
      return {
        users_with_messages: [],
      }
    },

    mounted: function () {

    },

    methods:{
        getUsersMessaged(){
          let axiosConfig = {
              headers: {
              'Authorization': 'Token ' + this.token
              }
          };
          axios.get(`http://127.0.0.1:8000/api/get_messages_user_list`, axiosConfig)
          .then(res => console.log(this.users_with_messages = res.data))
          .catch(err => console.log(err))
        }
    },
    created() {
      let token;
      this.token = TokenService.getToken();
      this.getUsersMessaged();
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
