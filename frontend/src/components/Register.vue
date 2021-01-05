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

          <b-alert
            variant="danger"
            dismissible
            fade
            :show="showRegulationAlert"
            @dismissed="showRegulationAlert=false"
          >
            You must accept Regulations
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
    <b-modal id="RegisterModal" size="lg" title="Regulations of the auction portal">
      <td id="mytext" v-html="regulations"></td>
    
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
        regulations: "<p><strong>Regulations of the auction portal</strong></p><p><strong>This document specifies the terms of using the auction portal.</strong></p><p><strong>1.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;General Provision</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The auction site is a communication platform for concluding commercial transactions between users.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Using the auction portal is free.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auctions enable the presentation of goods offered by the seller.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Bidding on the highest amount does not require a commercial transaction, but only allows contact between the seller and the buyer.</p><p>&nbsp;</p><p><strong>2.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Registration</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Users of the auction site may be natural persons over 18 years of age.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To register a user, the following are required: login / user name, e-mail address and accept these regulations.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After logging in, the user is able to add their own auctions and bidding.</p><p>&nbsp;</p><p><strong>3.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Personal data protection</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;By registering, the user consents to the processing of his personal data for the purposes related solely to the functioning of the auction site.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Access to personal data and their change is possible by editing the user's own account.</p><p>&nbsp;</p><p><strong>4.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Offers</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The items listed on the auction portal should be free from physical and legal defects, or these defects should be described by the seller.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The presented photos may not contain pornographic materials or materials considered offensive.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The description of items should be prepared in a truthful manner, without using profanity.</p><p>&nbsp;</p><p><strong>5.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auction</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It is allowed to participate in auctions using only one account.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It is unacceptable to bid on your own auctions.</p><p><br></p><p><strong>6.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Comments</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The use of profanity, slander, in the comments is prohibited.</p><p><br></p><p><strong>7.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Final Provisions</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Failure to comply with the regulations may result in the removal of the auction or the user of the auction portal by its administrator.</p>",
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
      getState() {
        let res;
        if (this.form.confirm_rules == true)
          return true;
        if (this.form.confirm_rules.length >= 1)
          return true;
        else
          return false;
      },
      registerUser(){
        if(!this.getState()){
          this.showRegulationAlert = true;
          console.log("err")
          this.form.password1 = '';
          this.form.password2 = '';
          return;
        }

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
