<template>
  <div id="app">
    <div class="panel">
      <div class="controls">
        <form action="#" @submit.prevent="getData">
          <div class="form-group">
            <p>Date</p>
            <datepicker
              v-model="picked"
              :upperLimit="to"
              :lowerLimit="from"
              :monthHeadingFormat="outputFormat"
              :typeable="true"
            />
            <p>
              Time
              <input v-model="appt" type="time" id="appt" name="appt" />
            </p>
            <button type="submit" class="button">Update dashboard</button>
          </div>
        </form>
        <div>
          <div v-show="loading">Loading...</div>
          <div v-show="errored">An error occured</div>
          <div v-show="ok">&nbsp;</div>
        </div>
      </div>

      <div class="info">
        <h2>Vaccination dashboard</h2>
        <p>
          This dashboard displays data from
          <a href="https://github.com/solita/vaccine-exercise-2021"
            >https://github.com/solita/vaccine-exercise-2021</a
          >. The data contains information about vaccines and vaccinations.
        </p>
        <p>
          Choose a date and time and update the dashboard to view aggregate
          data.
        </p>
      </div>
    </div>

    <div class="charts">
      <div class="chart-table">
        <Chart :visualData="data[8]" :title="titles[0]" />
        <table>
          <tr>
            <th>Producer</th>
            <th>Orders</th>
            <th>Injections</th>
          </tr>
          <tr v-for="manufacturer in data[8]" :key="manufacturer.vaccine">
            <td>{{ manufacturer.vaccine }}</td>
            <td>{{ manufacturer.orders }}</td>
            <td>{{ manufacturer.injections }}</td>
          </tr>
        </table>
      </div>
      <div class="chart-table">
        <Chart :visualData="data[9]" :title="titles[1]" />
        <table>
          <tr>
            <th>Healthcare district</th>
            <th>Orders</th>
            <th>Injections</th>
          </tr>
          <tr v-for="district in data[9]" :key="district.healthcaredistrict">
            <td>{{ district.healthcaredistrict }}</td>
            <td>{{ district.orders }}</td>
            <td>{{ district.injections }}</td>
          </tr>
        </table>
      </div>
    </div>
    <div class="charts">
      <div class="chart">
        <DataTable :tableData="data" :title="titles[2]" />
      </div>
      <div class="chart">
        <Donut :visualData="data[10]" :title="titles[3]" />
      </div>
    </div>
    <div class="data">
      <Line :visualData="mountData[0]" :title="titles[4]" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "./components/Chart.component.vue";
import Line from "./components/Line.component.vue";
import Donut from "./components/Donut.component.vue";
import DataTable from "./components/DataTable.component.vue";
import Datepicker from "vue3-datepicker";
import moment from "moment";

export default {
  name: "app",
  components: { Chart, Line, Donut, DataTable, Datepicker },
  data() {
    return {
      loading: false,
      errored: false,
      ok: true,
      date: "20210412",
      data: [],
      mountData: [],
      visualData: [],
      apiUri: process.env.VUE_APP_API_URI || 'http://localhost:8080',
      picked: new Date(2021, 3, 12),
      from: new Date(),
      to: new Date(),
      outputFormat: "yyyy-MM-dd",
      appt: "23:59", // set to end of the by default so data from chosen day is taken to account
      titles: [
        "Orders and injections by manufacturer",
        "Orders and injections by healthcare district",
        "Situation on given time",
        "Gender of persons vaccinated on given day",
        "Time series of orders, injections and vaccinations",
      ],
    };
  },
  mounted() {
    let timeSeries = `${this.apiUri}/timeseries`;
    const reqTimeSeries = axios.get(timeSeries);
    axios
      .all([reqTimeSeries])
      .then(
        axios.spread((...responses) => {
          this.loading = false;
          this.errored = false;
          this.ok = true;

          const resTimeSeries = responses[0];

          this.mountData = [resTimeSeries.data];

          // set limits to date picker from time series data
          this.from = new Date(this.mountData[0][0].day);
          this.to = new Date(
            this.mountData[0][this.mountData[0].length - 1].day
          );
          this.picked = new Date(
            this.mountData[0][this.mountData[0].length - 1].day
          );
        })
      )
      .catch(() => {
        this.loading = false;
        this.errored = true;
      });
  },
  methods: {
    getData() {
      // set date to correct format and concat date and time
      let pickedDate = moment(this.picked).format("YYYY-MM-DD").toString();
      let timeAndDate = pickedDate + " " + this.appt;

      this.ok = false;
      this.loading = true;

      let ordTotal = `${this.apiUri}/orders/total/` + timeAndDate;

      let vacTotal = `${this.apiUri}/vaccinations/total/` + timeAndDate;

      let vacUsed = `${this.apiUri}/vaccinations/used/` + timeAndDate;

      let ordExp = `${this.apiUri}/orders/expired/` + timeAndDate;

      let vacExp = `${this.apiUri}/vaccinations/expired/` + timeAndDate;

      let vacLeft = `${this.apiUri}/vaccinations/left/` + timeAndDate;

      let vacExpTen =
        `${this.apiUri}/vaccinations/expiring_tendays/` + timeAndDate;

      let ordDay = `${this.apiUri}/orders/day/` + timeAndDate;

      let manufacturer = `${this.apiUri}/manufacturer/total/` + timeAndDate;

      let district = `${this.apiUri}/district/total/` + timeAndDate;

      let gender = `${this.apiUri}/gender/total/` + timeAndDate;

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

      const reqGender = axios.get(gender);

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
          reqGender,
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

            const resGender = responses[10];

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
              resGender.data,
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
body {
  background: #e9e4dc;
}

a:link,
a:visited {
  color: #ee442f;
}

a:hover,
a:active {
  color: #601a4a;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background: #f9f4ec;
}

.panel {
  padding: 2%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  max-width: 100%;
}

.controls {
  background: #e9e4dc;
  padding: 1%;
  outline-style: dotted;
  outline-color: #e9e4dc;
}

.form-group {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
}

.button {
  background-color: #63acbe;
  border: none;
  padding: 5%;
  text-align: center;
  text-decoration: none;
  font-size: 16px;
}

.info {
  background: #e9e4dc;
  padding: 2%;
  max-width: 50%;
  outline-style: dotted;
  outline-color: #e9e4dc;
}

.data {
  padding: 2%;
}

.charts {
  display: flex;
  flex-direction: row;
  max-width: 100%;
}

.chart {
  width: 50%;
  padding: 2%;
}

.chart-table {
  display: flex;
  flex-direction: column;
  width: 50%;
  padding: 2%;
}

table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td,
th {
  border: 1px solid #e9e4dc;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #e9e4dc;
}

@media only screen and (max-width: 600px) {
  .panel {
    flex-direction: column-reverse;
    padding: 2%;
  }

  .controls {
    padding: 1%;
    outline-style: none;
  }

  .info {
    max-width: 100%;
    outline-style: none;
  }

  .charts {
    flex-direction: column;
  }

  .chart-table {
    width: 100%;
  }

  .chart {
    width: 100%;
  }
}
</style>
