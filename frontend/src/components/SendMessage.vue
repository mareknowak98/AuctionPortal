<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">
    <div v-if="token != null">
      <b-list-group-item id="userto">
      <b-avatar button v-on:click="$goToAnotherPage('/profile/' + profileData.id)" :src="profileData.profileAvatar" size="5rem" variant="primary" text="FF"></b-avatar>
        {{profileData.profileUser.username}}
      </b-list-group-item>
    <section ref="chatArea" class="chat-area">
      <b-col>
        <div>
            <p v-for="message in messagesProcessed" class="message" :key="message.text" :class="{ 'message-out': message.dest === 'from', 'message-in': message.dest !== 'from' }">
              {{ message.text }}
            </p>

        </div>
      </b-col>
      <b-container id="texttable" class="bv-example-row">
        <b-row>
          <b-col cols="10">
            <b-form-textarea
            id="textarea"
            v-model="messageText"
            placeholder="Enter message..."
          ></b-form-textarea>
          </b-col>
          <b-col cols="2">
              <b-button id="sendbutton" block variant="outline-primary" v-on:click="sendMessage()">Send</b-button>
          </b-col>
        </b-row>
      </b-container>
    </section>
    



    </div>
    <div v-else>
      <h1>Log in to send messages</h1>
    </div>
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
    name: "UserMessage",
    components:{
        Navbar,
        Footer,
    },
    computed: {

    },
    data() {
      return {
        userToId: '',
        messageText: '',
        messages: [],
        messagesProcessed: [],
        profileData: [],

      }
    },

    mounted: function () {
      this.userToId = this.$route.params.userId;
      this.getMessages()
      this.getProfileData()

    },

    methods:{
      sendMessage(){
          const axiosFormData = new FormData();
          axiosFormData.append("to_user_id", this.userToId)
          axiosFormData.append("text", this.messageText)

          let axiosTokenConfig = {
              headers: {
                  'Authorization': 'Token ' + localStorage.getItem("user-token")
              }
          };
          axios.post(`https://auctionportalbackend.herokuapp.com/api/messaging/send/`, axiosFormData, axiosTokenConfig)
              .then(res => res.data)
              .then(res => {
                this.getMessages()
              })
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
          axios.post(`https://auctionportalbackend.herokuapp.com/api/messages/getMessagesWithUser/`, formData, axiosConfig)
              .then(res => this.messages = res.data)
              .then(res => this.processMessages())
              .catch(err => console.log(err))
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
        for (let msg=0; msg < this.messages['to'].length; msg++){
          let tmp = []
          tmp.push(this.messages['to'][parseInt(msg)].id)
          tmp.push("to")
          tmp.push(this.messages['to'][parseInt(msg)].messageContent)
          tmp.push(this.messages['to'][parseInt(msg)].messageCreatedAt)
          messageList.push(tmp)
        }
        for (let msg=0; msg < this.messages['from'].length; msg++){
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
        this.messagesProcessed = this.convertToJSON(messageList)
      },
      getProfileData(){
        let axiosConfig = {
            headers: {
                'Authorization': 'Token ' + localStorage.getItem("user-token")
            }
        };
        axios.get(`https://auctionportalbackend.herokuapp.com/api/profileUser/getUserImage?user_id=` + this.$route.params.userId, axiosConfig)
            .then(res => this.profileData = res.data)
            .catch(err => console.log(err))
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

body, html {
  font-family: sans-serif;
  font-weight: 100;
  background: #7b4397;  /* fallback for old browsers */
  background: -webkit-linear-gradient(to right, #dc2430, #7b4397);  /* Chrome 10-25, Safari 5.1-6 */
  background: linear-gradient(to right, #dc2430, #7b4397); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}

.headline {
  text-align: center;
  font-weight: 100;
  color: white;
}
.chat-area {
  background: white;
  border-radius: 10px;
  height: 100%;
  max-height: 300px;
  padding: 1em;
  padding-bottom: 0%;
  overflow: auto;
  max-width: 80%;
  margin: 0 auto 2em auto;
  margin-bottom: 0%;
  box-shadow: 2px 2px 5px 2px rgba(0, 0, 0, 0.3)
}
.message {
  width: 45%;
  height: 10%;
  border-radius: 10px;
  padding: .5em;
/*   margin-bottom: .5em; */
  font-size: .8em;
}
.message-out {
  background: #407FFF;
  color: white;
  margin-left: 55.5%;
}
.message-in {
  background: #F1F0F0;
  color: black;
}

#texttable{
  position: relative;
  bottom: 0;
  margin-top: 50px;
  padding-bottom:1%;
  display: flex;
  flex-direction: column-reverse;
}

#textarea{
  height: 80px;
}

#sendbutton{
  height: 80px;
}

#userto{
  padding-bottom: 0%;
  overflow: auto;
  max-width: 80%;
  margin: 0 auto 2em auto;
  margin-bottom: 1%;
  background-color: transparent;
  border-color: transparent;
}

</style>
