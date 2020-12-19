<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">

  <div v-if="$getToken != null">
    <h1 id="myh1">Edit auction : {{auction.title}}</h1>

    <notification v-if="$route.query.success === true" messageType="success">
     Report has been
     <span v-if="$route.query.type === 'publish'">published</span>
     <span v-else>activated</span>
   </notification>
   <notification v-if="$route.query.success === false" messageType="failure">Error occured</notification>

    <b-form @submit.prevent="updateAuction" >
      <b-container class="bv-example-row">
        <b-row class="justify-content-md-center">
          <b-col col lg="8">
            <!-- {{auction}} -->

            <b-form-group>
            <p>Choose image</p>
            <b-form-file
              v-model="new_image"

              placeholder="Choose a file or drop it here..."
              drop-placeholder="Drop file here..."
              type='file'
            ></b-form-file>
            </b-form-group>

            <b-form-group id="input-group-1" label="Name of auction:" label-for="input-1">
              <b-form-input
                id="input-1"
                v-model="auction.product_name"
                placeholder="Enter auction name"
              ></b-form-input>
            </b-form-group>


            <label class="mr-2">Category:&nbsp;</label>
            <b-form-group>
              <b-form-select inline v-model="new_selectedCategory">
                <template #first>
                  <b-form-select-option :value="null" disabled>-- Please select category --</b-form-select-option>
                  <option v-for="category in categories" v-bind:key="category.id" v-bind:value="category.id">
                    {{ category.category_name }}
                  </option>
                </template>
              </b-form-select>
            </b-form-group>


            <p>Auction Description</p>
            <div id="textinput">
              <vue-editor v-model="auction.description" :editorToolbar="customToolbar"></vue-editor>
            </div>

            <p>    </p>
            <p>Condition: </p>
            <b-form-radio-group label="is new">
              <b-form-radio v-model="auction.is_new" name="some-radios" value=true>New</b-form-radio>
              <b-form-radio v-model="auction.is_new" name="some-radios" value=false>Used</b-form-radio>
            </b-form-radio-group>

            <p>    </p>
            <p>Is shipping available: </p>
            <b-form-radio-group label="is shipping">
              <b-form-radio v-model="auction.is_shipping_av" name="some-radios" value=true>Yes</b-form-radio>
              <b-form-radio v-model="auction.is_shipping_av" name="some-radios" value=false>No</b-form-radio>
            </b-form-radio-group>

            <div v-if="auction.is_shipping_av == 'true' || auction.is_shipping_av == true">
              <div role="group">
                  <label for="input-live">Enter shipping costs: </label>
                  <b-form-input
                  id="input-live"
                  v-model="auction.auctionShippingCost"
                  aria-describedby="input-live-help input-live-feedback"
                  trim
                  ></b-form-input>
                  <b-form-invalid-feedback id="input-live-feedback">
                  Enter a numeric value
                  </b-form-invalid-feedback>
              </div>
            </div>
            <p>         </p>
            <b-button type="submit" variant="secondary">Submit</b-button>




          </b-col>
        </b-row>
      </b-container>
    </b-form>
  </div>

  <Footer></Footer>
  </b-jumbotron>
  </div>
</template>



<script>
import Navbar from './Navbar.vue'
import Footer from './Footer.vue'
import { VueEditor } from "vue2-editor";


import axios from 'axios';
  export default {
    name: "EditAuction",
    components:{
        Navbar,
        Footer,
        VueEditor,
    },

    data() {
      return {
        auction: [],
        categories: [],
        new_selectedCategory: '',
        new_image: null,
        new_product_name: '',
        customToolbar: [["bold", "italic", "underline"], [{ list: "ordered" }, { list: "bullet" }]],


      }
    },

    mounted: function () {
      this.categories = this.getCategories();

    },
    created() {
      this.getAuction(this.$route.params.auctionId)
    },


    methods:{
      getAuction(id){
        axios.get("http://localhost:8000/api/auctions/" + id)
          .then(res => this.auction = res.data)
          .catch(err => console.log(err));
      },
      getCategories(){
        axios.get("http://127.0.0.1:8000/api/categories/")
          .then(res => {
          this.categories = res.data
          })
          .catch(err => console.log(err));
      },
      updateAuction(){
        const formData = new FormData();
        if (this.new_image != null && this.new_image != '')
          formData.append("image", this.new_image)
        if (this.new_selectedCategory != null && this.new_selectedCategory !='')
          formData.append("category", this.new_selectedCategory)
        formData.append("product_name", this.auction.product_name)
        formData.append("description", this.auction.description)
        formData.append("is_new", this.auction.is_new)
        formData.append("is_shipping_av", this.auction.is_shipping_av)
        if (this.auction.is_shipping_av == true || this.auction.is_shipping_av == 'true')
          formData.append("auctionShippingCost", this.auction.auctionShippingCost)
        else
          formData.append("auctionShippingCost", 0.0)

        console.log("Data:")
        for (var value of formData.values()) {
           console.log(value);
        }

        let axiosConfig = {
            headers: {
                'Authorization': 'Token ' + localStorage.getItem("user-token")
            }
        };

        console.log("http://127.0.0.1:8000/api/auctioncreate/" + this.$route.params.auctionId)
        axios.patch("http://127.0.0.1:8000/api/auctioncreate/" + this.$route.params.auctionId +'/', formData, axiosConfig)
          .then(res => {
            console.log(res.status)
            alert ("Changes saved succesfully.");
            this.getAuction(this.$route.params.auctionId);
            this.$sleep(500);
            this.$router.back();
          })

          .catch(err => {
            console.log(err)
            alert ("Error ocured.");

            // commit('setMessage', {response: 'failure', type: type})

          });


      }
    },


  }
</script>

<style scoped>
@media (min-width: 100px) {
    .container{
        max-width: 1400px;
    }
}

#textinput{
  background-color: white;
}

</style>
