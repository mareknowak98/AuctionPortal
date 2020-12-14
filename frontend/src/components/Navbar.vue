<template>
  <div>
    <div v-if="$getToken() == null">

      <b-jumbotron class="jumbotron jumbotron-special" header=" ">
        <h1> </h1>
        <h1> </h1>
        <h1> </h1>
        <h1> </h1>
      <b-navbar sticky toggleable="lg" type="dark" variant="dark">
       <b-navbar-brand v-on:click="$goToAnotherPage('')">Home</b-navbar-brand>

       <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

       <b-collapse id="nav-collapse" is-nav>
         <b-nav-form>
           <b-form-input size="sm" class="mr-sm-2" placeholder="Search auctions..."></b-form-input>
           <b-button size="sm" class="my-2 my-sm-0">Search</b-button>
         </b-nav-form>
         <!-- Right aligned nav items -->
         <b-navbar-nav class="ml-auto">
           <b-nav-item v-b-modal.loginModal>Log In</b-nav-item>
           <b-nav-item v-on:click="$goToAnotherPage('/register/')">Register</b-nav-item>
         </b-navbar-nav>
       </b-collapse>
     </b-navbar>
     <b-modal id="loginModal" title="Log in" @ok="login" ok-title="Log in">
       <label class="mb-2">Please enter your username, then your password, and press Log in.</label>
       <b-form-input class="mb-2" placeholder="Username" v-model="username"></b-form-input>
       <!-- <b-form-input class="mb-2" placeholder="Email" v-model="email" autocomplete="email"></b-form-input> -->
       <b-form-input class="mb-2" placeholder="Password" v-model="password" type="password"></b-form-input>
     </b-modal>
    </b-jumbotron>
  </div>
  <div v-else>
    <b-jumbotron class="jumbotron jumbotron-special" header=" " border-variant="dark">
      <h1> </h1>
      <h1> </h1>
      <h1> </h1>
      <h1> </h1>
       <b-navbar toggleable="lg" type="dark" variant="dark">
         <b-navbar-brand v-on:click="$goToAnotherPage('')">Home</b-navbar-brand>
         <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

         <b-collapse id="nav-collapse" is-nav>
          <b-nav-form>
            <b-form-input size="sm" class="mr-sm-2" placeholder="Search auctions..."></b-form-input>
            <b-button size="sm" class="my-2 my-sm-0">Search</b-button>
          </b-nav-form>
          <b-navbar-nav>
          <b-nav-item-dropdown text="Buying" right>
            <b-dropdown-item>Auctions I've won</b-dropdown-item>
            <b-dropdown-item>Auctions I'm bidding on</b-dropdown-item>
            <b-dropdown-item>3</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item-dropdown text="Selling" right>
            <b-dropdown-item v-on:click="$goToAnotherPage('/newauction')">Create new auction</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item>Items I'm selling</b-dropdown-item>
            <b-dropdown-item>Items I've sold</b-dropdown-item>
            <b-dropdown-item>Unsold Items</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>

          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-nav-item size="sm" v-on:click="$goToAnotherPage('/messages')" class="my-2 my-sm-0"><b-icon icon="envelope" variant="success" font-scale="1.5"></b-icon></b-nav-item>
            <b-avatar variant="info" :src=profileData.profileAvatar></b-avatar>
            <b-nav-item v-on:click="goToUserPage()">My Account</b-nav-item>
            <b-nav-item v-on:click="logout()">Log Out</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
      </b-jumbotron>
    </div>
  </div>
</template>



<script>
import axios from 'axios';
  export default {
    name: "Navbar",
    components:{

    },
    data(){
      return{
        username: '',
        password: '',
        // token: localStorage.getItem('user-token') || null,
        userId: null,
        profileData: [],
      }
    },
    mounted: function (){
      this.userId = this.$getUserId()
    },
    methods: {
      goToUserPage: function () {
        this.$goToAnotherPage('/myprofile');
      },
      login(){
        axios.post('http://127.0.0.1:8000/api-token-auth/',{
          username: this.username,
          password: this.password,
        })
        .then(resp => {
        this.token = resp.data.token;
        localStorage.setItem('user-token',resp.data.token)
        this.username = '';
        this.password = '';
        })
        .then(resp =>{
          console.log(this.userId)
          this.getProfile(this.userId)
        })
        .catch(err => {
          console.log(err);
          localStorage.removeItem('user-token');
        })
        // this.$forceUpdate()
        // this.$router.go();
        this.$goToMainPage();
      },

      logout() {
        localStorage.removeItem('user-token');
        this.token = null;
        this.$router.go();
        this.$goToMainPage();
        },

      getProfile(id){
        console.log("costam")
        let axiosConfig = {
            headers: {
            'Authorization': 'Token ' + this.token
            }
        };
        axios.get(`http://127.0.0.1:8000/api/profileUser/getProfileByUserId?id=` + id , axiosConfig)
        .then(res => this.profileData = res.data)
        .catch(err => console.log(err))
      },

    }
  }
</script>

<style scoped>
.jumbotron-special{
  background-image: url("../../static/bid_background4.jpg");
  background-size: cover;
  margin-bottom: 0.5%;

  padding-bottom: 1%;
}
.jumbotron h1{
  text-align: center;
  padding: 1%;
}
</style>
