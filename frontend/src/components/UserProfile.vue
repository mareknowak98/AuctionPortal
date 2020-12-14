<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">

  <div v-if="token != null">
    <b-list-group v-for="profile in profileData" :key="profile.id">
    </b-list-group>

  <b-card>
    <b-media>
      <template #aside>
        <table>
          <tr>
            <b-img :src="profileData.profileAvatar" fluid width="144" alt="placeholder"></b-img>
          </tr>
          <tr><p></p></tr>
          <tr>
              <b-button block variant="secondary" v-on:click="$goToAnotherPage('/message/' + profileData.profileUser.id + '/')">Write message</b-button>
          </tr>
          <tr><p></p></tr>
          <tr>
              <b-button block variant="secondary" v-on:click="$goToAnotherPage('/message/' + profileData.profileUser.id + '/')">Add opinion</b-button>
          </tr>
        </table>
      </template>

      <h5 class="mt-0">{{profileData.profileUser.username}}</h5>
      <p>
        Registered since: {{this.getRegistrationDate()}}
      </p>
      <p>
        {{this.getUserProfileRating()}}

           <b-form-rating
            id="rating-inline"
            inline value="4"
             variant="warning"
             v-model="rating"
             readonly
             show-value
             show-value-max
             precision="2"
           ></b-form-rating>
      </p>
      <table>
        <tr>
          <b-list-group v-for="opinion in opinions" :key="opinion.id">
            <td>
              <b-media>
                <template #aside>
                <div v-if="opinion.opinionStars == 1">
                    <b-img :src="require('../../static/smile1.png')" width="64" alt="placeholder"></b-img>
                </div>
                <div v-if="opinion.opinionStars == 2">
                    <b-img :src="require('../../static/smile2.png')" width="64" alt="placeholder"></b-img>
                </div>
                <div v-if="opinion.opinionStars == 3">
                    <b-img :src="require('../../static/smile3.png')" width="64" alt="placeholder"></b-img>
                </div>
                <div v-if="opinion.opinionStars == 4">
                    <b-img :src="require('../../static/smile4.png')" width="64" alt="placeholder"></b-img>
                </div>
                <div v-if="opinion.opinionStars == 5">
                    <b-img :src="require('../../static/smile5.png')" width="64" alt="placeholder"></b-img>
                </div>
              </template>
                  <h5 class="mt-0">{{opinion.opinionUserAuthor.username}}</h5>
                  <p class="mb-0">
                      {{opinion.opinionDescription}}
                  </p>
                  <b-form-rating
                  id="rating-inline"
                  inline value="4"
                  variant="warning"
                  v-model="opinion.opinionStars"
                  ></b-form-rating>


              </b-media>
            </td>
          </b-list-group>

        </tr>
      </table>



    </b-media>
  </b-card>

  </div>




  <div v-else>
  <h1>Log in to see other's profiles</h1>
  </div>
  <Footer></Footer>
  </b-jumbotron>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import {TokenService} from '../store/service';
import axios from 'axios';
import Footer from './Footer.vue'
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
        profileId: '',
        rating: '',
        opinions: [],
        images: [],
      }
    },

    mounted: function () {
          this.profileId = this.$route.params.profileId;
          this.getProfile(this.profileId)
          this.getUserOpinions()
        },


    methods:{
      getProfile(id){
        console.log(12345)
        let axiosConfig = {
            headers: {
            'Authorization': 'Token ' + localStorage.getItem("user-token")
            }
        };
        axios.get(`http://127.0.0.1:8000/api/profileUser/` + parseInt(id) + '/', axiosConfig)
        .then(res => this.profileData = res.data)
        .catch(err => console.log(err))
        // this.getUserOpinions();
      },

      getRegistrationDate(){
        var date = new Date(this.profileData.profileUser.date_joined)
        date = date.toISOString().split('T')[0]
        return date;
      },

      getUserProfileRating(){
        let axiosConfig = {
            headers: {
            'Authorization': 'Token ' + localStorage.getItem("user-token")
            }
        };
        var tmp
        axios.get(`http://127.0.0.1:8000/api/profile/getUserIdByProfile?profile_id=` + this.$route.params.profileId + '/', axiosConfig)
        .then(res => this.tmp = res.data)
        .catch(err => console.log(err))
        console.log(tmp)


        axios.get(`http://127.0.0.1:8000/api/opinion/getUserAvgRating?user_id=` + this.profileData.profileUser.id, axiosConfig)
            .then(res => console.log(this.rating = res.data))
            .catch(err => console.log(err))
      },

      getUserOpinions(){
          let axiosConfig = {
              headers: {
              'Authorization': 'Token ' + localStorage.getItem("user-token")
              }
          };
          var tmp
          axios.get(`http://127.0.0.1:8000/api/profile/getUserIdByProfile?profile_id=` + this.$route.params.profileId , axiosConfig)
          .then(res => this.tmp = res.data)
          .then(res =>{
            console.log("tmp " + this.tmp)
            axios.get(`http://127.0.0.1:8000/api/opinion/getUserOpinions?user_id=` + this.tmp, axiosConfig)
                .then(res => console.log(this.opinions = res.data))
                .catch(err => console.log(err))
          })
          .catch(err => console.log(err))
          console.log(tmp)

      },

    },
    created() {
      let token;
      this.token = TokenService.getToken();
      this.userId = this.$getUserId();
      this.getProfile();
    },
  }
</script>

<style scoped>
@media (min-width: 100px) {
    .container{
        max-width: 1400px;
    }
}
.b-media{
  padding: 5%;
}
td{
  padding: 1%;
}

</style>
