import Vue from "vue";
import App from "./App.vue";
import Register from './components/Register.vue';
import Home from './views/Home.vue';
import ListAuctions from './components/ListAuctions.vue';


import "./registerServiceWorker";
// import router from "./router";
import store from "./store";
import axios from "axios";
import VueRouter from 'vue-router';

window.axios = require('axios');
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
Vue.use(VueRouter);

// Install BootstrapVue
Vue.use(BootstrapVue)
    // Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


const basePath = process.env.BASE_PATH || '/auctions';
console.log(basePath)
const routes = [{
        path: basePath + "/register",
        name: "register",
        component: Register
    },
    {
        path: basePath + "/",
        name: "home",
        component: Home
    },
    {
        path: basePath + "/auctions",
        name: "auction",
        component: ListAuctions
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
        $getCategories: function() {
            axios.post('http://127.0.0.1:8000/api/categories', {})
                .then(resp => {
                    this.categories = resp.data;
                })
                .catch(err => {
                    console.log(err);
                })
        },
        $getUserId: function() {
            return parseInt(localStorage.getItem("id"));
        },
    },

})

const router = new VueRouter({
    routes: routes,
    mode: 'history'
});

Vue.config.productionTip = false;

// new Vue({
//     router: router,
//     store,
//     render: h => h(App)
// }).$mount("#app");

Vue.prototype.$basePath = basePath;

new Vue({
    el: '#app',
    router: router,
    render: h => h(App)
});