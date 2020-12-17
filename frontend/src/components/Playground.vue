<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">

    

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

      }
    },

    mounted: function () {

    },


    methods:{

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
