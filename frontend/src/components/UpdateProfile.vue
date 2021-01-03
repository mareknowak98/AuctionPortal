<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">
    <b-container class="bv-example-row">
      <b-row class="justify-content-md-center">
        <b-col col lg="8">
        <div v-if="$getToken() != null">
            <b-list-group v-for="profile in profileData" :key="profile.id">
            <h2>{{profile.profileUser.username}}</h2>
            <b>Your current avatar:</b>
            <b-row class="justify-content-md-center">
            <div class="imagecontainer">
              <enlargeable-image :src=profile.profileAvatar :src_large=profile.profileAvatar  />
            </div>
            </b-row>

            <b-form @submit.prevent="updateProfile" >
              <b-form-group>
                <p>Choose your new avatar:</p>
                <b-form-file
                  v-model="image"
                  drop-placeholder="Drop file here..."
                  type='file'
                ></b-form-file>
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

              <b-form-group id="input-group-4" label="Your telephone number:" label-for="input-4">
                <b-form-input
                  id="input-4"
                  v-model="tel_num"
                  :placeholder = profile.profileTelephoneNumber
                ></b-form-input>
              </b-form-group>

              <b-button type="submit" block variant="secondary">Update</b-button>


      </b-form>
    </b-list-group>


  </div>

  <div v-else>
  <h1>Log in to edit your profile</h1>
  </div>

  </b-col>
  </b-row>
  <Footer></Footer>
  </b-container>
  </b-jumbotron>
  </div>
</template>

{% csrf_token %}
<script>
import Navbar from './Navbar.vue';
import {TokenService} from '../store/service';
import Footer from './Footer.vue'
import axios from 'axios';

  export default {
    name: "Profile",
    components:{
        Navbar,
        Footer,
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
        tel_num: '',
      }
    },

    mounted: function () {
          let recaptchaScript = document.createElement('script')
          recaptchaScript.async = true
          recaptchaScript.setAttribute('src', 'https://unpkg.com/@diracleo/vue-enlargeable-image/dist/vue-enlargeable-image.min.js')
          document.head.appendChild(recaptchaScript)
        },

    methods:{
      getProfile(){
      let axiosConfig = {
          headers: {
          'Authorization': 'Token ' + this.$getToken()
          }
      };
      axios.get(`https://auctionportalbackend.herokuapp.com/api/profile/`, axiosConfig)
      .then(res => this.profileData = res.data)
      .catch(err => console.log(err))
      },

      updateProfile(){
        const formData = new FormData();
        formData.append("profileUserName", this.name)
        formData.append("profileUserSurname", this.surname)
        formData.append("profileTelephoneNumber", this.tel_num)
        formData.append("profileAvatar", this.image)
        formData.append("profileNumberOfOpinions", '')
        formData.append("profileAvgOpinion", '')
        console.log(this.profileData.id)
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.$getToken()
          }
        };
        axios.put(`https://auctionportalbackend.herokuapp.com/api/profile/` + this.profileData[0].id + '/', formData, axiosConfig)
        .then(res => console.log(res.data))
        .then(res =>{
          this.getProfile()
        })
        .catch(err => console.log(err))

        
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


@media (min-width: 100px) {
    .imagecontainer{
        max-width: 200px;
    }
}
.enlargeable-image .enlargeable-image-slot {
  display:inline-block;
}
.enlargeable-image .enlargeable-image-slot > img {
  max-width:100%;
}
.enlargeable-image > .enlargeable-image-slot {
  max-width:100%;
  max-height:100%;
  cursor:zoom-in;
}
.enlargeable-image > .enlargeable-image-slot.active {
  opacity:0.3;
  filter:grayscale(100%);
}
.enlargeable-image .enlargeable-image-full {
  cursor:zoom-out;
  background-color:transparent;
  align-items:center;
  justify-content:center;
  background-position: center center;
  background-repeat:no-repeat;
  background-size:contain;
  z-index:2000;
  display:none;
}
.enlargeable-image .enlargeable-image-full > img {
  object-fit:contain;
  width:100%;
  height:100%;
}
.enlargeable-image .enlargeable-image-full.enlarging {
  display:flex;
  position:fixed;
  left:0px;
  top:0px;
  width:100%;
  height:100%;
  background-color:transparent;
  cursor:zoom-out;
}
.enlargeable-image .enlargeable-image-full.delarging {
  display:flex;
  position:fixed;
  left:0px;
  top:0px;
  width:100%;
  height:100%;
  background-color:transparent;
  cursor:zoom-in;
}
.enlargeable-image .enlargeable-image-full.enlarged {
  display:flex;
}

</style>
