<template>
  <div class = jumbotron>
  <h1 class="title"> New Auction </h1>
  <navbar></navbar>
  <b-jumbotron>
    <div v-if="token != null">
      <h1>Add an auciton</h1>

      <b-form @submit.prevent="" >


        <b-form-group>
        <p>Choose image</p>
        <b-form-file
          v-model="image"
          :state="Boolean(file1)"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."
        ></b-form-file>
        <div class="mt-3">Selected file: {{ image ? image.name : '' }}</div>
        </b-form-group>

        <label class="mr-2">Category:&nbsp;</label>
        <b-form-group
        required
        >
          <b-form-select inline v-model="selectedCategory"><!-- :state="categoryState"-->
            <option v-for="category in categories" v-bind:key="category.id">
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

        <b-form-group label="Is this item new?"
          required
        >
          <b-form-radio-group id="radio-group-2" v-model="is_new" name="radio-sub-component">
            <b-form-radio :value="{ first: 1 }">New</b-form-radio>
            <b-form-radio :value="{ second: 0 }">Used</b-form-radio>
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
            required
            placeholder="..."
          ></b-form-input>
        </b-form-group>

        <b-form-group label="Is shipping available?"
          required
        >
          <b-form-radio-group id="radio-group-2" v-model="is_shipping_av" name="radio-sub-component">
            <b-form-radio :value="{ first: 1 }">Yes</b-form-radio>
            <b-form-radio :value="{ second: 0 }">No</b-form-radio>
          </b-form-radio-group>
        </b-form-group>

        </b-form>

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
        product_name: '',
        categories: [],
        image: null,
        description: '',
        is_new: null,
        // date_started: '',
        date_end: '',
        date_end_hr: '',
        starting_price: '',
        minimal_price: '',
        is_shipping_av: null,
        token: localStorage.getItem('user-token') || null,
      }
    },
    mounted: function () {
      // this.token = this.$getToken();
      this.categories = this.getCategories();
      console.log("Token to " + this.form.token);
    },
    methods:{
      getCategories(){
        axios.get("http://127.0.0.1:8000/api/categories/")
          .then(res => {
          this.categories = res.data
          console.log("essa")
          console.log(this.data)
          })
          .catch(err => console.log(err));
      },
    }

  }
</script>

<style scoped>

</style>