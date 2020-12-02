<template>
  <div>
    
    <div v-if="errorFlag" style="color: red;">
      {{ error }}
    </div>

    <div class="taskbar">

      <!-- User not logged in -->
      <div v-if="token == null">

        <b-button class="mb-2 mr-sm-2 mb-sm-0" variant='primary'>
          Home
        </b-button>

        <b-button class="mb-2 mr-sm-2 mb-sm-0" variant='primary' v-b-modal.loginModal>
          Log in
        </b-button>

        <b-button class="mb-2 mr-sm-2 mb-sm-0" variant='primary' v-on:click="$goToAnotherPage('/register')">
          Register
        </b-button>

        <!-- Login form in a modal -->
          <b-modal id="loginModal" title="Log in" @ok="login" ok-title="Log in">
            <label class="mb-2">Please enter your username, then your password, and press Log in.</label>
            <b-form-input class="mb-2" placeholder="Username" v-model="username"></b-form-input>
            <!-- <b-form-input class="mb-2" placeholder="Email" v-model="email" autocomplete="email"></b-form-input> -->
            <b-form-input class="mb-2" placeholder="Password" v-model="password" type="password"></b-form-input>
          </b-modal>

      </div>

      <!-- User logged in -->
      <div v-else>

        <b-button class="mb-2 mr-sm-2 mb-sm-0" variant='primary' v-on:click="$goToAnotherPage('/')">
          Home
        </b-button>

        <b-button class="mb-2 mr-sm-2 mb-sm-0" variant='primary' v-on:click="goToUserPage()">
          Me
        </b-button>

        <b-dropdown class="mb-2 mr-sm-2 mb-sm-0" variant='primary' id="buyingDropdown" text="Buying">
          <!-- <b-dropdown-item v-on:click="$goToAnotherPage('/won')">Auctions I've won</b-dropdown-item> -->
          <!-- <b-dropdown-item v-on:click="$goToAnotherPage('/bidding_on')">Auctions I'm bidding on</b-dropdown-item> -->
        </b-dropdown>

        <b-dropdown class="mb-2 mr-sm-2 mb-sm-0" variant='primary' id="sellingDropdown" text="Selling">
          <b-dropdown-item v-on:click="$goToAnotherPage('/newauction')">Create an auction</b-dropdown-item>
          <!-- <b-dropdown-item v-on:click="$goToAnotherPage('/current')">Items I'm selling</b-dropdown-item> -->
          <!-- <b-dropdown-item v-on:click="$goToAnotherPage('/sold')">Items I've sold</b-dropdown-item> -->
          <!-- <b-dropdown-item v-on:click="$goToAnotherPage('/unsold')">Unsold items</b-dropdown-item> -->
        </b-dropdown>

        <b-button class="mb-2 mr-sm-2 mb-sm-0" variant='primary' v-on:click="logout()">
          Log out
        </b-button>

      </div>

    </div>
    <div class="container">
      <header class="site-header">
      <b-navbar toggleable="lg" type="dark" variant="info">
        <b-navbar-brand href="">NavBar</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <!-- <b-nav-item href="#">Link</b-nav-item>
            <b-nav-item href="#" disabled>Disabled</b-nav-item> -->
          </b-navbar-nav>

          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-nav-form>
              <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
              <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
            </b-nav-form>

            <b-nav-item-dropdown text="Lang" right>
              <!-- <b-dropdown-item href="#">EN</b-dropdown-item>
              <b-dropdown-item href="#">ES</b-dropdown-item>
              <b-dropdown-item href="#">RU</b-dropdown-item>
              <b-dropdown-item href="#">FA</b-dropdown-item> -->
            </b-nav-item-dropdown>

            <b-nav-item-dropdown right>
              <!-- Using 'button-content' slot -->
              <template #button-content>
                <em>User</em>
              </template>
              <!-- <b-dropdown-item href="#">Profile</b-dropdown-item> -->
              <!-- <b-dropdown-item href="#">Sign Out</b-dropdown-item> -->
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
      </header>
      <main role="main" class="container">

      </main>
     
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
        token: localStorage.getItem('user-token') || null,
      }
    },
    methods: {
      login(){
        axios.post('http://127.0.0.1:8000/api-token-auth/',{
          username: this.username,
          password: this.password,
        })
        .then(resp => {
        this.token = resp.data.token;
        // console.log(this.token) #dont want to 
        localStorage.setItem('user-token',resp.data.token)
        })
        .catch(err => {
          console.log(err);
          localStorage.removeItem('user-token');
        })
      },

    logout() {
      localStorage.removeItem('user-token');
      this.token = null;
      }
    }
  }
</script>

<style scoped>

</style>