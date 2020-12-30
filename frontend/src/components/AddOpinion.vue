<template>
  <div class="container">
  <navbar></navbar>

  <b-jumbotron class="jumbotron jumbotron-home">
    <b-container class="bv-example-row">
      <b-row class="justify-content-md-center">
        <b-col col lg="8">
          <h1>Add opinion about user: <strong>{{this.user_about}}</strong></h1>
          <b-form-textarea
            id="textarea"
            v-model="opinion_content"
            placeholder="Enter opinion..."
            rows="3"
            max-rows="6"
          ></b-form-textarea>
          <b-form-rating v-model="opinion_stars" variant="warning" class="mb-2"></b-form-rating>
          <b-button block type="submit" variant="secondary" v-on:click="addOpinion">Submit</b-button>

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
    name: "AddOpinion",
    components:{
        Navbar,
        Footer,
    },

    data() {
      return {
        opinion_stars: '',
        opinion_content: '',
        user_about: ''
      }
    },

    mounted: function () {
      this.user_about = this.$route.params.userId;
      this.getUsername();
    },


    methods:{
      getUsername(){
        var username;
        axios.get("https://auctionportalbackend.herokuapp.com/api/users/getUsernameById?id=" + this.$route.params.userId)
          .then(res => this.user_about = res.data)
          .catch(err => console.log(err));
        return this.username;
      },
      addOpinion(){
        const formData = new FormData();
        formData.append("opinionStars", this.opinion_stars)
        formData.append("opinionDescription", this.opinion_content)
        formData.append("opinionUserAbout", this.$route.params.userId)
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.$getToken()
          }
        };
        axios.post(`https://auctionportalbackend.herokuapp.com/api/opinion/`, formData, axiosConfig)
        .then(res => console.log(res.data))
        .catch(err => console.log(err))
        this.$sleep(500);
        this.$router.back();
      },
    },


  }
</script>

<style scoped>
@media (min-width: 100px) {
    .container{
        max-width: 1400px;
    }
}
</style>
