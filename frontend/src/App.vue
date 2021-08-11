<template>
  <div id="app">
    <div class="panel">
      <div class="controls">
        <form action="#" @submit.prevent="getData">
          <div class="form-group">
            <button type="submit">Get data for day</button>
          </div>
        </form>

        <datepicker
          v-model="picked"
          :upperLimit="to"
          :lowerLimit="from"
          :monthHeadingFormat="outputFormat"
          :typeable="true"
        />

        <div v-show="loading">Loading...</div>
        <div v-show="errored">An error occured</div>
        <div v-show="ok">Ok</div>
      </div>

      <div class="info">
        <p>
          Run a manual sweep of anomalous airborne or electromagnetic readings.
          Radiation levels in our atmosphere have increased by 3,000 percent.
          Electromagnetic and subspace wave fronts approaching synchronization.
          What is the strength of the ship's deflector shields at maximum
          output? The wormhole's size and short period would make this a local
          phenomenon. Do you have sufficient data to compile a holographic
          simulation?
        </p>
      </div>
    </div>

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
    </div>
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
      ok: true,
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
      let time = "23:59";
      let pickedDate = moment(this.picked).format("YYYY-MM-DD").toString();
      let timeAndDate = pickedDate + " " + time;

      this.ok = false;
      this.loading = true;

      let ordTotal = `http://${this.apiUri}/orders/total/` + timeAndDate;

      let vacTotal = `http://${this.apiUri}/vaccinations/total/` + timeAndDate;

      let vacUsed = `http://${this.apiUri}/vaccinations/used/` + timeAndDate;

      let ordExp = `http://${this.apiUri}/orders/expired/` + timeAndDate;

      let vacExp = `http://${this.apiUri}/vaccinations/expired/` + timeAndDate;

      let vacLeft = `http://${this.apiUri}/vaccinations/left/` + timeAndDate;

      let vacExpTen =
        `http://${this.apiUri}/vaccinations/expiring_tendays/` + timeAndDate;

      let ordDay = `http://${this.apiUri}/orders/day/` + timeAndDate;

      let manufacturer =
        `http://${this.apiUri}/manufacturer/total/` + timeAndDate;

      let district = `http://${this.apiUri}/district/total/` + timeAndDate;

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
            this.ok = true;

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

.panel {
  padding: 5%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  max-width: 100%;
}

.controls {
  background: #dddddd;
  padding: 5%;
}

.info {
  background: #dddddd;
  padding: 5%;
  max-width: 50%;
}

.data {
  padding: 5%;
}

.charts {
  display: flex;
  flex-direction: row;
  max-width: 100%;
}

.chart-table {
  display: flex;
  flex-direction: column;
  width: 50%;
  padding: 5%;
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
