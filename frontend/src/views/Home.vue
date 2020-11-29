<template>
  <div class="home">
      <b-jumbotron lead="abcdefg">
          <navbar></navbar>
          <template #header>AuctionPortal</template>
          <hr class="my-4">
          <p>
            <ListAuctions msg="essa"/>

          </p>
        </b-jumbotron>
  </div>
</template>



<script>
// @ is an alias to /src
import ListAuctions from '../components/ListAuctions.vue';
import Navbar from '../components/Navbar.vue';

export default {
  name: "Home",
  components: {
    ListAuctions,
    Navbar,
  }
};
</script>
