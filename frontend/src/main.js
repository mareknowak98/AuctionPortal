import Vue from "vue";
import App from "./App.vue";
import Register from './components/Register.vue';
import EnlargeableImage from '@diracleo/vue-enlargeable-image';
import "./registerServiceWorker";
import axios from "axios";
import VueRouter from 'vue-router';
import Home from './components/Home.vue';
import NewAuction from './components/CreateNewAuction.vue';
import DetailedAuction from './components/DetailedAuction.vue';
import Profile from './components/UpdateProfile.vue';
import UserProfile from './components/UserProfile.vue';
import UserMessage from './components/SendMessage.vue';
import MessageManager from './components/MessageManager.vue';
import AddOpinion from './components/AddOpinion.vue';
import MyActualAuctions from './components/MyActualAuctions.vue';
import EditAuction from './components/EditAuction.vue';
import EndedAuctions from './components/EndedAuctions.vue';
import WonAuctions from './components/WonAuctions.vue';
import ParticipatedAuctions from './components/ParticipatedAuctions.vue';
import StaffPanel from './components/StaffPanel.vue';




window.axios = require('axios');
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
Vue.use(VueRouter);
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(EnlargeableImage)
Vue.component('enlargeable-image', EnlargeableImage)
import { VueEditor } from "vue2-editor";
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';


// const basePath = process.env.BASE_PATH || '/';
// console.log(basePath)

const routes = [{
        path: "/",
        name: "home",
        component: Home
    },
    {
        path: "/register",
        name: "register",
        component: Register
    },
    // {
    //     path: basePath + "/auctions",
    //     name: "auction",
    //     component: ListAuctions
    // },
    {
        path: "/newauction",
        name: "newauction",
        component: NewAuction
    },
    {
        path: "/auctions/:auctionId",
        name: "auctionDetail",
        component: DetailedAuction
    },
    {
        path: "/myprofile",
        name: "profile",
        component: Profile
    },
    {
        path: "/profile/:profileId",
        name: "userProfile",
        component: UserProfile
    },
    {
        path: "/message/:userId",
        name: "message",
        component: UserMessage
    },
    {
        path: "/messages",
        name: "messages",
        component: MessageManager
    },
    {
        path: "/opinion/:userId",
        name: "opinion",
        component: AddOpinion
    },
    {
        path: "/activeauctions",
        name: "activeauctions",
        component: MyActualAuctions
    },
    {
        path: "/editauction/:auctionId",
        name: "editauction",
        component: EditAuction
    },
    {
        path: "/endedauctions",
        name: "endedauctions",
        component: EndedAuctions
    },
    {
        path: "/wonauctions",
        name: "wonauctions",
        component: WonAuctions
    },
    {
        path: "/participatedauctions",
        name: "participatedauctions",
        component: ParticipatedAuctions
    },
    {
        path: "/staffpanel",
        name: "staffpanel",
        component: StaffPanel
    },

    // {
    //     path: '/*',
    //     redirect: { name: 'home' }
    // }

]

Vue.mixin({
    methods: {
        $goToAnotherPage: function(page) {
            this.$router.push(page);
        },
        $goToMainPage: function() {
            if (this.$route.path !== "/") this.$router.replace("/")
        },
        $getToken: function() {
            return localStorage.getItem("user-token");
        },
        $getUserId: function() {
            let axiosConfig = {
                headers: {
                    'Authorization': 'Token ' + localStorage.getItem("user-token")
                }
            };
            var userId;
            axios.get(`https://auctionportalbackend.herokuapp.com/api/user-id`, axiosConfig)
                .then(res => this.userId = res.data[0].id)
                .catch(err => console.log(err))
            return userId;
        },
        $sleep: function(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },

    },

})

const router = new VueRouter({
    routes: routes,
    mode: 'history',
});

Vue.config.productionTip = false;

const DEFAULT_TITLE = 'BidIt';

router.afterEach((to, from) => {
    Vue.nextTick(() => {
        document.title = to.meta.title || DEFAULT_TITLE;
    });
});

// Vue.prototype.$basePath = basePath;

new Vue({
    el: '#app',
    router: router,
    render: h => h(App)
});
