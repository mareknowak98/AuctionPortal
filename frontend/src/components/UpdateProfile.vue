<template>
  <div class="container">
  <h1 class="title"> Profile Update </h1>
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">

  <div v-if="token != null">
      <p>{{this.userId}}</p>
      <b-list-group v-for="profile in profileData" :key="profile.id">
          {{ profile }}
      <b>Your current image:</b>
      <div>
        <b-img :src= profile.profileAvatar height="180px" width="250px"></b-img>
      </div>
      <h2>-----------------------------------------</h2>
      <b-form @submit.prevent="updateProfile" >
        <b-form-group>
          <p>Choose your new avatar:</p>
          <b-form-file
            v-model="image"
            :state="Boolean(image)"
            :placeholder= profile.profileAvatar
            drop-placeholder="Drop file here..."
            type='file'
          ></b-form-file>
          <div class="mt-3">Selected file: {{ image ? image.name : '' }}</div>
        </b-form-group>

        <b-form-group id="input-group-1" label="Your name:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="name"
            :placeholder = profile.profileUserName
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-2" label="Your surname:" label-for="input-2">
          <b-form-input
            id="input-2"
            v-model="surname"
            :placeholder = profile.profileUserSurname
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-3" label="Your account number:" label-for="input-3">
          <b-form-input
            id="input-3"
            v-model="acc_num"
            :placeholder = profile.profileBankAccountNr
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-4" label="Your telephone number:" label-for="input-4">
          <b-form-input
            id="input-4"
            v-model="tel_num"
            :placeholder = profile.profileTelephoneNumber
          ></b-form-input>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>

      </b-form>
    </b-list-group>


  </div>

  <div v-else>
  <h1>Log in to edit your profile</h1>
  </div>
  </b-jumbotron>
  </div>
</template>

{% csrf_token %}
<script>
import Navbar from './Navbar.vue';
import {TokenService} from '../store/service';
import axios from 'axios';

  export default {
    name: "Profile",
    components:{
        Navbar,
    },
    computed: {

    },
    data() {
      return {
        userId: '',
        profileData: [],
        image: null,
        name: '',
        surname: '',
        acc_num: '',
        tel_num: '',
      }
    },

    mounted: function () {

        },

    methods:{
      getProfile(){

      // console.log("test: "+ this.userId)
      let axiosConfig = {
          headers: {
          'Authorization': 'Token ' + this.token
          }
      };
      axios.get(`http://127.0.0.1:8000/api/profile/`, axiosConfig)
      .then(res => this.profileData = res.data)
      .catch(err => console.log(err))
      },

      updateProfile(){
        const formData = new FormData();
        formData.append("profileUserName", this.name)
        formData.append("profileUserSurname", this.surname)
        formData.append("profileBankAccountNr", this.acc_num)
        formData.append("profileTelephoneNumber", this.tel_num)
        formData.append("profileAvatar", this.image)
        formData.append("profileNumberOfOpinions", '')
        formData.append("profileAvgOpinion", '')
        console.log(this.profileData.id)
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.token
          }
        };
        axios.put(`http://127.0.0.1:8000/api/profile/` + this.profileData[0].id + '/', formData, axiosConfig)
        .then(res => console.log(res.data))
        .catch(err => console.log(err))

        location.reload();
        },

    },
    created() {
      let token;
      this.token = TokenService.getToken();
      this.userId = this.$getUserId();
      this.getProfile();
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
