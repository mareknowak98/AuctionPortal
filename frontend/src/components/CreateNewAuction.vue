<template>
  <div class = jumbotron>
  <h1 class="title"> New Auction </h1>
  <navbar></navbar>
  <b-jumbotron>
    <div v-if="token != null">
      <h1>Add an auciton</h1>
      <!-- <b-form @submit.prevent="registerUser" @reset="onReset">
        
        <b-form-select v-model="selectedCategory" class="mb-2 mr-sm-2 mb-sm-0">
          <option disabled selected hidden value="">Category</option>
          <option value="">all</option>
          <option v-bind:key='category.id' v-for="category in categories">
            {{ category.category_name }}
          </option>
        </b-form-select>

      </b-form>   -->

    </div>
    <div v-else>
      <h1>Log in to add auction</h1>
    </div>
  </b-jumbotron>
  </div>
</template>



<script>
import Navbar from './Navbar.vue'


import axios from 'axios';
  export default {
    name: "NewAuction",
    components:{
        Navbar,
    },

    data() {
      return{
        categories: [],
        image: '',
        product_name: '',
        description: '',
        is_new: '',
        date_started: '',
        date_end: '',
        starting_price: '',
        minimal_price: '',
        is_shipping_av: '',
        token: localStorage.getItem('user-token') || null,
      }
    },
    // mounted: function () {
    //   this.token = this.$getToken();
    //   this.$getCategories2();
    //   console.log("Token to " + this.form.token);
    // },
    methods:{
      getCategories2(){
        axios.get('http://127.0.0.1:8000/api/categories')
            .then(resp => {
                this.categories = resp.data;
            })
            .catch(err => {
                console.log(err);
            })
      }
    }

  }
</script>

<style scoped>

</style>