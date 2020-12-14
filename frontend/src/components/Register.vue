<template>
  <div class="container">
  <h1 class="title"> Register </h1>
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
        description="We'll use this email to activate your account"
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
    <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card>
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
          axios.post('http://127.0.0.1:8000/api/users/',{
          username: this.form.username,
          email: this.form.email,
          password: this.form.password1,
          })
          .then(resp => {
            console.log(resp);
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

      //TODELETE
      onSubmit(evt) {
        evt.preventDefault()
        alert(JSON.stringify(this.form))
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
