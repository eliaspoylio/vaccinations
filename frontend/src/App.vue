<template>
  <div id="app">
    <form action="#" @submit.prevent="getData">
      <div class="form-group">
         <button type="submit">
            Get data for day
        </button>
      </div>
    </form>

    <datepicker
      v-model="picked"
      :upperLimit="to"
      :lowerLimit="from"
      :monthHeadingFormat="outputFormat"
      :typeable=true
    />

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
      <div class="charts">
        <div class="chart-table">
          <Chart :visualData="data[8]" />
          <table>
            <tr>
              <th>Producer</th>
              <th>Orders</th>
              <th>Vaccines</th>
            </tr>
            <tr v-for="manufacturer in data[8]" :key="manufacturer.vaccine">
              <td>{{ manufacturer.vaccine }}</td>
              <td>{{ manufacturer.orders }}</td>
              <td>{{ manufacturer.injections }}</td>
            </tr>
          </table>
        </div>
        <div class="chart-table">
          <Chart :visualData="data[9]" />
          <table>
            <tr>
              <th>Healthcare district</th>
              <th>Orders</th>
              <th>Vaccines</th>
            </tr>
            <tr v-for="district in data[9]" :key="district.healthcaredistrict">
              <td>{{ district.healthcaredistrict }}</td>
              <td>{{ district.orders }}</td>
              <td>{{ district.injections }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "./components/Chart.component.vue";
import Datepicker from "vue3-datepicker";
import moment from "moment";

export default {
  name: "app",
  components: { Chart, Datepicker },
  data() {
    return {
      loading: false,
      errored: false,
      date: "20210412",
      data: [],
      visualData: [],
      apiUri: process.env.VUE_APP_API_URI,
      picked: new Date(2021, 3, 12),
      to: new Date(2021, 3, 12),
      from: new Date(2021, 0, 2),
      outputFormat: "yyyy-MM-dd",
    };
  },
  methods: {
    getData() {
      let pickedDate = moment(this.picked).format("YYYY-MM-DD HH:mm:ss").toString();

      this.loading = true;

      let ordTotal = `http://${this.apiUri}/orders/total/` + pickedDate;

      let vacTotal = `http://${this.apiUri}/vaccinations/total/` + pickedDate;

      let vacUsed = `http://${this.apiUri}/vaccinations/used/` + pickedDate;

      let ordExp = `http://${this.apiUri}/orders/expired/` + pickedDate;

      let vacExp = `http://${this.apiUri}/vaccinations/expired/` + pickedDate;

      let vacLeft = `http://${this.apiUri}/vaccinations/left/` + pickedDate;

      let vacExpTen =
        `http://${this.apiUri}/vaccinations/expiring_tendays/` + pickedDate;

      let ordDay = `http://${this.apiUri}/orders/day/` + pickedDate;

      let manufacturer =
        `http://${this.apiUri}/manufacturer/total/` + pickedDate;

      let district = `http://${this.apiUri}/district/total/` + pickedDate;

      const reqOrdTotal = axios.get(ordTotal);

      const reqVacTotal = axios.get(vacTotal);

      const reqVacUsed = axios.get(vacUsed);

      const reqOrdExp = axios.get(ordExp);

      const reqVacExp = axios.get(vacExp);

      const reqVacLeft = axios.get(vacLeft);

      const reqVacExpTen = axios.get(vacExpTen);

      const reqOrdDay = axios.get(ordDay);

      const reqManufacturer = axios.get(manufacturer);

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
          reqManufacturer,
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

            const resManufacturer = responses[8];

            const resDistrict = responses[9];

            this.data = [
              resOrdTotal.data[0].count,
              resVacTotal.data[0].sum,
              resVacUsed.data[0].sum,
              resOrdExp.data[0].count,
              resVacExp.data[0].sum,
              resVacLeft.data[0].sum,
              resVacExpTen.data[0].sum,
              resOrdDay.data[0].count,
              resManufacturer.data,
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
  color: #2c3e50;
  margin-top: 60px;
}

.charts {
  display: flex;
  flex-direction: row;
  width: 100%;
}

.chart-table {
  display: flex;
  flex-direction: column;
  width: 50%;
}

.chartsrow {
  flex-direction: row;
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
