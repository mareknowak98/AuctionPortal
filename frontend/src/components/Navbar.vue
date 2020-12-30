<template>
  <div>
    <div v-if="$getToken() == null">
      <b-jumbotron class="jumbotron jumbotron-special" header=" ">
        <h1> </h1>
        <h1> </h1>
        <h1> </h1>
        <h1> </h1>
      <b-navbar sticky toggleable="lg" type="dark" variant="dark">
       <b-navbar-brand v-on:click="$goToAnotherPage('/')">Home</b-navbar-brand>

       <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

       <b-collapse id="nav-collapse" is-nav>
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
         <b-navbar-brand v-on:click="$goToAnotherPage('/')">Home</b-navbar-brand>
         <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

         <b-collapse id="nav-collapse" is-nav>


          <b-navbar-nav>
          <b-nav-item-dropdown text="Buying" right>
            <b-dropdown-item v-on:click="$goToAnotherPage('/wonauctions')">Auctions I've won</b-dropdown-item>
            <b-dropdown-item v-on:click="$goToAnotherPage('/participatedauctions')">Participated auctions</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item-dropdown text="Selling" right>
            <b-dropdown-item v-on:click="$goToAnotherPage('/newauction')">Create new auction</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item v-on:click="$goToAnotherPage('/activeauctions')">Items I'm selling  </b-dropdown-item>
            <b-dropdown-item v-on:click="$goToAnotherPage('/endedauctions')">Ended auctions</b-dropdown-item>
          </b-nav-item-dropdown>

          <div v-if="is_staff == 'True'">
            <b-navbar-nav>
              <b-nav-item v-on:click="$goToAnotherPage('/staffpanel')">Admin Panel</b-nav-item>
            </b-navbar-nav>
          </div>

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
        userId: null,
        profileData: [],
        token: null,
        is_staff: '',
      }
    },
    mounted: function (){
      this.userId = this.$getUserId()
      this.getProfile()
      this.isStaff()
    },
    methods: {
      goToUserPage: function () {
        this.$goToAnotherPage('/myprofile');
      },
      login(){
        axios.post('https://auctionportalbackend.herokuapp.com/api-token-auth/',{
          username: this.username,
          password: this.password,
        })
        .then(resp => {
        this.token = resp.data.token;
        localStorage.setItem('user-token',resp.data.token)
        this.username = '';
        this.password = '';
        })
        .then(resp => {
          console.log(this.userId)
          this.getProfile()
        })
        .then(resp => {
          this.isStaff()
        })
        .catch(err => {
          console.log(err);
          localStorage.removeItem('user-token');
        })
        this.$goToMainPage();
      },

      logout() {
        localStorage.removeItem('user-token');
        this.token = null;
        this.$goToMainPage();
        this.is_staff = "False";
        },

      getProfile(){
        let axiosConfig = {
            headers: {
            'Authorization': 'Token ' + localStorage.getItem("user-token")
            }
        };
        axios.get(`https://auctionportalbackend.herokuapp.com/api/profileUser/getMyProfile`, axiosConfig)
        .then(res => this.profileData = res.data)
        .catch(err => console.log(err))
      },
      isStaff(){
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem("user-token")
          }
        };
        var userId
        axios.get(`https://auctionportalbackend.herokuapp.com/api/user-id`, axiosConfig)
            .then(res => console.log(userId = res.data[0].id))
            .then(res =>{
            axios.get(`https://auctionportalbackend.herokuapp.com/api/staff/isStaffUser?user_id=` + userId, axiosConfig)
                  .then(res => {
                    this.is_staff = res.data
                  })
                  .catch(err => console.log(err))
            })
            .catch(err => console.log(err))

      },
    }
  }
</script>

<style scoped>
.jumbotron-special{
  background-image: url("../../static/bidbackground.jpg");
  background-size: cover;
  margin-bottom: 0.5%;

  padding-bottom: 1%;
}
.jumbotron h1{
  text-align: center;
  padding: 1%;
}

</style>
