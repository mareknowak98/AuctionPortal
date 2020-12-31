<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">
    <div v-if="token != null">
      <h1>Send message to:</h1>
      <b-list-group v-for="user in users_with_messages" :key="user.usermessToUser__id">
        <b-list-group-item :to="'/message/' + user.usermessToUser__id + '/'">
          <b-avatar button v-on:click="$goToAnotherPage('/profile/' + user.usermessToUser__id)" :src="user.profile.profileAvatar" size="5rem" variant="primary" text="FF"></b-avatar>
          {{ user.usermessToUser__username }}
        </b-list-group-item>
      </b-list-group>
    </div>

    <div v-else>
    <h1>Log in to see messages</h1>
    </div>
  <Footer></Footer>
  </b-jumbotron>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import Footer from './Footer.vue';
import {TokenService} from '../store/service';
import axios from 'axios';

  export default {
    name: "UserManager",
    components:{
        Navbar,
        Footer,
    },
    computed: {

    },
    data() {
      return {
        users_with_messages: [],
        temp_profile: null,
      }
    },

    mounted: function () {

    },

    methods:{
      getProfileData(id, index){
        let axiosConfig = {
            headers: {
                'Authorization': 'Token ' + localStorage.getItem("user-token")
            }
        };
        var result
        axios.get(`https://auctionportalbackend.herokuapp.com/api/profileUser/getUserImage?user_id=` + id, axiosConfig)
            .then(res => result = res.data)
            .then(res =>{
              this.$set(this.users_with_messages[index], "profile", result)
            })
            .catch(err => console.log(err))
      },

      getUsersMessaged(){
        let axiosConfig = {
            headers: {
            'Authorization': 'Token ' + this.token
            }
        };
        axios.get(`https://auctionportalbackend.herokuapp.com/api/get_messages_user_list`, axiosConfig)
        .then(res => this.users_with_messages = res.data)
        .then(res => {
          for (let user in this.users_with_messages){
            let tmp = this.getProfileData(this.users_with_messages[user].usermessToUser__id, user)
          }

        })
        .catch(err => console.log(err))
      },
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
