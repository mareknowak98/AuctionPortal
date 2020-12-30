<template>
  <div class="container">
  <navbar></navbar>

  <b-jumbotron class="jumbotron jumbotron-home">
    <!-- {{this.my_auctions}} -->
    <b-list-group v-for="auction in my_won_auctions" :key="auction.id">
      {{auction}}

      <b-container class="bv-example-row bv-example-row-flex-cols">

        <b-row align-v="center">
          <b-col sm="10">
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
                    <p>Bought by: <strong>{{auction.auctionHighestBid }}$</strong></p>
                  </b-card-body>
                </b-col>
              </b-row>
            </b-card>
          </b-list-group-item>
          </b-col>
          <b-col sm="2">
            <b-row>
              <b-button block v-on:click="$goToAnotherPage('/message/' + auction.auctionUserSeller.id)" variant="secondary">Write message</b-button>
            </b-row>
            <b-row>
              <!-- v-b-modal.deleteModal -->
              <!-- <b-button block v-on:click="setDelAuction(auction.id)" v-b-modal.deleteModal variant="danger">Delete</b-button> -->
            </b-row>
          </b-col>

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
    name: "MyActualAuctions",
    components:{
        Navbar,
        Footer,
    },

    data() {
      return {
        my_won_auctions: [],
      }
    },

    mounted: function () {
      this.getMyWonAuctions()
    },


    methods:{
      getMyWonAuctions(){
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.$getToken()
          }
        };
        axios.get(`https://auctionportalbackend.herokuapp.com/api/auctions/getMyWonAuctions`, axiosConfig)
        .then(res => this.my_won_auctions = res.data)
        .catch(err => console.log(err))
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
