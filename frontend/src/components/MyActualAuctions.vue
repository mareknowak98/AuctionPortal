<template>
  <div class="container">
  <navbar></navbar>

  <b-jumbotron class="jumbotron jumbotron-home">
    <b-modal id="deleteModal" title="Are you sure?" >
      <label class="mb-2">Confirm auction removal</label>
      <template #modal-footer="{ cancel }">
        <!--   -->
        <b-button size="sm" variant="danger" @click="cancel(); deleteAuction(auction_to_del)">
          Delete
        </b-button>
        <b-button size="sm" variant="success" @click="cancel()">
          Cancel
        </b-button>
      </template>
    </b-modal>
    <!-- {{this.my_auctions}} -->
    <b-list-group v-for="auction in my_auctions" :key="auction.id">
      <!-- {{auction}} -->

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
                    <p>Highest offer: <strong>{{auction.auctionHighestBid }}$</strong></p>
                    <Roller :text="auction.time_to_end"/>
                  </b-card-body>
                </b-col>
              </b-row>
            </b-card>
          </b-list-group-item>
          </b-col>
          <b-col sm="2">
            <b-row>
              <b-button block v-on:click="$goToAnotherPage('/editauction/' + auction.id)" variant="secondary">Edit</b-button>
            </b-row>
            <b-row>
              <!-- v-b-modal.deleteModal -->
              <b-button block v-on:click="setDelAuction(auction.id)" v-b-modal.deleteModal variant="danger">Delete</b-button>
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
        my_auctions: [],
        auction_to_del: '',
      }
    },

    mounted: function () {
      this.getMyActiveAuctions()
    },


    methods:{
      getMyActiveAuctions(){
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.$getToken()
          }
        };
        axios.get(`https://auctionportalbackend.herokuapp.com/api/auctions/getMyAuctions/?active=True&ended=False`, axiosConfig)
        .then(res => this.my_auctions = res.data)
        .catch(err => console.log(err))
      },
      deleteAuction(id){
        console.log(`https://auctionportalbackend.herokuapp.com/api/auctions/` + id +'/')
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.$getToken()
          }
        };
        axios.delete(`https://auctionportalbackend.herokuapp.com/api/auctions/` + id +'/', axiosConfig)
        .then(res => console.log(res.data))
        .then(res => this.getMyActiveAuctions())
        .catch(err => console.log(err))
      },
      setDelAuction(id){
        this.auction_to_del = id;
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
