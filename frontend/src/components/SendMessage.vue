<template>
  <div class = jumbotron>
  <h1 class="title"> Send message to user: {{this.userToId}} </h1>
  <navbar></navbar>

  <div v-if="token != null">
    <h1>---</h1>
    <!-- <b-list-group v-for="profile in profileData" :key="profile.id">
        {{ profile }}
    </b-list-group> -->
    
    <b-form-textarea
      id="textarea"
      v-model="messageText"
      placeholder="Enter message..."
      rows="3"
      max-rows="6"
    ></b-form-textarea>
    
    
    
    <b-button variant="outline-primary" v-on:click="sendMessage()">Send</b-button>

  </div>

  


  <div v-else>
  <h1>Log in to send messages</h1>
  </div>

  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import {TokenService} from '../store/service';
import axios from 'axios';

  export default {
    name: "UserMessage",
    components:{
        Navbar,
    },
    computed: {

    },
    data() {
      return {
        userToId: '',
        messageText: '',
      }
    },

    mounted: function () {

    },

    methods:{
      sendMessage(){
          const formData = new FormData();
          formData.append("to_user_id", this.userToId)
          formData.append("text", this.messageText)

          let axiosConfig = {
              headers: {
                  'Authorization': 'Token ' + localStorage.getItem("user-token")
              }
          };
          axios.post(`http://127.0.0.1:8000/api/messaging/send/`, formData, axiosConfig)
              .then(res => console.log(res.data))
              .catch(err => console.log(err))
          console.log("test" + this.profileId)
      },
        
    },
    created() {
      let token;
      this.token = TokenService.getToken();
      this.userToId = this.$route.params.userId;
    }
  }
</script>

<style scoped>

</style>