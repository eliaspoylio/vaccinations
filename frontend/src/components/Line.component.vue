<template>
  <div>
    <h3>{{ title }}</h3>
    <apexcharts
      width="100%"
      height="450"
      type="line"
      :options="chartOptions"
      :series="series"
    ></apexcharts>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "Line",
  props: { visualData: Array, title: String },
  components: {
    apexcharts: VueApexCharts,
  },
  data: function () {
    return {
      chartOptions: {
        chart: {
          id: "id",
        },
        xaxis: {
          categories: [],
        },
        colors: ["#601a4a", "#63acbe", "#ee442f"],
      },
      series: [
        {
          name: "Orders",
          data: [],
        },
        {
          name: "Injections",
          data: [],
        },
        {
          name: "Vaccinations",
          data: [],
        },
      ],
    };
  },
  watch: {
    visualData(val) {
      this.changeData(val);
    },
  },
  methods: {
    changeData(data) {
      let resKey = [];
      let resOrders = [];
      let resInjections = [];
      let resVaccinations = [];
      for (let i = 0; i < data.length; i++) {
        // key changes by request/response
        resKey[i] = data[i].day;
        resOrders[i] = data[i].orders;
        resInjections[i] = data[i].injections;
        resVaccinations[i] = data[i].vaccinations;
      }
      this.chartOptions = {
        xaxis: {
          categories: resKey,
        },
      };
      this.series = [
        {
          data: resOrders,
        },
        {
          data: resInjections,
        },
        {
          data: resVaccinations,
        },
      ];
    },
  },
};
</script>
