<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">
    <div v-if="token != null">
      <h1>Add an auciton</h1>

      <b-form @submit.prevent="createAuction" >


        <b-form-group>
        <p>Choose image</p>
        <b-form-file
          v-model="image"
          :state="Boolean(image)"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."
          type='file'
        ></b-form-file>
        <div class="mt-3">Selected file: {{ image ? image.name : '' }}</div>
        </b-form-group>

        <label class="mr-2">Category:&nbsp;</label>
        <b-form-group
        required
        >
          <b-form-select inline v-model="selectedCategory">
            <option v-for="category in categories" v-bind:key="category.id" v-bind:value="category.id">
              {{ category.category_name }}
            </option>
          </b-form-select>
        </b-form-group>

        <b-form-group id="input-group-1" label="Name of auction:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="product_name"
            required
            placeholder="Enter auction name"
          ></b-form-input>
        </b-form-group>

        <p>Auction Description</p>
        <b-form-textarea
          required
          id="description"
          v-model="text"
          placeholder="..."
          rows="3"
          max-rows="6"
        ></b-form-textarea>
        <pre class="mt-3 mb-0">{{ text }}</pre>

        <b-form-group id="radio1" label="Is this item new?"
          required
        >
          <b-form-radio-group id="radio-group-1" v-model="is_new" name="radio-sub-component1">
            <b-form-radio :value="true">New</b-form-radio>
            <b-form-radio :value="false">Used</b-form-radio>
          </b-form-radio-group>
        </b-form-group>

        <label for="datepicker-full-width">Choose a date</label>
        <b-form-datepicker
          required
          id="datepicker-full-width"
          v-model="date_end"
          menu-class="w-100"
          calendar-width="100%"
          class="mb-2"
        ></b-form-datepicker>
        <p>Value: '{{ date_end }}'</p>

        <b-form-timepicker
        required
        v-model="date_end_hr" locale="en"></b-form-timepicker>
        <div class="mt-2">Value: '{{ date_end_hr }}'</div>

        <b-form-group id="input-group-1" label="Enter starting price" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="starting_price"
            required
            placeholder="..."
          ></b-form-input>
        </b-form-group>

        <b-form-group id="input-group-1" label="Enter minimal price" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="minimal_price"
            placeholder="..."
          ></b-form-input>
        </b-form-group>

        <b-form-group id="radio2" label="Is shipping available?"
          required
        >
          <b-form-radio-group id="radio-group-2" v-model="is_shipping_av" name="radio-sub-component2">
            <b-form-radio :value="true">Yes</b-form-radio>
            <b-form-radio :value="false">No</b-form-radio>
          </b-form-radio-group>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>

        </b-form>

    </div>
    <div v-else>
      <h1>Log in to add auction</h1>
    </div>

    <p>{{$data}}</p>


  </b-jumbotron>
  </div>
</template>


{% csrf_token %}
<script>
import Navbar from './Navbar.vue'

import {TokenService} from '../store/service'

import axios from 'axios';
  export default {
    name: "NewAuction",
    components:{
        Navbar,
    },

    data() {
      return{
        product_name: '',
        categories: [],
        selectedCategory: '',
        image: null,
        description: '',
        is_new: null,
        date_end: '',
        date_end_hr: '',
        starting_price: '',
        minimal_price: '',
        is_shipping_av: null,
        token: localStorage.getItem('user-token') || null,

        debugtext1: '',
        debugtext2: '',

      }
    },
    mounted: function () {
      this.token = TokenService.getToken();
      this.categories = this.getCategories();
      console.log("Token to " + this.form.token);
    },
    methods:{
      getCategories(){
        axios.get("http://127.0.0.1:8000/api/categories/")
          .then(res => {
          this.categories = res.data
          console.log(this.data)
          })
          .catch(err => console.log(err));
      },

      createAuction(){
        var fulldate_end = "" + this.date_end + "T" + this.date_end_hr + "Z"
        this.debugtext1 = fulldate_end

        // getting current date
        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();


        var fulldate_start = yyyy + "-" + mm + "-" + dd + "T" + today.getHours() + ":"
          + today.getMinutes() + ":" + today.getSeconds() + "Z";

        this.debugtext2 = fulldate_start

        console.log('Date string is ' + fulldate_end)

      this.token = TokenService.getToken();
      const formData = new FormData();

      formData.append("image", this.image)
      formData.append("product_name", this.product_name)
      formData.append("description", this.description)
      formData.append("is_new", this.is_new)
      formData.append("category", this.selectedCategory)
      formData.append("date_started", fulldate_start)
      formData.append("date_end", fulldate_end)
      formData.append("starting_price", this.starting_price)
      formData.append("minimal_price", this.minimal_price)
      formData.append("is_shipping_av", this.is_shipping_av)

      let axiosConfig = {
        headers: {
          'Authorization': 'Token ' + this.token
        }
      };
      axios.post(`http://127.0.0.1:8000/api/auctioncreate/`, formData,axiosConfig)
      .then(res => console.log(res.data))
      .catch(err => console.log(err))
      },
    },
    created() {
      let token;
      this.token = TokenService.getToken();
    }

  }
</script>

<style scoped>
@import '../styles/style.css';

@media (min-width: 100px) {
    .container{
        max-width: 1400px;
    }
}
.jumbotron-home{
    margin: 0%;
    padding: 1%;
    padding-left:0.5%;
    padding-right:0.5%;

}

</style>
