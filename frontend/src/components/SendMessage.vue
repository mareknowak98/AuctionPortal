<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">

    <div v-if="token != null">
      <h1>---</h1>
      <b-list-group v-for="message in messages" :key="message.id">
        <b-list-group-item class="auctionListItem">
          <div v-if="message.dest == 'to'">
            <p>From: {{message.text}}</p>
          </div>
          <div v-else>
            <p>To: {{message.text}}</p>
          </div>
          <p>Date: {{message.date}}</p>

        </b-list-group-item>
      </b-list-group>

      <b-form-textarea
        id="textarea"
        v-model="messageText"
        placeholder="Enter message..."
        rows="3"
        max-rows="6"
      ></b-form-textarea>



      <b-button variant="outline-primary" v-on:click="sendMessage()">Send</b-button>

    </div>




    <div v-else>
    <h1>Log in to send messages</h1>
    </div>
  </b-jumbotron>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import {TokenService} from '../store/service';
import axios from 'axios';

  export default {
    name: "UserMessage",
    components:{
        Navbar,
    },
    computed: {

    },
    data() {
      return {
        userToId: '',
        messageText: '',
        messages: [],
      }
    },

    mounted: function () {
      this.userToId = this.$route.params.userId;
      this.getMessages()

    },

    methods:{
      sendMessage(){
          const formData = new FormData();
          formData.append("to_user_id", this.userToId)
          formData.append("text", this.messageText)

          let axiosConfig = {
              headers: {
                  'Authorization': 'Token ' + localStorage.getItem("user-token")
              }
          };
          axios.post(`http://127.0.0.1:8000/api/messaging/send/`, formData, axiosConfig)
              .then(res => console.log(res.data))
              .catch(err => console.log(err))
          console.log("test" + this.profileId)
      },
      getMessages(){
          const formData = new FormData();
          formData.append("userToID", this.userToId)

          let axiosConfig = {
              headers: {
                  'Authorization': 'Token ' + localStorage.getItem("user-token")
              }
          };
          axios.post(`http://127.0.0.1:8000/api/messages/getMessagesWithUser/`, formData, axiosConfig)
              .then(res => this.messages = res.data)
              .then(res =>{
                this.processMessages()
              })
              .catch(err => console.log(err))

          // this.processMessages()
      },

      convertToJSON(array) {
        var objArray = [];
        for (var i = 1; i < array.length; i++) {
          objArray[i - 1] = {};
          for (var k = 0; k < array[0].length && k < array[i].length; k++) {
            var key = array[0][k];
            objArray[i - 1][key] = array[i][k]
          }
        }

        return objArray;
      },

      processMessages(){
        let messageList = []
        console.log(this.messages['to'][0].id)
        for (let msg in this.messages['to']){
          let tmp = []
          tmp.push(this.messages['to'][parseInt(msg)].id)
          tmp.push("to")
          tmp.push(this.messages['to'][parseInt(msg)].messageContent)
          tmp.push(this.messages['to'][parseInt(msg)].messageCreatedAt)
          messageList.push(tmp)
        }
        for (let msg in this.messages['from']){
          let tmp = []
          tmp.push(this.messages['from'][parseInt(msg)].id)
          tmp.push("from")
          tmp.push(this.messages['from'][parseInt(msg)].messageContent)
          tmp.push(this.messages['from'][parseInt(msg)].messageCreatedAt)
          messageList.push(tmp)
        }
        messageList = messageList.sort(function(a, b) {
          return a[0] - b[0];
        });
        messageList.unshift(['id', 'dest', 'text', 'date'])
        this.messages = this.convertToJSON(messageList)

      },
    },
    created() {
      let token;
      this.token = TokenService.getToken();

    }
  }
</script>

<style scoped>
@media (min-width: 100px) {
    .container{
        max-width: 1400px;
    }
}
</style>
