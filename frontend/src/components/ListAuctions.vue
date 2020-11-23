<template>
  <div class="">
     <navbar></navbar>

    <!-- Taskbar -->
    <b-form inline @submit.prevent="updateSearch" id="searchform" class="taskbar">

      <!-- Search box -->
      <b-input-group class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-input v-model="searchTerm"></b-form-input>
        <b-input-group-append>
          <b-btn class="mb-2 mr-sm-2 mb-sm-0" variant="primary" type="submit">
            <!-- magnifying glass -->
            <div style="transform: rotate(-45deg);">&#9906;</div>
          </b-btn>
        </b-input-group-append>
      </b-input-group>

      <!-- Category selector -->
      <!-- <b-form-select v-model="selectedCategory" class="mb-2 mr-sm-2 mb-sm-0" @input="updateSearch()">
        <option disabled selected hidden value="">Category</option>
        <option value="">all</option>
        <option v-for="category in categories" v-bind:value="category.categoryId">
          {{ category.categoryTitle }}
        </option>
      </b-form-select> -->

      <!-- Auction status selector -->
      <!-- <b-form-select v-model="selectedStatus" class="mb-2 mr-sm-2 mb-sm-0" @input="updateSearch()">
        <option disabled selected hidden value="">Status</option>
          <option v-for="status in statuses" v-bind:value="status">
            {{ status }}
          </option>
      </b-form-select> -->

    </b-form>

    <!-- Auction list -->

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

  </div>
</template>




<script>
import Navbar from './Navbar.vue'
// @ is an alias to /src
import axios from "axios";

export default {
  name: "home",
  components: {
    Navbar,
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
