<template>
  <div class="">
    <b-list-group v-for="auction in auctions" :key="auction.id">

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
                        <td id="mytext" v-html="auction.description">
                        </td>
                       </div>
                </b-card-text>
                <p>Highest offer: <strong>{{auction.highest_bid}}$</strong></p>
              </b-card-body>
            </b-col>
          </b-row>
        </b-card>
        <!-- <h2>{{auction.product_name}}</h2>
        <div>
          <b-img :src= "'http://localhost:8000' + auction.image " fluid alt="Responsive image" height="180px" width="250px"></b-img>
        </div>
        <p>{{ auction.highest_bid }}</p>
        {{ auction }} -->
      </b-list-group-item>
    </b-list-group>

    <!-- <b-pagination @input="updateSearch()" align="center" class="mt-2" v-model="currentPage" :total-rows="numberOfAuctions"
                  :per-page="itemsPerPage" :limit="10"/> -->
    <p></p>
  </div>
</template>




<script>
// @ is an alias to /src
import axios from "axios";

export default {
  name: "home",
  components: {
  },
  data() {
    return {
      auctions: [],
    }
  },
  mounted(){
    this.getAuctions()
  },
  methods: {
    getAuctions(){
      axios.get("http://localhost:8000/api/auctions/")
        .then(res => (this.auctions = res.data))
        .catch(err => console.log(err));
    }
  }
};
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
