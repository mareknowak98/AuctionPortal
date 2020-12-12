import Vue from "vue";
import App from "./App.vue";
import Register from './components/Register.vue';
// import Home from './views/Home.vue';
import ListAuctions from './components/ListAuctions.vue';

import "./registerServiceWorker";
// import router from "./router";
import store from "./store";
import axios from "axios";
import VueRouter from 'vue-router';
import Home from './components/Home.vue';
import NewAuction from './components/CreateNewAuction.vue';
import DetailedAuction from './components/DetailedAuction.vue';
import Profile from './components/UpdateProfile.vue';
import UserProfile from './components/UserProfile.vue';
import UserMessage from './components/SendMessage.vue';
import MessageManager from './components/MessageManager.vue';

window.axios = require('axios');
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
Vue.use(VueRouter);

// Install BootstrapVue
Vue.use(BootstrapVue)
    // Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';


const basePath = process.env.BASE_PATH || '/';
console.log(basePath)
const routes = [{

        path: basePath + "/register",
        name: "register",
        component: Register
    },
    {
        path: basePath + "",
        name: "home",
        component: Home
    },
    // {
    //     path: basePath + "/auctions",
    //     name: "auction",
    //     component: ListAuctions
    // },
    {
        path: basePath + "/newauction",
        name: "newauction",
        component: NewAuction
    },
    {
        path: basePath + "/auctions/:auctionId",
        name: "auctionDetail",
        component: DetailedAuction
    },
    {
        path: basePath + "/myprofile",
        name: "profile",
        component: Profile
    },
    {
        path: basePath + "/profile/:profileId",
        name: "userProfile",
        component: UserProfile
    },
    {
        path: basePath + "/message/:userId",
        name: "message",
        component: UserMessage
    },
    {
        path: basePath + "/messages",
        name: "messages",
        component: MessageManager
    },
]

Vue.mixin({
    methods: {
        $goToAnotherPage: function(page) {
            console.log("going");
            console.log(page);
            this.$router.push(basePath + page);
        },
        $getToken: function() {
            return localStorage.getItem("token");
        },
        $getUserId: function() {
            let axiosConfig = {
                headers: {
                    'Authorization': 'Token ' + localStorage.getItem("user-token")
                }
            };
            var userId;
            axios.get(`http://127.0.0.1:8000/api/user-id`, axiosConfig)
                .then(res => this.userId = res.data[0].id)
                .catch(err => console.log(err))
            return userId;
        },
    },

})

const router = new VueRouter({
    routes: routes,
    mode: 'history'
});

Vue.config.productionTip = false;


Vue.prototype.$basePath = basePath;

new Vue({
    el: '#app',
    router: router,
    render: h => h(App)
});