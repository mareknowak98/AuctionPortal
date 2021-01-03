<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">
    <div v-if="token != null">
      <b-container class="bv-example-row">
        <b-row class="justify-content-md-center">
          <b-col col lg="8">
            <h1>Messages:</h1>
            <b-list-group v-for="user in users_with_messages" :key="user.usermessFromUser__id">
              <b-list-group-item :to="'/message/' + user.usermessFromUser_id + '/'">
                <b-avatar button v-on:click="$goToAnotherPage('/profile/' + user.usermessFromUser__id)" :src="user.profile.profileAvatar" size="5rem" variant="primary" text="FF"></b-avatar>
                {{ user.usermessFromUser__username }}
              </b-list-group-item>
            </b-list-group>
          </b-col>
      </b-row>
    </b-container>
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
            .then(res => console.log(result = res.data))
            .then(res =>{
              this.$set(this.users_with_messages[index], "profile", result)
            })
            .catch(err => console.log(err))
      },

      getUsersMessaged(){
        let axiosConfig = {
            headers: {
            'Authorization': 'Token ' + localStorage.getItem("user-token")
            }
        };
        axios.get(`https://auctionportalbackend.herokuapp.com/api/get_messages_user_list`, axiosConfig)
        .then(res => this.users_with_messages = res.data)
        .then(res => {
          let tmp_list = []
          for (let user in this.users_with_messages){
            console.log(this.users_with_messages[user])
            let tmp;
            if ('usermessToUser__id' in this.users_with_messages[user]){
              console.log("Es")
              tmp = {'usermessFromUser_id' : this.users_with_messages[user].usermessToUser__id, 'usermessFromUser__username': this.users_with_messages[user].usermessToUser__username}
            }
            else
              tmp = this.users_with_messages[user]
            tmp_list.push(tmp)
          }
          this.users_with_messages = [...new Map(tmp_list.map(item => [item['usermessFromUser_id'], item])).values()]

        })
        .then(res => {
          for (let user in this.users_with_messages){
            let tmp = this.getProfileData(this.users_with_messages[user].usermessFromUser_id, user)
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
