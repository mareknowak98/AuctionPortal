<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">

    <main id="app">
      <b-container class="bv-example-row">

      <section ref="chatArea" class="chat-area">
        <b-col>
          <div>
              <p v-for="message in messages" class="message" :key="message.body" :class="{ 'message-out': message.author === 'you', 'message-in': message.author !== 'you' }">
                <!-- <span
                  @mouseover="hover = true"
                  @mouseleave="hover = false"
                > -->
                {{ message.body }}
                <!-- <span v-if="hover">{{message.body}}</span> -->
              <!-- </span> -->

              </p>

          </div>
        </b-col>
      </section>

    </b-container>

      <section class="chat-inputs">

        <form @submit.prevent="sendMessage('in')" id="person1-form">
          <label for="person1-input">Bob</label>
          <input v-model="bobMessage" id="person1-input" type="text" placeholder="Type your message">
          <button type="submit">Send</button>
        </form>
    <button @click="clearAllMessages">Clear All</button>
        <form @submit.prevent="sendMessage('out')" id="person2-form">
          <label for="person2-input">You</label>
          <input v-model="youMessage" id="person2-input" type="text" placeholder="Type your message">
          <button type="submit">Send</button>
        </form>
      </section>
    </main>

  <Footer></Footer>
  </b-jumbotron>
  </div>
</template>



<script>
import Navbar from './Navbar.vue'
import Footer from './Footer.vue'
import Vue from "vue";

import axios from 'axios';
  export default {
    name: "AddOpinion",
    components:{
        Navbar,
        Footer,
    },

    data() {
      return {
        hover: false,
        mouse_here: '',
        bobMessage: '',
        youMessage: '',
           messages: [
             {
               body: 'Welcome to the chat, I\'m Bob!',
               author: 'bob'
             },
             {
               body: 'Thank you Bob',
               author: 'you'
             },
             {
               body: 'You\'re most welcome',
               author: 'bob'
             },
             {
               body: 'You\'re most welcome',
               author: 'bob'
             }
           ]
      }
    },

    mounted: function () {

    },


    methods:{
      sendMessage(direction) {
            if (!this.youMessage && !this.bobMessage) {
              return
            }
            if (direction === 'out') {
              this.messages.push({body: this.youMessage, author: 'you'})
              this.youMessage = ''
            } else if (direction === 'in') {
              this.messages.push({body: this.bobMessage, author: 'bob'})
              this.bobMessage = ''
            } else {
              alert('something went wrong')
            }
            Vue.nextTick(() => {
              let messageDisplay = this.$refs.chatArea
              messageDisplay.scrollTop = messageDisplay.scrollHeight
            })
          },
          clearAllMessages() {
            this.messages = []
          }
    },


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
  height: 50vh;
  padding: 1em;
  overflow: auto;
  max-width: 80%;
  margin: 0 auto 2em auto;
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
  margin-left: 50%;
}
.message-in {
  background: #F1F0F0;
  color: black;
}
.chat-inputs {
  display: flex;
  justify-content: space-between;
}
#person1-input {
  padding: .5em;
}
#person2-input {
  padding: .5em;
}

</style>
