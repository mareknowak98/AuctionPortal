<template>
  <div class="container">
    <b-alert
      variant="danger"
      dismissible
      fade
      :show="showDismissibleAlert"
      @dismissed="showDismissibleAlert=false"
    >
      Log in to see Users profiles
    </b-alert>
    <b-alert
      variant="danger"
      dismissible
      fade
      :show="showOverbidAlert"
      @dismissed="showOverbidAlert=false"
    >
      You cannot overbid yourself
    </b-alert>
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">

    <b-container class="bv-example-row">
      <b-row>
        <b-col sm="4">
          <enlargeable-image :src=auction.auctionImage :src_large=auction.auctionImage />
        </b-col>
        <b-col sm="5">
          <h1>{{auction.auctionProductName}}</h1>
          <h2>Highest offer: <strong>{{auction.auctionHighestBid }}$</strong></h2>
          <p>Category: <strong>{{auction.auctionCategory.category_name}}</strong></p>
          <div v-if="auction.auctionIsNew==null">Condition: -</div>
          <div v-if="auction.auctionIsNew==true">Condition: <strong>New</strong></div>
          <div v-if="auction.auctionIsNew==false">Condition: <strong>Used</strong></div>
          <p>Auction in term: <strong>{{dataParser(auction.auctionDateStarted) }} - {{ dataParser(auction.auctionDateEnd) }}</strong></p>
          <div v-if="auction.auctionIsActive == true">
                <table>
                  <td>
                    <p>Time to end: </p>
                  </td>
                  <th>
                    <Roller :text="time_left"/>
                  </th>
                </table>          </div>
          <div v-else>
            <p>Time to end: <strong>ended</strong></p>
          </div>

          <div v-if="auction.auctionIsShippingAv ==true">
          <p>Shipping: <strong>Yes ({{auction.auctionShippingCost}})$ </strong></p></div>
          <div v-if="auction.auctionIsShippingAv ==false">
          <p>Shipping: <strong>No</strong></p></div>
          <div v-if="auction.auctionIsShippingAv ==null">
          <p>Shipping: - </p></div>
        </b-col>
        <b-col sm="3">
          <b-container class="bv-example-row">
            <b-row>
              <b-col sm="10">
                <div v-if="$getToken() != null && auction.auctionIsActive == true && user_id!=auction.auctionUserSeller.id ">
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
                        Bid must be higher than the highest offer and be numeric value
                        </b-form-invalid-feedback>
                      <b-row>
                        <b-col sm="12">
                          <b-button block type="submit" variant="secondary" v-on:click="bidAuction">Submit</b-button>
                          <b-button block v-b-modal.reportModal variant="secondary">Report violation of the rules</b-button>

                          <h1></h1>
                        </b-col>
                      </b-row>
                    </div>
                </div>
          <p> </p>

          <div v-if="$getToken() != null">
            from: <b-link v-on:click="$goToAnotherPage('/profile/' + userProfileId + '/')">{{auction.auctionUserSeller.username}}</b-link>
          </div>
          <div v-else>
            from: <b-link @click="showDismissibleAlert=true" variant="info" class="m-1">{{auction.auctionUserSeller.username}}</b-link>
          </div>
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
        <b-modal id="reportModal" title="File a report" @ok="reportAuction" ok-title="Send">

          <b-form-select v-model="report_category" :options="options" class="mb-3">
            <!-- This slot appears above the options from 'options' prop -->
            <template #first>
              <b-form-select-option :value="null" disabled>-- Please select category --</b-form-select-option>
            </template>
          </b-form-select>

          <b-form-textarea
            id="textarea"
            v-model="report_content"
            placeholder="..."
            rows="3"
            max-rows="6"
          ></b-form-textarea>
        </b-modal>

        <b-col sm="12">
        <p> </p>
        <h2>Description:</h2>
        <td id="mytext" v-html="auction.auctionDescription">
        </td>
        <h1>  </h1>
        <grid
        :cols="cols"
        :rows="rows"
        :pagination="{
            limit: 5
        }"
        :sort="Time"

        ></grid>


      </b-col>
      <b-col sm="0">
      </b-col>
      </b-row>
    </b-container>
    <Footer></Footer>
  </b-jumbotron>
  </div>
</template>
<script>
import Navbar from './Navbar.vue';
import Footer from './Footer.vue'
import {TokenService} from '../store/service';
import axios from 'axios';
import Roller from "vue-roller";
import Grid from 'gridjs-vue'

  export default {
    name: "DetailedAuction",
    components:{
        Navbar,
        Footer,
        Roller,
        Grid,
    },
    computed: {
      nameState() {
        if (this.bid == "")
          return "isnull"
        let res = this.isNumeric(this.bid) ? true : false;
        if (res)
          var res2 = parseFloat(this.bid) > parseFloat(this.auction.auctionHighestBid) + 0.01 ? true : false;
        return res && res2;
      }
    },
    data() {
      return {
          user_id: '',
          name: '',
          auctionid: '',
          bid: '',
          auction: [],
          userProfileId: '',
          time_left: '',
          user_rating: '',
          report_category: '',
          report_content: '',
          selected: null,
          options: [
            { value: 'Spam', text: 'Spam' },
            { value: 'Incorrect category', text: 'Incorrect category' },
            { value: 'Illegal objects', text: 'Illegal objects' },
            { value: 'Attempt at fraud', text: 'Attempt at fraud' },
            { value: 'Other', text: 'Other' },
          ],
          bids: [],
          cols: ['User', 'Bid', 'Time'],
          rows: [],


      }
    },
    mounted: function (){
      this.token = TokenService.getToken();
      this.auctionid = this.$route.params.auctionId;
      this.getAuction(this.auctionid)
      this.getUserProfileId();
      this.getBids();
      window.setInterval(() => {
        this.getTimeToEnd()
      }, 1000)
      window.setInterval(() => {
        this.getAuction()
      }, 10000)
      this.getUserId()
    },


    methods:{
    getAuction(id){
    console.log("https://auctionportalbackend.herokuapp.com/api/auctions/" + id)
      axios.get("https://auctionportalbackend.herokuapp.com/api/auctions/" + id)
        .then(res => this.auction = res.data)
        .then(res => this.getUserAvgRating(this.auction.auctionUserSeller.id))
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

        console.log(this.user_id)
        console.log(this.auction.auctionUserHighestBid)

        if (parseInt(this.user_id)== parseInt(this.auction.auctionUserHighestBid)){
          this.bid = ''
          this.showOverbidAlert = true;
          return;
        }

        axios.post(`https://auctionportalbackend.herokuapp.com/api/bids/`, formData, axiosConfig)
        .then(res => console.log(res.data))
        .then(res => {
          this.bid = '';
          this.getBids();
          this.getAuction(this.$route.params.auctionId);
        })
        .catch(err => console.log(err))
        this.getAuction(this.auctionid)

    },

    getUserId() {
        let axiosConfig = {
          headers: {
              'Authorization': 'Token ' + localStorage.getItem("user-token")
          }
        };

        axios.get(`https://auctionportalbackend.herokuapp.com/api/user-id`, axiosConfig)
          .then(res => this.user_id = res.data[0].id)
          .catch(err => console.log(err))
    },

    getUserProfileId() {
        const formData = new FormData();
        formData.append("id", this.auctionid)
        let axiosConfig = {
          headers: {
              'Authorization': 'Token ' + localStorage.getItem("user-token")
          }
        };
        axios.post(`https://auctionportalbackend.herokuapp.com/api/get_user_profile_by_auction_id/`, formData, axiosConfig)
          .then(res => this.userProfileId = res.data[0])
          .catch(err => console.log(err))
        return this.userProfileId;
    },

    getTimeToEnd() {
      try {
        var ending_date = new Date(this.auction.auctionDateEnd );
        var now_date = new Date();
        var time_between = ending_date - now_date;
        var days = parseInt((time_between)/(24*3600*1000));
        time_between -= days*(24*3600*1000);
        var hours = parseInt((time_between)/(3600*1000));
        time_between -= hours*(3600*1000);
        var minutes = parseInt((time_between)/(60*1000));
        time_between -= minutes*(60*1000);
        var seconds = parseInt((time_between)/(1000));
        var res = "" + days + " days " + hours +":" + minutes + ":" + seconds + "";
        this.time_left = res
      }
      catch (error){
        this.time_left = ""
      }
    },

    getUserAvgRating(id){
      axios.get(`https://auctionportalbackend.herokuapp.com/api/opinion/getUserAvgRating?user_id=` + this.auction.auctionUserSeller.id)
          .then(res => console.log(this.user_rating = parseFloat(res.data)))
          .catch(err => console.log(err))
    },
    reportAuction(){
      const formData = new FormData();
      let content = this.report_category + "\n" + this.report_content;
      console.log("Content" + content)
      formData.append("reportAuction", this.auctionid)
      formData.append("reportContent", content)

      let axiosConfig = {
          headers: {
              'Authorization': 'Token ' + localStorage.getItem("user-token")
          }
      };
      axios.post(`https://auctionportalbackend.herokuapp.com/api/report/`, formData, axiosConfig)
          .then(res => console.log(res.data))
          .catch(err => console.log(err))
    },

    getBids(){
      axios.get(`https://auctionportalbackend.herokuapp.com/api/bids/getAuctionBids/?auction_id=` + this.$route.params.auctionId)
        .then(res => console.log(this.bids = res.data))
        .then(res =>{
          this.rows = [];
          for (var i in this.bids){
            let dat = new Date(this.bids[i].bidDate);
            let tmp = [this.bids[i].bidUserBuyer.username, this.bids[i].bidPrice, dat.toISOString().split('T')[0]+ " "+ dat.toISOString().split('T')[1].split('Z')[0]]
            this.rows.push(tmp)
          }
        })
        .catch(err => console.log(err))
    },

    dataParser(date_str){
      let date =  new Date(date_str);
      return date.toISOString().split('T')[0]+ " "+ date.toISOString().split('T')[1].split('Z')[0].slice(0, -7);
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
  width: 100%;
  width: 100vw;
  background-color: white;
  border-radius: 10px;

}
</style>
