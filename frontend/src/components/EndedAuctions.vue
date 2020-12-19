<template>
  <div class="container">
  <navbar></navbar>

  <b-jumbotron class="jumbotron jumbotron-home">
    <div>
    <b-form-select v-on:change="filterEndedAuctions()" v-model="selected" class="mb-3">
      <b-form-select-option value="1">All ended</b-form-select-option>
      <b-form-select-option value="2">Sold</b-form-select-option>
      <b-form-select-option value="3">Unsold</b-form-select-option>

    </b-form-select>
    </div>

    <b-list-group v-for="auction in my_auctions" :key="auction.id">
      <!-- {{auction}} -->

      <b-container class="bv-example-row bv-example-row-flex-cols">

        <b-row align-v="center">
          <!-- <b-col sm="10"> -->
          <b-list-group-item :to="$basePath + '/auctions/' + auction.id" class="auctionListItem">
            <b-card no-body class="overflow-hidden">
              <b-row no-gutters>
                <tr>
                  <td width="300px">
                  <b-card-img :src="'http://localhost:8000' + auction.image"  fluid alt="Responsive image"></b-card-img>
                </td>
                </tr>
                <b-col>
                  <b-card-body :title="auction.product_name">
                    <b-card-text>
                      <div id="entity-list">
                        <td id="mytext" v-html="auction.description"></td>
                      </div>
                    </b-card-text>
                    <p>Highest offer: <strong>{{auction.highest_bid}}$</strong></p>
                    <Roller :text="auction.time_to_end"/>
                  </b-card-body>
                </b-col>
              </b-row>
            </b-card>
          </b-list-group-item>
          <!-- </b-col> -->


        </b-row>

      </b-container>

    </b-list-group>
  <Footer></Footer>
  </b-jumbotron>
  </div>
</template>



<script>
import Navbar from './Navbar.vue'
import Footer from './Footer.vue'


import axios from 'axios';
  export default {
    name: "EndedAuctions",
    components:{
        Navbar,
        Footer,
    },

    data() {
      return {
        selected: '',
        my_auctions: [],

      }
    },

    mounted: function () {
      this.getMyInActiveAuctions()
    },


    methods:{
      getMyInActiveAuctions(){
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.$getToken()
          }
        };
        axios.get(`http://127.0.0.1:8000/api/auctions/getMyAuctions/?active=False`, axiosConfig)
        .then(res => this.my_auctions = res.data)
        .catch(err => console.log(err))
      },

      filterEndedAuctions(){
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.$getToken()
          }
        };
        let query = "http://127.0.0.1:8000/api/auctions/getMyAuctions/?active=False"
        if (this.selected == 2)
          query += "" + "&ended=True"
        if (this.selected == 3)
          query += "" + "&ended=False"
        console.log(query)
        axios.get(query, axiosConfig)
        .then(res => this.my_auctions = res.data)
        .catch(err => console.log(err))
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
</style>
