<template>
  <div class="container">
    <navbar></navbar>
    <b-jumbotron class="jumbotron jumbotron-home">
       <b-container class="bv-example-row">
         <b-row class="text-center">
           <b-col class="myform1">
             <div>
                <b-form-group
                  id="input-group-2"
                  label="Search:"
                  label-for="input-1"
                >
                  <b-form-input
                    id="input-2"
                    v-model="form.search"
                    placeholder="Search..."
                    required
                  ></b-form-input>
                  </b-form-group>
                <b-button block v-on:click="searchAuctions()" class="my-2 my-sm-0" type="submit">Search</b-button>
                <p> </p>
              <p>Category:</p>
               <b-form-group
               >
                 <b-form-select inline v-model="form.selectedCategory">
                  <template #first>
                    <b-form-select-option :value="null" disabled>-- Please select category --</b-form-select-option>
                  </template>
                   <option v-for="category in form.categories" v-bind:key="category.id" v-bind:value="category.id">
                     {{ category.category_name }}
                   </option>
                 </b-form-select>
               </b-form-group>
               </div>

               <table>
              <b-form-group id="input-group-1" label="Price:" label-for="input-1">
                <tr>
                  <td>
                    <b-form-input
                      type="number"
                      step="0.01"
                      min=0
                      id="input-1"
                      v-model="form.min_price"
                      placeholder="min"
                    ></b-form-input>
                  </td>
                  <td>
                    <b-form-input
                      type="number"
                      step="0.01"
                      min=0
                      id="input-2"
                      v-model="form.max_price"
                      placeholder="max"
                    ></b-form-input>
                  </td>
                </tr>
              </b-form-group>

              <tr>
                <td>
                  <b-form-checkbox class="b-form-checkbox b-form-checkbox-home" v-model="form.search_in_desc" name="check-button" switch default="false">
                Search in descriptions
                </b-form-checkbox>
                </td>
              </tr>
            </table>

            <p>Condition:</p>
            <b-form-group block>
              <b-form-radio-group button-variant="secondary custom" buttons v-model="form.selected">
                <b-form-radio v-bind:value=true>New</b-form-radio>
                <b-form-radio v-bind:value=false>Used</b-form-radio>
                <b-form-radio v-bind:value=null>All</b-form-radio>
              </b-form-radio-group>
            </b-form-group>

            <p>Is shipping available:</p>
            <b-form-group>
              <b-form-radio-group button-variant="secondary custom" buttons v-model="form.selected2">
                <b-form-radio v-bind:value=true>Yes</b-form-radio>
                <b-form-radio v-bind:value=false>No</b-form-radio>
                <b-form-radio v-bind:value=null>All</b-form-radio>
              </b-form-radio-group>
            </b-form-group>


            <hr class="my-4">

            <p>Sort by:</p>
             <b-form-group>
               <b-form-radio-group button-variant="secondary custom2" stacked buttons v-model="form.selected3">
                 <b-form-radio v-bind:value=1>Price ascending</b-form-radio>
                 <b-form-radio v-bind:value=2>Price descending</b-form-radio>
                 <b-form-radio v-bind:value=3>Time left: the least</b-form-radio>
                 <b-form-radio v-bind:value=null>None</b-form-radio>
               </b-form-radio-group>
             </b-form-group>

           </b-col>
           <b-col class="myform2" cols="10">
            <ListAuctions ref='componentOne'/>
           </b-col>
         </b-row>
         <div>


         </div>
       </b-container>
       <Footer></Footer>

     </b-jumbotron>
  </div>
</template>



<script>
import ListAuctions from '../components/ListAuctions.vue';
import Navbar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
import axios from 'axios';
export default {
  name: "Home",
  components: {
    ListAuctions,
    Navbar,
    Footer,
  },
  data() {
    return {
      form: {
          search: '',
          selected: null,
          selected2: null,
          selected3: null,
          categories: [],
          selectedCategory: null,
          min_price: '',
          max_price: '',
          search_in_desc: false,
      },
    }
  },
  mounted: function () {
    this.categories = this.getCategories();
  },



  methods:{
    getCategories(){
      axios.get("https://auctionportalbackend.herokuapp.com/api/categories/")
        .then(res => {
        this.form.categories = res.data
        console.log(this.data)
        })
        .then(res=>{
          this.form.categories.push({"category_name" : "All", "id" : ""})
        })
        .catch(err => console.log(err));
    },
    searchAuctions: function() {
      this.$refs.componentOne.getFilteredAuctions(this.form);
    }
  }
};
</script>

<style scoped>
@import '../styles/style.css';

.custom {
    width: 73px !important;
}
.custom2 {
    width: 219px!important;
}


.myform1{
  padding: 0%;
  margin-left: 0%;
  margin-right: 0.3%;
  text-align: left;
}
.myform2{
  padding: 0%;
  margin: 0%;
  text-align: left;

}
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
