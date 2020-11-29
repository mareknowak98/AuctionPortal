<template>
  <div class="">
    <b-list-group v-for="auction in auctions" :key="auction.id">
      <b-list-group-item :to="$basePath + '/auctions/' + auction.id" class="auctionListItem">
        <h2>{{auction.product.product_name}}</h2>
        <div>
          <b-img :src= auction.product.image  fluid alt="Responsive image" height="180px" width="250px"></b-img>
        </div>
        <p>{{ auction.highest_bid }}</p>
        {{ auction }}
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
