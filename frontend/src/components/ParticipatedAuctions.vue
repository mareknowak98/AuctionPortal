<template>
  <div class="container">
  <navbar></navbar>

  <b-jumbotron class="jumbotron jumbotron-home">
    <div>
    <b-form-select v-on:change="getMyParticipatedAuctions()" v-model="selected" class="mb-3">
      <b-form-select-option value="1">Current</b-form-select-option>
      <b-form-select-option value="2">Ended</b-form-select-option>

    </b-form-select>
    </div>

    <b-list-group v-for="auction in my_auctions" :key="auction.id">
      <!-- {{auction}} -->

      <b-container class="bv-example-row bv-example-row-flex-cols">

        <b-row align-v="center">
          <!-- <b-col sm="10"> -->
          <b-list-group-item :to="'/auctions/' + auction.id" class="auctionListItem">
            <b-card no-body class="overflow-hidden">
              <b-row no-gutters>
                <tr>
                  <td width="300px">
                  <b-card-img :src="auction.auctionImage"  fluid alt="Responsive image"></b-card-img>
                </td>
                </tr>
                <b-col>
                  <b-card-body :title="auction.auctionProductName">
                    <b-card-text>
                      <div id="entity-list">
                        <td id="mytext" v-html="auction.auctionDescription"></td>
                      </div>
                    </b-card-text>
                    <p>Highest offer: <strong>{{auction.auctionHighestBid }}$</strong></p>
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
        selected: 1,
        my_auctions: [],

      }
    },

    mounted: function () {
      this.getMyParticipatedAuctions()
    },


    methods:{
      getMyParticipatedAuctions(){
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.$getToken()
          }
        };
        let query = "https://auctionportalbackend.herokuapp.com/api/auctions/getMyParticipatedAuctions/?active="
        if (this.selected == 1)
          query += "" + "True"
        if (this.selected == 2)
          query += "" + "False"
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
