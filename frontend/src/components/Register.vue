<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">
      <b-container class="bv-example-row">
        <b-row class="justify-content-md-center">
          <b-col col lg="8">
            <b-alert
            variant="danger"
            dismissible
            fade
            :show="showPasswordAlert"
            @dismissed="showPasswordAlert=false"
          >
            Passwords are not equal.
          </b-alert>

            <div v-if="token == null">
            <h1>Register:</h1>
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

          <div>
              <b-form-checkbox-group
                v-model="form.confirm_rules"
                :options="options"
                :state="state"
                name="checkbox-validation"
                unchecked-value=false

              ><b-link v-b-modal.RegisterModal>Link</b-link>
              <b-form-invalid-feedback :state="state">Confirm to register</b-form-invalid-feedback>
              <b-form-valid-feedback :state="state">Thank you</b-form-valid-feedback>
              </b-form-checkbox-group>
          </div>

          <p></p>

          <b-button block type="submit" v-on:click="registerUser()" variant="secondary">Submit</b-button>
          </b-form>

    </div>
    <b-modal id="RegisterModal" size="lg" title="Large Modal">
      Here bedzie regulamin
      <h2></h2>
      <h2></h2>
      <h2></h2>
      <h2></h2>
      <h2></h2>
      <h2></h2>
      <h2></h2>
    </b-modal>

    </b-col>
    </b-row>
    </b-container>
    <Footer></Footer>
  </b-jumbotron>
  </div>
</template>



<script>
import Navbar from './Navbar.vue'
import Footer from './Footer.vue'


import axios from 'axios';
  export default {
    name: "Register",
    components:{
        Navbar,
        Footer,
    },
  

    data() {
      return {
        options: [
          { text: 'I have read the terms and conditions of membership and agree with the content.', value: true},
        ],
        form: {
          token: localStorage.getItem('user-token') || null,
          confirm_rules: false,
          username: '',
          email: '',
          password1: '',
          password2: '',
        },
      }
    },

    mounted: function () {
      this.form.token = this.$getToken();
    },

    computed: {
      state() {
        let res;
        if (this.form.confirm_rules == true)
          return true;
        if (this.form.confirm_rules.length >= 1)
          return true;
        else
          return false;
      },
    },

    methods:{
      uncheck(){
        console.log("es")
        this.form.confirm_rules = !this.form.confirm_rules
      },
      registerUser(){
        if (this.form.password1 == this.form.password2){
          axios.post('https://auctionportalbackend.herokuapp.com/api/users/',{
          username: this.form.username,
          email: this.form.email,
          password: this.form.password1,
          })
          .then(res =>{
            this.$goToAnotherPage('/');
          })
          .catch(err => {
          console.log(err);
          })
        }
        if (this.form.password1 != this.form.password2 && this.form.username.length != 0 && this.form.email.length != 0  ){
          this.showPasswordAlert = true;
          this.form.password1 = '';
          this.form.password2 = '';
        }



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
