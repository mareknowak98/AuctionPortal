<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">
    <div v-if="token != null">
      <h1 id="myh1">Add an auction</h1>

      <b-form @submit.prevent="createAuction" >
        <b-container class="bv-example-row">
          <b-row class="justify-content-md-center">
            <b-col col lg="8">


        <b-form-group>
        <p>Choose image</p>
        <b-form-file
          v-model="auctionImage"

          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."
          type='file'
        ></b-form-file>
        </b-form-group>

        <b-form-group id="input-group-1" label="Name of auction:" label-for="input-1">
          <b-form-input
            id="input-1"
            v-model="auctionProductName"
            required
            placeholder="Enter auction name"
          ></b-form-input>
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


        <p>Auction Description</p>
        <div id="textinput">
          <vue-editor v-model="auctionDescription" :editorToolbar="customToolbar"></vue-editor>
        </div>

        <p> </p>
        <b-form-group label="Condition:">
          <b-form-radio-group v-model="auctionIsNew" :options="options" :state="state" name="radio-validation">
            <b-form-invalid-feedback :state="state">Please select one</b-form-invalid-feedback>
            <b-form-valid-feedback :state="state"></b-form-valid-feedback>
          </b-form-radio-group>
        </b-form-group>

      <p>Enter end date:</p>
      <b-row>
        <b-col cols="6" >
          <b-form-datepicker
            required
            id="datepicker-full-width"
            v-model="auctionDateEnd "
            menu-class="w-100"
            calendar-width="100%"
            class="mb-2"
          ></b-form-datepicker>
        </b-col>
          <b-col cols="5" ><vue-timepicker required v-model="date_end_hr"></vue-timepicker>
        </b-col>
    </b-row>

    <b-row>
      <b-col cols="6" >
    <div role="group">
        <label for="input-live">Enter starting price: </label>
        <b-form-input
        id="input-live"
        v-model="auctionStartingPrice "
        :state="priceState"
        aria-describedby="input-live-help input-live-feedback"
        placeholder="..."
        trim
        ></b-form-input>
        <b-form-invalid-feedback id="input-live-feedback">
        Enter a numeric value
        </b-form-invalid-feedback>
    </div>
      </b-col>
      <b-col cols="6" >
    <div role="group">
        <label for="input-live">Enter minimal price:</label>
        <b-form-input
        id="input-live"
        v-model="auctionMinimalPrice "
        :state="minPrizeState"
        aria-describedby="input-live-help input-live-feedback"
        placeholder="..."
        trim
        ></b-form-input>
        <b-form-invalid-feedback id="input-live-feedback">
        Enter a numeric value
        </b-form-invalid-feedback>
    </div>
    </b-col>
  </b-row>
  <div>
    <p>   </p>
    <b-form-group label="Is shipping available">
      <b-form-radio-group v-model="auctionIsShippingAv " :options="options2" :state="state2" name="radio-validation">
        <b-form-invalid-feedback :state="state2">Please select one</b-form-invalid-feedback>
        <b-form-valid-feedback :state="state2"></b-form-valid-feedback>
      </b-form-radio-group>
    </b-form-group>
    <b-row>
    <b-col cols="6" >

    <div v-if="auctionIsShippingAv  == 'true'">
      <div role="group">
          <label for="input-live">Enter shipping costs: </label>
          <b-form-input
          id="input-live"
          v-model="shipping_cost"
          :state="shippingState"
          aria-describedby="input-live-help input-live-feedback"
          placeholder="..."
          trim
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback">
          Enter a numeric value
          </b-form-invalid-feedback>
      </div>
    </div>
    </b-col>
    <b-col cols="6" >
    </b-col>
    </b-row>

    </div>


    <p>         </p>


      <b-button type="submit" variant="secondary">Submit</b-button>
    </b-col>
   </b-row>
   </b-container>
      </b-form>


      </div>
      <div v-else>
        <h1>Log in to add auction</h1>
      </div>



    <!-- <p>{{$data}}</p> -->
    <Footer></Footer>

  </b-jumbotron>
  </div>
</template>


<script>
import Navbar from './Navbar.vue'
import VueTimepicker from 'vue2-timepicker'
import Footer from './Footer.vue'
import {TokenService} from '../store/service'
import { VueEditor } from "vue2-editor";
import '../styles/style.css';


import axios from 'axios';
  export default {
    name: "NewAuction",
    components:{
        Navbar,
        VueEditor,
        VueTimepicker,
        Footer,
    },

    data() {
      return{
        content: "",
        shipping_cost: "",
        customToolbar: [["bold", "italic", "underline"], [{ list: "ordered" }, { list: "bullet" }]],
        value: null,
        options: [
          { text: 'New', value: 'true' },
          { text: 'Used', value: 'false' },
        ],
        options2: [
          { text: 'Yes', value: 'true' },
          { text: 'No', value: 'false' },
        ],
        date: null,
        auctionProductName: '',
        categories: [],
        selectedCategory: '',
        auctionImage: null,
        auctionDescription: '',
        auctionIsNew: null,
        auctionDateEnd : '',
        date_end_hr: '00:00',
        auctionStartingPrice : '',
        auctionMinimalPrice : '',
        auctionIsShippingAv : null,
        is_visable: this.auctionIsShippingAv ,
        token: localStorage.getItem('user-token') || null,

        debugtext1: '',
        debugtext2: '',

      }
    },

    computed: {
      state() {
        return Boolean(this.auctionIsNew)
      },
      state2() {
        return Boolean(this.auctionIsShippingAv )
      },
      priceState() {
        if (this.auctionStartingPrice  == "")
          return "isnull"
        return this.isNumeric(this.auctionStartingPrice ) ? true : false
      },
      minPrizeState() {
        if (this.auctionMinimalPrice  == "")
          return "isnull"
        return this.isNumeric(this.auctionMinimalPrice ) ? true : false
      },
      shippingState() {
        if (this.shipping_cost == "")
          return "isnull"
        return this.isNumeric(this.shipping_cost) ? true : false
      },
    },


    mounted: function () {
      this.token = TokenService.getToken();
      this.categories = this.getCategories();
      console.log("Token to " + this.form.token);


    },
    methods:{
      getVisability(){
        console.log("es")
        if (this.auctionIsShippingAv  == null){
          return 0;
        }
        if (this.auctionIsShippingAv  == true){
          this.is_visable = "true"
        }
        else{
          this.is_visable = "false"
        }
      },
      isNumeric(str) {
          if (typeof str != "string") return false
          return !isNaN(str) && !isNaN(parseFloat(str))
      },
      getCategories(){
        axios.get("https://auctionportalbackend.herokuapp.com/api/categories/")
          .then(res => {
          this.categories = res.data
          })
          .catch(err => console.log(err));
      },

      createAuction(){
        var fulldate_end = "" + this.auctionDateEnd  + "T" + this.date_end_hr + "Z"
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

        formData.append("auctionImage", this.auctionImage)
        formData.append("auctionProductName", this.auctionProductName)
        formData.append("auctionDescription", this.auctionDescription)
        formData.append("auctionIsNew", this.auctionIsNew)
        formData.append("auctionCategory", this.selectedCategory)
        formData.append("auctionDateStarted ", fulldate_start)
        formData.append("auctionDateEnd ", fulldate_end)
        formData.append("auctionStartingPrice ", this.auctionStartingPrice )
        formData.append("auctionMinimalPrice ", this.auctionMinimalPrice )
        formData.append("auctionIsShippingAv ", this.auctionIsShippingAv )
        formData.append("auctionShippingCost", this.sshipping_cost)

        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.token
          }
        };
        axios.post(`https://auctionportalbackend.herokuapp.com/api/auctioncreate/`, formData,axiosConfig)
        .then(res => console.log(res.data))
        .catch(err => console.log(err))

        this.$sleep(500); //TODO check it
        this.$router.back();
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
@import '~vue2-timepicker/dist/VueTimepicker.css';

@media (min-width: 100px) {
    .container{
        max-width: 1400px;
    }
}

#textinput{
  background-color: white;
}

#myh1{
  margin-bottom: 4%;
}

</style>
