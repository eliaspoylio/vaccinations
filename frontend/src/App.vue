<template>
  <div id="app">
    <form action="#" @submit.prevent="getData">
      <div class="form-group">
        <input
          type="text"
          placeholder="date"
          v-model="date"
        />
      </div>
    </form>
    <div class="alert alert-info" v-show="loading">Loading...</div>
    <div class="alert alert-danger" v-show="errored">An error occured</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "app",
  components: {
  },
  data() {
    return {
      loading: false,
      errored: false,
      date: "",
    };
  },
  methods: {
    getData() {
      console.log(this.date);
      this.loading = true;

      let injTotal = "http://localhost:8080/injections/total/" + this.date;

      let ordDay = "http://localhost:8080/orders/day/" + this.date;

      let vacUsed = "http://localhost:8080/vaccinations/used/" + this.date;

      const reqInjTotal = axios.get(injTotal);

      const reqOrdDay = axios.get(ordDay);

      const reqVacUsed = axios.get(vacUsed);

      axios
        .all([reqInjTotal, reqOrdDay, reqVacUsed])
        .then(
          axios.spread((...responses) => {
            this.loading = false;
            const respInjTotal = responses[0];

            const resOrdDay = responses[1];

            const resVacUsed = responses[2];

            console.log(respInjTotal.data[0].sum)
            console.log(resOrdDay.data[0].count)
            console.log(resVacUsed.data[0].sum)
          })
        )
        .catch((errors) => {
          console.log(errors)
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
</style>
