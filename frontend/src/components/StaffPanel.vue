<template>
  <div class="container">
  <navbar></navbar>
  <b-jumbotron class="jumbotron jumbotron-home">

    <div id="tabs" class="container">

        <div class="tabs">
            <a v-on:click="activetab=1; getReports()" v-bind:class="[ activetab === 1 ? 'active' : '' ]">Reported auctions</a>
            <a v-on:click="activetab=2; getUsers()" v-bind:class="[ activetab === 2 ? 'active' : '' ]">Ban users</a>
            <a v-on:click="activetab=3; getUsers()" v-bind:class="[ activetab === 3 ? 'active' : '' ]">Staff crew</a>
        </div>

        <div class="content">
            <div v-if="activetab === 1" class="tabcontent">
                <b-container fluid class="bv-example-row" >

                  <b-row>
                    <b-col cols="6">
                    <b-form-group
                      label="Filter"
                      label-for="filter-input"
                      label-cols-sm="3"
                      label-align-sm="right"
                      label-size="sm"
                      class="mb-0"
                    >
                      <b-input-group size="sm">
                        <b-form-input
                          id="filter-input"
                          v-model="filter"
                          type="search"
                          placeholder="Type to Search"
                        ></b-form-input>

                        <b-input-group-append>
                          <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                        </b-input-group-append>
                      </b-input-group>
                    </b-form-group>
                    </b-col>

                    <b-col  cols="6">
                    <b-form-group
                      label="Per page"
                      label-for="per-page-select"
                      label-cols-sm="6"
                      label-cols-md="4"
                      label-cols-lg="3"
                      label-align-sm="right"
                      label-size="sm"
                      class="mb-0"
                    >
                      <b-form-select
                        id="per-page-select"
                        v-model="perPage"
                        :options="pageOptions"
                        size="sm"
                      ></b-form-select>
                    </b-form-group>
                    </b-col>
                  </b-row>
                  </b-container>



                <b-container fluid>

                <b-table
                  :items="reports"
                  :fields="fields_auctions"
                  :current-page="currentPage"
                  :per-page="perPage"
                  :filter="filter"
                  :filter-included-fields="filterOn"
                  :sort-by.sync="sortBy"
                  :sort-desc.sync="sortDesc"
                  :sort-direction="sortDirection"
                  sort-icon-left
                  stacked="md"
                  show-empty
                  small
                  @filtered="onFiltered2"
                >
                  <template #cell(name)="row">
                    {{ row.value.first }} {{ row.value.last }}

                  </template>

                  <template #row-details="row">
                    <b-card>
                      <p><strong>Report deatils</strong></p>
                      <span style="white-space: pre-line">{{row.item.reportContent}}</span>
                      <p><strong>Auction deatils</strong></p>
                        <ul class='b'>
                          <li>Auction name: {{row.item.reportAuction.auctionProductName}}</li>
                          <li>Category: {{row.item.reportAuction.auctionCategory.category_name}}</li>
                          <li>Description: {{row.item.reportAuction.auctionDescription}}</li>
                          <li>Started: {{parseDate(row.item.reportAuction.auctionDateStarted)}}</li>
                          <li>Planned ending: {{parseDate(row.item.reportAuction.auctionDateEnd)}}</li>
                          <li>Is now active: {{row.item.reportAuction.auctionIsActive}}</li>
                        </ul>
                      <p><strong>Reporting user</strong></p>
                        <ul class='b'>
                          <li>Username: {{row.item.reportUser.username}}</li>
                        </ul>

                    </b-card>
                  </template>

                  <template #cell(actions)="row">
                    <b-row>
                      <b-button block size="sm" @click="row.toggleDetails" class="mr-1">
                        {{row.detailsShowing ? 'Hide' : 'Show' }}Details
                      </b-button>
                    <b-button block size="sm" @click="goToAuction(row.item)" class="mr-1">
                      To auction
                    </b-button>
                    <b-button block size="sm" @click="inforemoveAuction(row.item, row.index, $event.target)" class="mr-1">
                      Delete auction
                    </b-button>

                  </b-row>
                  </template>
                </b-table>

                <b-col sm="7" md="6" class="my-1"  offset-md="3">
                  <b-pagination
                    v-model="currentPage"
                    :total-rows="totalRowsAuctions"
                    :per-page="perPage"
                    align="fill"
                    size="sm"
                    class="my-0"
                  ></b-pagination>
                </b-col>
                <b-modal :id="removeAuctionModal.id" :title="removeAuctionModal.title" @ok="removeAuction(removeAuctionModal.content)" @hide="resetInfoModal1">
                  <pre>Confirm auction delete (removed permanently)</pre>
                </b-modal>

              </b-container>

            </div>
            <div v-if="activetab === 2" class="tabcontent">
                <b-container fluid class="bv-example-row" >
                  <b-row>
                    <b-col cols="6">
                    <b-form-group
                      label="Filter"
                      label-for="filter-input"
                      label-cols-sm="3"
                      label-align-sm="right"
                      label-size="sm"
                      class="mb-0"
                    >
                      <b-input-group size="sm">
                        <b-form-input
                          id="filter-input"
                          v-model="filter"
                          type="search"
                          placeholder="Type to Search"
                        ></b-form-input>

                        <b-input-group-append>
                          <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                        </b-input-group-append>
                      </b-input-group>
                    </b-form-group>
                    </b-col>

                    <b-col  cols="6">
                    <b-form-group
                      label="Per page"
                      label-for="per-page-select"
                      label-cols-sm="6"
                      label-cols-md="4"
                      label-cols-lg="3"
                      label-align-sm="right"
                      label-size="sm"
                      class="mb-0"
                    >
                      <b-form-select
                        id="per-page-select"
                        v-model="perPage"
                        :options="pageOptions"
                        size="sm"
                      ></b-form-select>
                    </b-form-group>
                    </b-col>
                  </b-row>
                  </b-container>

                <b-container fluid>

                <b-table
                  :items="users_table"
                  :fields="fields"
                  :current-page="currentPage"
                  :per-page="perPage"
                  :filter="filter"
                  :filter-included-fields="filterOn"
                  :sort-by.sync="sortBy"
                  :sort-desc.sync="sortDesc"
                  :sort-direction="sortDirection"
                  sort-icon-left
                  stacked="md"
                  show-empty
                  small
                  @filtered="onFiltered"
                >
                  <template #cell(name)="row">
                    {{ row.value.first }} {{ row.value.last }}
                  </template>

                  <template #cell(actions)="row">
                    <b-row>
                    <div v-if="row.item.is_superuser == true || row.item.is_staff == true">
                      <b-button size="sm" disabled @click="info1(row.item, row.index, $event.target)" class="mr-1">
                        Ban user
                      </b-button>
                    </div>
                    <div v-else>
                      <b-button size="sm" @click="info1(row.item, row.index, $event.target)" class="mr-1">
                        Ban user
                      </b-button>
                    </div>
                    <div v-if="row.item.is_superuser == true || row.item.is_staff == true">
                      <b-button size="sm" disabled @click="info2(row.item, row.index, $event.target)" class="mr-1">
                        Unban user
                      </b-button>
                    </div>
                    <div v-else>
                      <b-button size="sm" @click="info2(row.item, row.index, $event.target)" class="mr-1">
                        Unban user
                      </b-button>
                    </div>
                  </b-row>
                  </template>
                </b-table>

                <b-col sm="7" md="6" class="my-1"  offset-md="3">
                  <b-pagination
                    v-model="currentPage"
                    :total-rows="totalRows"
                    :per-page="perPage"
                    align="fill"
                    size="sm"
                    class="my-0"
                  ></b-pagination>
                </b-col>
                <b-modal :id="banModal.id" :title="banModal.title" @ok="deactivateUser(banModal.content)" @hide="resetInfoModal1">
                  <pre>Deactivate user account (can be activate later) </pre>
                </b-modal>
                <b-modal :id="unbanModal.id" :title="unbanModal.title" @ok="activateUser(unbanModal.content)" @hide="resetInfoModal2">
                  <pre>Activate user account</pre>
                </b-modal>
              </b-container>

            </div>
            <div v-if="activetab === 3" class="tabcontent">
              <b-container fluid class="bv-example-row" >
                <b-row>
                  <b-col cols="6">
                  <b-form-group
                    label="Filter"
                    label-for="filter-input"
                    label-cols-sm="3"
                    label-align-sm="right"
                    label-size="sm"
                    class="mb-0"
                  >
                    <b-input-group size="sm">
                      <b-form-input
                        id="filter-input"
                        v-model="filter"
                        type="search"
                        placeholder="Type to Search"
                      ></b-form-input>

                      <b-input-group-append>
                        <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                      </b-input-group-append>
                    </b-input-group>
                  </b-form-group>
                  </b-col>

                  <b-col  cols="6">
                  <b-form-group
                    label="Per page"
                    label-for="per-page-select"
                    label-cols-sm="6"
                    label-cols-md="4"
                    label-cols-lg="3"
                    label-align-sm="right"
                    label-size="sm"
                    class="mb-0"
                  >
                    <b-form-select
                      id="per-page-select"
                      v-model="perPage"
                      :options="pageOptions"
                      size="sm"
                    ></b-form-select>
                  </b-form-group>
                  </b-col>
                </b-row>
                </b-container>

              <b-container fluid>
              <b-table
                :items="users_table"
                :fields="fields_staff"
                :current-page="currentPage"
                :per-page="perPage"
                :filter="filter"
                :filter-included-fields="filterOn"
                :sort-by.sync="sortBy"
                :sort-desc.sync="sortDesc"
                :sort-direction="sortDirection"
                sort-icon-left
                stacked="md"
                show-empty
                small
                @filtered="onFiltered"
              >
                <template #cell(name)="row">
                  {{ row.value.first }} {{ row.value.last }}
                </template>

                <template #cell(actions)="row">
                  <b-row>
                  <div v-if="row.item.is_superuser == true || row.item.is_active == false">
                    <b-button size="sm" disabled @click="info1_staff(row.item, row.index, $event.target)" class="mr-1">
                      Add to staff
                    </b-button>
                  </div>
                  <div v-else>
                    <b-button size="sm" @click="info1_staff(row.item, row.index, $event.target)" class="mr-1">
                      Add to staff
                    </b-button>
                  </div>
                  <div v-if="row.item.is_superuser == true">
                    <b-button size="sm" disabled @click="info2_staff(row.item, row.index, $event.target)" class="mr-1">
                      Remove from staff
                    </b-button>
                  </div>
                  <div v-else>
                    <b-button size="sm" @click="info2_staff(row.item, row.index, $event.target)" class="mr-1">
                      Remove from staff
                    </b-button>
                  </div>
                </b-row>
                </template>
              </b-table>

              <b-col sm="7" md="6" class="my-1"  offset-md="3">
                <b-pagination
                  v-model="currentPage"
                  :total-rows="totalRows"
                  :per-page="perPage"
                  align="fill"
                  size="sm"
                  class="my-0"
                ></b-pagination>
              </b-col>

              <b-modal :id="grantStaffModal.id" :title="grantStaffModal.title"  @ok="grantStaffPrivillege(grantStaffModal.content)" @hide="resetInfoModal3">
                This will grant staff member privileges to this user.
              </b-modal>
              <b-modal :id="revokeStaffModal.id" :title="revokeStaffModal.title" @ok="revokeStaffPrivilege(revokeStaffModal.content)" @hide="resetInfoModal4">
                This will remove staff member privileges from this user.
              </b-modal>
            </b-container>
            </div>
        </div>
    </div>

  <Footer></Footer>
  </b-jumbotron>
  </div>
</template>


<script>
import Navbar from './Navbar.vue'
import Footer from './Footer.vue'
import axios from 'axios';

  export default {
    name: "StaffPanel",
    components:{
        Navbar,
        Footer,
    },

    data() {
      return {
        activetab: 1,
        reports: [],
        users: [],
        users_table: [],

        fields: [
          { key: 'id', label: 'User id', sortable: true, sortDirection: 'desc' },
          { key: 'username', label: 'User username', sortable: true, class: 'desc' },
          { key: 'email', label: 'User email', sortable: true, sortDirection: 'desc' },
          {
            key: 'is_active',
            label: 'Is Active',
            formatter: (value, key, item) => {
              return value ? 'Yes' : 'No'
            },
            sortable: true,
            sortByFormatted: true,
            filterByFormatted: true
          },
          { key: 'actions', label: 'Actions' }
        ],

        fields_staff: [
          { key: 'id', label: 'User id', sortable: true, sortDirection: 'desc' },
          { key: 'username', label: 'User username', sortable: true, class: 'desc' },
          { key: 'email', label: 'User email', sortable: true, sortDirection: 'desc' },
          {
            key: 'is_staff',
            label: 'Is staff member',
            formatter: (value, key, item) => {
              return value ? 'Yes' : 'No'
            },
            sortable: true,
            sortByFormatted: true,
            filterByFormatted: true
          },
        { key: 'actions', label: 'Actions' }
        ],

        fields_auctions: [
          { key: 'id', label: 'Report id', sortable: true, sortDirection: 'desc' },
          { key: 'reportAuction.auctionProductName', label: 'Auction name', sortable: true, class: 'desc' },
          { key: 'reportAuction.auctionDescription', label: 'Auction description', formatter: 'shortenAuction', sortable: true, sortDirection: 'desc', thStyle: {width: '350px'}},
          { key: 'reportUser.username', label: 'Report by:', sortable: true, sortDirection: 'desc' },
          { key: 'reportContent', label: 'Report:', sortable: true, formatter: 'shortenAuction', sortDirection: 'desc',  thStyle: {width: '350px'}},
          { key: 'actions', label: 'Actions' }

        ],

        totalRows: 1,
        totalRowsAuctions: 1,
        currentPage: 1,
        perPage: 5,
        pageOptions: [2, 5, 10, 15, { value: 100, text: "Show a lot" }],
        sortBy: '',
        sortDesc: false,
        sortDirection: 'asc',
        filter: null,
        filterOn: [],
        banModal: {
          id: 'ban-modal',
          title: '',
          content: ''
        },
        unbanModal: {
          id: 'unban-modal',
          title: '',
          content: ''
        },
        grantStaffModal: {
          id: 'grant-modal',
          title: '',
          content: ''
        },
        revokeStaffModal: {
          id: 'revoke-modal',
          title: '',
          content: ''
        },
        removeAuctionModal: {
          id: 'revoke-modal',
          title: '',
          content: ''
        },
      }
    },
    mounted: function () {
      this.getReports()

    },
    methods:{
      inforemoveAuction(item, index, button) {
        this.removeAuctionModal.title = `Delete: ${item.reportAuction.auctionProductName}`
        this.removeAuctionModal.content = JSON.stringify(item, null, 2)
        this.$root.$emit('bv::show::modal', this.removeAuctionModal.id, this.removeAuction)
      },

      info1(item, index, button) {
        this.banModal.title = `Confirm user ban: ${item.username}`
        this.banModal.content = JSON.stringify(item, null, 2)
        this.$root.$emit('bv::show::modal', this.banModal.id, this.deactivateUser)
      },

      info2(item, index, button) {
        this.unbanModal.title = `Confirm user unban: ${index}`
        this.unbanModal.content = JSON.stringify(item, null, 2)
        this.$root.$emit('bv::show::modal', this.unbanModal.id, this.activateUser)
      },

      info1_staff(item, index, button) {
        this.grantStaffModal.title = `Confirm adding to staff: ${item.username}`
        this.grantStaffModal.content = JSON.stringify(item, null, 2)
        this.$root.$emit('bv::show::modal', this.grantStaffModal.id, this.grantStaffPrivillege)
     },

      info2_staff(item, index, button) {
        this.revokeStaffModal.title = `Confirm removal from staff: ${item.username}`
        this.revokeStaffModal.content = JSON.stringify(item, null, 2)
        this.$root.$emit('bv::show::modal', this.revokeStaffModal.id, this.revokeStaffPrivilege)
      },

      resetInfoModal1() {
        this.banModal.title = ''
        this.banModal.content = ''
      },

      resetInfoModal2() {
        this.unbanModal.title = ''
        this.unbanModal.content = ''
      },

      resetInfoModal3() {
        this.grantStaffModal.title = ''
        this.grantStaffModal.content = ''
      },

      resetInfoModal4() {
        this.revokeStaffModal.title = ''
        this.revokeStaffModal.content = ''
      },

     onFiltered(filteredItems) {
       this.totalRows = filteredItems.length
       this.currentPage = 1
      },

      onFiltered2(filteredItems) {
        this.totalRowsAuctions = filteredItems.length
        this.currentPage = 1
      },

      getReports(){
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.$getToken()
          }
        };

        axios.get(`https://auctionportalbackend.herokuapp.com/api/report/getReports` , axiosConfig)
        .then(res => this.reports = res.data)
        .then(res=>{
          this.totalRowsAuctions = this.reports.length
        })
        .catch(err => console.log(err))
      },

      getUsers(){
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + this.$getToken()
          }
        };

        axios.get(`https://auctionportalbackend.herokuapp.com/api/users/getUsers` , axiosConfig)
        .then(res => this.users = res.data)
        .then(res=>{
          this.users_table = []
          for (var i in this.users){
            console.log(i)
            let tmp = {"id": this.users[i].id, "username": this.users[i].username, "is_staff": this.users[i].is_staff, "is_superuser": this.users[i].is_superuser, "is_active" : this.users[i].is_active, "email": this.users[i].email}
            this.users_table.push(tmp)
          }
          this.totalRows = this.users_table.length
        })
        .catch(err => console.log(err))
      },

      deactivateUser(user){
        var user_json = JSON.parse(user)
        const formData = new FormData();
        formData.append("user_id", user_json.id)
        formData.append("ban", "True")

        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem("user-token")
          }
        };

        axios.post(`https://auctionportalbackend.herokuapp.com/api/staff/setActivateUser/`, formData,axiosConfig)
        .then(res => console.log(res.data))
        .then(res =>{
          this.getUsers()
        })
        .catch(err => console.log(err))
      },

      activateUser(user){
        var user_json = JSON.parse(user)
        const formData = new FormData();
        formData.append("user_id", user_json.id)
        formData.append("ban", "False")
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem("user-token")
          }
        };

        axios.post(`https://auctionportalbackend.herokuapp.com/api/staff/setActivateUser/`, formData,axiosConfig)
        .then(res => console.log(res.data))
        .then(res =>{
          this.getUsers()
        })
        .catch(err => console.log(err))
      },

      grantStaffPrivillege(user){
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem("user-token")
          }
        };

        var user_json = JSON.parse(user)
        const formData = new FormData();
        formData.append("user_id", user_json.id)

        axios.post(`https://auctionportalbackend.herokuapp.com/api/staff/grantStaffStatus/`, formData, axiosConfig)
          .then(res => res.data)
          .then(res =>{
            this.getUsers()
          })
          .catch(err => console.log(err))
      },

      revokeStaffPrivilege(user){
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem("user-token")
          }
        };

        var user_json = JSON.parse(user)
        const formData = new FormData();
        formData.append("user_id", user_json.id)

        axios.post(`https://auctionportalbackend.herokuapp.com/api/staff/revokeStaffStatus/`, formData, axiosConfig)
          .then(res => res.data)
          .then(res =>{
            this.getUsers()
          })
          .catch(err => console.log(err))
      },

      goToAuction(auction){
        this.$goToAnotherPage('/auctions/' + auction.reportAuction.id)
      },

      removeAuction(auction){
        let axiosConfig = {
          headers: {
            'Authorization': 'Token ' + localStorage.getItem("user-token")
          }
        };

        var auction_json = JSON.parse(auction)
        const formData = new FormData();
        formData.append("auction_id", auction_json.reportAuction.id)

        axios.post(`https://auctionportalbackend.herokuapp.com/api/staff/deleteAuction/`, formData, axiosConfig)
          .then(res => console.log(res.data))
          .then(res =>{
            this.getReports()
          })
          .catch(err => console.log(err))
      },
      reportStringify(report){
        return JSON.stringify(report, null, 2);
      },
      parseDate(date_str){
        var date = new Date(date_str)
        return date.toTimeString();
      },
      shortenAuction(auction_str){
        if (auction_str.length < 100 )
          return auction_str;
        else {
          return auction_str.slice(0,100) + "...";
        }
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
.jumbotron-home{
    margin: 0%;
    padding: 1%;
    padding-left:0.5%;
    padding-right:0.5%;

}
* {
  box-sizing: border-box;
  /* margin: 0; */
  padding: 0;
}

.tabs {
    overflow: hidden;
  margin-left: 20px;
    margin-bottom: -2px;
}

.tabs ul {
    list-style-type: none;
    margin-left: 20px;
}

.tabs a{
    float: left;
    cursor: pointer;
    padding: 12px 24px;
    transition: background-color 0.2s;
    border: 1px solid #ccc;
    border-right: none;
    background-color: #f1f1f1;
    border-radius: 10px 10px 0 0;
    font-weight: bold;
}
.tabs a:last-child {
    border-right: 1px solid #ccc;
}

.tabs a:hover {
    background-color: #aaa;
    color: #fff;
}

.tabs a.active {
    background-color: #fff;
    color: #484848;
    border-bottom: 2px solid #fff;
    cursor: default;
}

.tabcontent {
    padding: 30px;
    border: 1px solid #ccc;
    border-radius: 10px;
  box-shadow: 3px 3px 6px #e1e1e1
}

ul.b {
  list-style-position: inside;
}

.tableWidthClass {
   max-width: 100px !important;
}


</style>
