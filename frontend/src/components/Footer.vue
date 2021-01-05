<template>
  <div>
    <b-modal id="RegisterModal" size="lg" title="Regulations of the auction portal">
      <td id="mytext" v-html="regulations"></td>
    </b-modal>
    <div id="container2">
     <div id="contacts">
       <div id="contacts--contact">
         <p>Contact us: <strong>auctionportalhelpdesk@gmail.com</strong> </p>
       </div>
       <div id="contacts--social">
         <p><b-link id="mylink" v-b-modal.RegisterModal>Conditions of Use</b-link></p>
       </div>
     </div>
     <div id="mentions">
       <p>WfiIS AGH 2020/2021. All rights reserved.</p>
     </div>
    </div>
  </div>
</template>


<script>
// import axios from 'axios';
export default {
    name: "Footer",
    data(){
      return {
      regulations: "<p><strong>Regulations of the auction portal</strong></p><p><strong>This document specifies the terms of using the auction portal.</strong></p><p><strong>1.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;General Provision</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The auction site is a communication platform for concluding commercial transactions between users.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Using the auction portal is free.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auctions enable the presentation of goods offered by the seller.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Bidding on the highest amount does not require a commercial transaction, but only allows contact between the seller and the buyer.</p><p>&nbsp;</p><p><strong>2.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Registration</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Users of the auction site may be natural persons over 18 years of age.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To register a user, the following are required: login / user name, e-mail address and accept these regulations.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After logging in, the user is able to add their own auctions and bidding.</p><p>&nbsp;</p><p><strong>3.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Personal data protection</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;By registering, the user consents to the processing of his personal data for the purposes related solely to the functioning of the auction site.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Access to personal data and their change is possible by editing the user's own account.</p><p>&nbsp;</p><p><strong>4.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Offers</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The items listed on the auction portal should be free from physical and legal defects, or these defects should be described by the seller.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The presented photos may not contain pornographic materials or materials considered offensive.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The description of items should be prepared in a truthful manner, without using profanity.</p><p>&nbsp;</p><p><strong>5.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auction</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It is allowed to participate in auctions using only one account.</p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It is unacceptable to bid on your own auctions.</p><p><br></p><p><strong>6.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Comments</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The use of profanity, slander, in the comments is prohibited.</p><p><br></p><p><strong>7.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Final Provisions</strong></p><p>\t-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Failure to comply with the regulations may result in the removal of the auction or the user of the auction portal by its administrator.</p>",
      }
    },
};
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css?family=Open+Sans');

body{
  display:flex;
  background-color:#F0F8FF;
  height:95vh;
  justify-content:center;
  align-items:flex-end;
  font-family:Open Sans;
}

#container2{
  border-radius: 10px;
  padding-top:2%;
  margin-bottom:0%;
  margin-top:15%;
  /* width:100vw; */
  color:white;
  background-color:	#6c757d;
  display:flex;
  flex-direction:column;
  align-items:center;
}
#contacts{
  display:flex;
  justify-content:space-around;
  align-items:center;
  width:100%;
}
#contacts--contact{
  text-align:right;
}
#contacts--social{
  width:20%;
  display : flex;
  justify-content : space-between;
}
#contacts--social div{
  height:30px;
  width:30px;
  background-color:white;
  border-radius:50%;
}
#mentions p {
  font-size:0.7em;
}
#mylink{
  color: white;
}
</style>
