<template>
  <div id="app">
    <form action="#" @submit.prevent="getData">
      <div class="form-group">
        <input type="text" placeholder="date" v-model="date" />
      </div>
    </form>
    <div v-show="loading">Loading...</div>
    <div v-show="errored">An error occured</div>
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
          <td>{{ data[3] }}</td>
        </tr>
        <tr>
          <td>How many vaccines expired before the usage</td>
          <td>{{ data[4] }}</td>
        </tr>
        <tr>
          <td>How many vaccines are left to use</td>
          <td>{{ data[5] }}</td>
        </tr>
        <tr>
          <td>How many vaccines are going to expire in the next 10 days</td>
          <td>{{ data[6] }}</td>
        </tr>
        <tr>
          <td>How many ordes arrived on this day</td>
          <td>{{ data[7] }}</td>
        </tr>
      </table>

      <table>
        <tr>
          <th>Producer</th>
          <th>Orders</th>
          <th>Vaccines</th>
        </tr>
        <tr
          v-for="(manufacturer, index) in data[8]"
          :key="manufacturer.vaccine"
        >
          <td>{{ manufacturer.vaccine }}</td>
          <td>{{ manufacturer.count }}</td>
          <td>{{ data[9][index].sum }}</td>
        </tr>
      </table>
      <table>
        <tr>
          <th>Healthcare district</th>
          <th>Orders</th>
          <th>Vaccines</th>
        </tr>
        <tr
          v-for="(district) in data[10]"
          :key="district.healthcaredistrict"
        >
          <td>{{ district.healthcaredistrict }}</td>
          <td>{{ district.orders }}</td>
          <td>{{ district.injections }}</td>
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
      apiUri: process.env.VUE_APP_API_URI,
    };
  },
  methods: {
    getData() {
      this.loading = true;

      let ordTotal = `http://${this.apiUri}/orders/total/` + this.date;

      let vacTotal = `http://${this.apiUri}/vaccinations/total/` + this.date;

      let vacUsed = `http://${this.apiUri}/vaccinations/used/` + this.date;

      let ordExp = `http://${this.apiUri}/orders/expired/` + this.date;

      let vacExp = `http://${this.apiUri}/vaccinations/expired/` + this.date;

      let vacLeft = `http://${this.apiUri}/vaccinations/left/` + this.date;

      let vacExpTen =
        `http://${this.apiUri}/vaccinations/expiring_tendays/` + this.date;

      let ordDay = `http://${this.apiUri}/orders/day/` + this.date;

      let ordByManuf =
        `http://${this.apiUri}/orders/manufacturer/total/` + this.date;

      let vacByManuf =
        `http://${this.apiUri}/vaccinations/manufacturer/total/` + this.date;

      let district = `http://${this.apiUri}/district/total/` + this.date;

      const reqOrdTotal = axios.get(ordTotal);

      const reqVacTotal = axios.get(vacTotal);

      const reqVacUsed = axios.get(vacUsed);

      const reqOrdExp = axios.get(ordExp);

      const reqVacExp = axios.get(vacExp);

      const reqVacLeft = axios.get(vacLeft);

      const reqVacExpTen = axios.get(vacExpTen);

      const reqOrdDay = axios.get(ordDay);

      const reqOrdByManuf = axios.get(ordByManuf);

      const reqVacByManuf = axios.get(vacByManuf);

      const reqDistrict = axios.get(district);

      axios
        .all([
          reqOrdTotal,
          reqVacTotal,
          reqVacUsed,
          reqOrdExp,
          reqVacExp,
          reqVacLeft,
          reqVacExpTen,
          reqOrdDay,
          reqOrdByManuf,
          reqVacByManuf,
          reqDistrict,
        ])
        .then(
          axios.spread((...responses) => {
            this.loading = false;
            this.errored = false;

            const resOrdTotal = responses[0];

            const resVacTotal = responses[1];

            const resVacUsed = responses[2];

            const resOrdExp = responses[3];

            const resVacExp = responses[4];

            const resVacLeft = responses[5];

            const resVacExpTen = responses[6];

            const resOrdDay = responses[7];

            const resOrdByManuf = responses[8];

            const resVacByManuf = responses[9];

            const resDistrict = responses[10];

            this.data = [
              resOrdTotal.data[0].count,
              resVacTotal.data[0].sum,
              resVacUsed.data[0].sum,
              resOrdExp.data[0].count,
              resVacExp.data[0].sum,
              resVacLeft.data[0].sum,
              resVacExpTen.data[0].sum,
              resOrdDay.data[0].count,
              resOrdByManuf.data,
              resVacByManuf.data,
              resDistrict.data,
            ];
          })
        )
        .catch(() => {
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
