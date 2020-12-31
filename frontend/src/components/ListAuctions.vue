<template>
  <div class="">

    <b-list-group v-for="(auction, i) in auctions" :key="auction.id">
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
                <p>Time to end:{{auction.time_to_end}}</p>
                <Roller :text="times_to_end[i]"/>

              </b-card-body>
            </b-col>
          </b-row>
        </b-card>
      </b-list-group-item>
    </b-list-group>

    <p></p>
  </div>
</template>




<script>
import axios from "axios";
import Roller from "vue-roller";

export default {
  name: "home",
  components: {
    Roller,
  },
  data() {
    return {
      auctions: [],
      times_to_end: [],
      filters: [],
    }
  },
  mounted(){
    this.getAuctions()
    window.setInterval(() => {
      this.getTimeToEnd()
    }, 1000)

  },
  methods: {
    getAuctions(){
      axios.get("https://auctionportalbackend.herokuapp.com/api/auctions/")
        .then(res => (this.auctions = res.data))
        .then(res =>{
          this.getTimeToEnd();
        })
        .catch(err => console.log(err));
    },

    getTimeToEnd() {
      this.times_to_end = []
      try {
        for (var i in this.auctions){
          var ending_date = new Date(this.auctions[i].auctionDateEnd );
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
          this.times_to_end.push(res)
          }
        }
        catch (error){
          this.times_to_end = []
        }
      },
    getFilteredAuctions: function(searchdata) {
      console.log(searchdata)
      let json_dict = JSON.stringify(searchdata)
      let querybuilder = "https://auctionportalbackend.herokuapp.com/api/auctions/?"
      console.log("querybuilder")
      if (searchdata.search != '' && searchdata.search_in_desc == false)
        querybuilder += "title=" + searchdata.search;
      if (searchdata.search != '' && searchdata.search_in_desc == true)
        querybuilder += "title=" + searchdata.search + "&desc=" + searchdata.search;
      if (searchdata.selectedCategory)
        querybuilder += "&cat=" + searchdata.selectedCategory;
      if (searchdata.min_price != '' && parseFloat(searchdata.min_price) >= 0.0)
        querybuilder += "&min=" + searchdata.min_price;
      if (searchdata.max_price != '' && parseFloat(searchdata.max_price) >= 0.0 && parseFloat(searchdata.max_price) >= parseFloat(searchdata.min_price))
        querybuilder += "&max=" + searchdata.max_price;
      if (searchdata.selected == true)
        querybuilder += "&new=True" 
      if (searchdata.selected == false)
        querybuilder += "&new=False" 
      if (searchdata.selected2 == true)
        querybuilder += "&ship=True" 
      if (searchdata.selected2 == false)
        querybuilder += "&ship=False"
      if (searchdata.selected3 == 1)
        querybuilder += "&price=1"
      if (searchdata.selected3 == 2)
        querybuilder += "&price=2"
      if (searchdata.selected3 == 3)
        querybuilder += "&time_left=1"

      axios.get(querybuilder)
        .then(res => (this.auctions = res.data))
        .then(res =>{
          this.getTimeToEnd();
        })
        .catch(err => console.log(err));

    }

  }
}
</script>
<style lang="scss" scoped>
#entity-list {
    max-height: 150px;
    overflow-y: scroll;
    overflow-x: hidden;
    div {
        height: 40px;
    }
}
</style>
