<template>
  <div class = jumbotron>
  <h1 class="title"> DetailedAuction </h1>
  <navbar></navbar>
    <h2>{{auction.product_name}}</h2>
    <div>
        <b-img :src= auction.image  fluid alt="Responsive image" height="180px" width="250px"></b-img>
    </div>
    <p>{{ auction.highest_bid }}</p>
    {{ auction }}

    <div v-if="token != null">

        <div role="group">
            <label for="input-live">Your bid:</label>
            <b-form-input
            id="input-live"
            v-model="bid"
            :state="nameState"
            aria-describedby="input-live-help input-live-feedback"
            placeholder="Enter your bid amount($)"
            trim
            ></b-form-input>

            <!-- This will only be shown if the preceding input has an invalid state -->
            <b-form-invalid-feedback id="input-live-feedback">
            Enter a numeric value
            </b-form-invalid-feedback>

            <!-- This is a form text block (formerly known as help block) -->
            <!-- <b-form-text id="input-live-help"></b-form-text> -->
            <b-button type="submit" variant="primary" v-on:click="bidAuction">Submit</b-button>
            <h1></h1>
            <b-button variant="outline-primary" v-on:click="$goToAnotherPage('/profile/' + userProfileId + '/')" >Go to users profile</b-button>

        </div>
    </div>

  </div>
</template>


{% csrf_token %}
<script>
import Navbar from './Navbar.vue';
import {TokenService} from '../store/service';
import axios from 'axios';

  export default {
    name: "Register",
    components:{
        Navbar,
    },
    computed: {
      nameState() {
        return this.isNumeric(this.bid) ? true : false
      }
    },
    data() {
      return {
          name: '',
          auctionid: '',
          bid: '',
          auction: [],
          userProfileId: '',
      }
    },

    mounted: function (){
      // this.getUserProfileId();
    },

    methods:{
    getAuction(id){
    console.log("http://localhost:8000/api/auctions/" + id)
      axios.get("http://localhost:8000/api/auctions/" + id)
        .then(res => this.auction = res.data)
        .catch(err => console.log(err));
    },

    //check if given string can be converted to numeric value
    isNumeric(str) {
        if (typeof str != "string") return false 
        return !isNaN(str) && !isNaN(parseFloat(str)) 
    },

    bidAuction(){
        var token = TokenService.getToken();
        const formData = new FormData();
        formData.append("bidPrice", this.bid)
        formData.append("bidAuction", this.auctionid)

        let axiosConfig = {
            headers: {
            'Authorization': 'Token ' + token
            }
        };

        axios.post(`http://127.0.0.1:8000/api/bids/`, formData, axiosConfig)
        .then(res => console.log(res.data))
        .catch(err => console.log(err))
        this.getAuction(this.auctionid)

    },

    getUserProfileId() {
        const formData = new FormData();
        formData.append("id", this.auctionid)
        let axiosConfig = {
            headers: {
                'Authorization': 'Token ' + localStorage.getItem("user-token")
            }
        };
        axios.post(`http://127.0.0.1:8000/api/get_user_profile_by_auction_id/`, formData, axiosConfig)
            .then(res => console.log(this.userProfileId = res.data[0]))
            .catch(err => console.log(err))
        console.log("test" + this.profileId)
        return this.userProfileId;
    },

    },

    created() {
      let token;
      this.token = TokenService.getToken();
      this.auctionid = this.$route.params.auctionId;
      this.getAuction(this.auctionid)
      this.getUserProfileId();
    }
  }
</script>

<style scoped>

</style>