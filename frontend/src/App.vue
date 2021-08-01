<template>
  <div id="app">
    <form action="#" @submit.prevent="getData">
      <div class="form-group">
        <input type="text" placeholder="date" v-model="date" />
      </div>
    </form>
    <div class="alert alert-info" v-show="loading">Loading...</div>
    <div class="alert alert-danger" v-show="errored">An error occured</div>
    <div class="data">
      <table>
        <tr>
          <td>How many orders have arrived total</td>
          <td>{{ data[0] }}</td>
        </tr>
        <tr>
          <td>How many vaccines have arrived total</td>
          <td>{{ data[1] }}</td>
        </tr>
        <tr>
          <td>How many of the vaccinations have been used</td>
          <td>{{ data[2] }}</td>
        </tr>
        <tr>
          <td>How many bottles have expired</td>
          <td></td>
        </tr>
        <tr>
          <td>How many vaccines expired before the usage</td>
          <td></td>
        </tr>
        <tr>
          <td>How many vaccines are left to use</td>
          <td></td>
        </tr>
        <tr>
          <td>How many vaccines are going to expire in the next 10 days</td>
          <td></td>
        </tr>
      </table>
      <table>
        <tr>
          <th>Producer</th>
          <th>orders</th>
          <th>vaccines</th>
        </tr>
        <tr>
          <td>Zerpfy</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Antiqua</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>SolarBuddhica</td>
          <td></td>
          <td></td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "app",
  components: {},
  data() {
    return {
      loading: false,
      errored: false,
      date: "",
      data: [],
      apiUri: process.env.VUE_APP_API_URI
    };
  },
  methods: {
    getData() {
      console.log(this.date);
      this.loading = true;


      let ordTotal = `http://${this.apiUri}/orders/total/` + this.date;

      let vacTotal = `http://${this.apiUri}/vaccinations/total/` + this.date;

      let vacUsed = `http://${this.apiUri}/vaccinations/used/` + this.date;

      let ordExp = `http://${this.apiUri}/orders/expired/` + this.date;

      let vacExp = `http://${this.apiUri}/vaccinations/expired/` + this.date;

      let vacLeft = `http://${this.apiUri}/vaccinations/left/` + this.date;

      let ordDay = `http://${this.apiUri}/orders/day/` + this.date;

      let byManuf = `http://${this.apiUri}/orders/manufacturer/total/` + this.date;

      const reqOrdTotal = axios.get(ordTotal);

      const reqVacTotal = axios.get(vacTotal);

      const reqVacUsed = axios.get(vacUsed);

      const reqOrdExp = axios.get(ordExp);

      const reqVacExp = axios.get(vacExp);

      const reqVacLeft = axios.get(vacLeft);

      const reqOrdDay = axios.get(ordDay);

      const reqByManuf = axios.get(byManuf);
      
      axios
        .all([reqOrdTotal, reqVacTotal, reqVacUsed, reqOrdExp, reqVacExp, reqVacLeft, reqOrdDay, reqByManuf])
        .then(
          axios.spread((...responses) => {
            this.loading = false;
            const respInjTotal = responses[0];

            const resOrdDay = responses[1];

            const resVacUsed = responses[2];

            this.data = [
              respInjTotal.data[0].sum,
              resOrdDay.data[0].count,
              resVacUsed.data[0].sum,
            ];
          })
        )
        .catch((errors) => {
          console.log(errors);
          this.loading = false;
          this.errored = true;
        });
    },
  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td,
th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
