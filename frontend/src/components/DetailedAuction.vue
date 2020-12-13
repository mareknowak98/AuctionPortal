<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">

    <b-container class="bv-example-row">
      <b-row>
        <b-col sm="4">
          <enlargeable-image :src=auction.image :src_large=auction.image />
        </b-col>
        <b-col sm="5">
          <h1>{{auction.product_name}}</h1>
          <h2>Highest offer: <strong>{{auction.highest_bid}}$</strong></h2>
          <p>Category: <strong>{{auction.category.category_name}}</strong></p>
          <div v-if="auction.is_new==null">Condition: -</div>
          <div v-if="auction.is_new==true">Condition: New</div>
          <div v-if="auction.is_new==false">Condition: Used</div>
          <p>Auction in term: {{auction.date_started}} - {{auction.date_end}}</p>
          <p>Time to end: {{time_left}}</p>
          <div v-if="auction.is_shipping_av==true">
          <p>Shipping: <strong>Yes ({{auction.auctionShippingCost}})$ </strong></p></div>
          <div v-if="auction.is_shipping_av==false">
          <p>Shipping: No</p></div>
          <div v-if="auction.is_shipping_av==null">
          <p>Shipping: - </p></div>
        </b-col>
        <b-col sm="3">
          <b-container class="bv-example-row">
            <b-row>
              <b-col sm="10">
                <div v-if="token != null">
                    <div role="group">
                        <label for="input-live">Your bid($):</label>
                        <b-form-input
                        id="input-live"
                        v-model="bid"
                        :state="nameState"
                        aria-describedby="input-live-help input-live-feedback"
                        placeholder="Enter your bid amount($)"
                        trim
                        ></b-form-input>
                        <b-form-invalid-feedback id="input-live-feedback">
                        Enter a numeric value
                        </b-form-invalid-feedback>
                      <b-row>
                        <b-col sm="12">
                          <b-button block type="submit" variant="secondary" v-on:click="bidAuction">Submit</b-button>
                          <h1></h1>
                        </b-col>
                      </b-row>
                    </div>
                </div>
          <p> </p>
          from: <b-link v-on:click="$goToAnotherPage('/profile/' + userProfileId + '/')">{{auction.user_seller.username}}</b-link>
          <div>
             <b-form-rating
               variant="warning"
               v-model="user_rating"
               readonly
               show-value
               show-value-max
               precision="2"
             ></b-form-rating>
           </div>
         </b-col>
       </b-row>
     </b-container>

          <p></p>

        </b-col>

        <b-col sm="12">
        <p> </p>
        <h2>Description:</h2>
        <td id="mytext" v-html="auction.description">

        </td>
      </b-col>
      <b-col sm="0">
      </b-col>

      </b-row>

    </b-container>

    <!-- {{ auction }} -->
    <Footer></Footer>
  </b-jumbotron>
  </div>
</template>
<script>
import Navbar from './Navbar.vue';
import Footer from './Footer.vue'
import {TokenService} from '../store/service';
import axios from 'axios';

  export default {
    name: "DetailedAuction",
    components:{
        Navbar,
        Footer,
    },
    computed: {
      nameState() {
        if (this.bid == "")
          return "isnull"
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
          time_left: '',
          user_rating: '',
      }
    },
    mounted: function (){
      let recaptchaScript = document.createElement('script')
      recaptchaScript.async = true
      recaptchaScript.setAttribute('src', 'https://unpkg.com/@diracleo/vue-enlargeable-image/dist/vue-enlargeable-image.min.js')
      document.head.appendChild(recaptchaScript)

      // let recaptchaScript2 = document.createElement('script')
      // recaptchaScript2.async = true
      // recaptchaScript2.setAttribute('src', 'https://cdnjs.cloudflare.com/ajax/libs/vue/2.5.17/vue.js')
      // document.head.appendChild(recaptchaScript2)

      this.token = TokenService.getToken();
      this.auctionid = this.$route.params.auctionId;
      this.getAuction(this.auctionid)
      this.getUserProfileId();
      window.setInterval(() => {
        this.getTimeToEnd()
      }, 1000)


    },


    methods:{
    getAuction(id){
    console.log("http://localhost:8000/api/auctions/" + id)
      axios.get("http://localhost:8000/api/auctions/" + id)
        .then(res => this.auction = res.data)
        .then(res => this.getUserAvgRating(this.auction.user_seller.id))
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

    getTimeToEnd() {
      try {
        var ending_date = new Date(this.auction.date_end);
        var now_date = new Date();
        var time_between = ending_date - now_date;
        var days = parseInt((time_between)/(24*3600*1000));
        time_between -= days*(24*3600*1000);
        var hours = parseInt((time_between)/(3600*1000));
        time_between -= hours*(3600*1000);
        var minutes = parseInt((time_between)/(60*1000));
        time_between -= minutes*(60*1000);
        var seconds = parseInt((time_between)/(1000));
        var res = "" + days + "d" + hours +":" + minutes + ":" + seconds + "";
        this.time_left = res
      }
      catch (error){
        this.time_left = ""
      }
    },

    getUserAvgRating(id){
      axios.get(`http://127.0.0.1:8000/api/opinion/getUserAvgRating?user_id=` + this.auction.user_seller.id)
          .then(res => console.log(this.user_rating = parseFloat(res.data)))
          .catch(err => console.log(err))
    },

    },

    created() {

    }
  }
</script>

<style scoped>
.jumbotron-home{
    margin: 0%;
    padding: 1%;
    padding-left:0.5%;
    padding-right:0.5%;

}

@media (min-width: 100px) {
    .container{
        max-width: 1400px;
    }
}
#mytext{
  background-color: white;
  border-radius: 10px;

}
</style>
