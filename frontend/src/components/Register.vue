<template>
  <div class="container">
  <navbar></navbar>

  <b-jumbotron class="jumbotron jumbotron-home">
      <div v-if="token == null">
      <b-form @submit.prevent="registerUser" @reset="onReset">
      <b-form-group id="input-group-1" label="Your Username:" label-for="input-1">
        <b-form-input
          id="input-1"
          v-model="form.username"
          required
          placeholder="Enter username"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-2"
        label="Email address:"
        label-for="input-2"
        description=""
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          required
          placeholder="Enter email"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-3" label="Password:" label-for="input-3">
        <b-form-input
          id="input-1"
          v-model="form.password1"
          type="password"
          required
          placeholder="Enter your Password"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-4" label="Confirm your password:" label-for="input-4">
        <b-form-input
          id="input-4"
          v-model="form.password2"
          type="password"
          required
          placeholder="Confirm your Password"
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">Submit</b-button>

    </b-form>

    </div>
  </b-jumbotron>
  </div>
</template>



<script>
import Navbar from './Navbar.vue'


import axios from 'axios';
  export default {
    name: "Register",
    components:{
        Navbar,
    },

    data() {
      return {
        form: {
          token: localStorage.getItem('user-token') || null,
          username: '',
          email: '',
          password1: '',
          password2: '',
        },
      }
    },

    mounted: function () {
      this.form.token = this.$getToken();
      console.log("Token to " + this.form.token);
    },


    methods:{
      registerUser(){
        //TODO make email authentiction and validation
        if (this.form.password1 == this.form.password2){
          axios.post('https://auctionportalbackend.herokuapp.com/api/users/',{
          username: this.form.username,
          email: this.form.email,
          password: this.form.password1,
          })
          .catch(err => {
          console.log(err);
          })
        }
        else{
          console.log("Passwords are not equal")
        }
        this.$goToAnotherPage('/');



      },
      onReset(evt) {
        evt.preventDefault()
        this.form.email = ''
        this.form.name = ''
        this.form.password1 = ''
        this.form.password2 = ''
      }

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
