<template>
    <apexcharts
      width="100%"
      height="350"
      type="bar"
      :options="chartOptions"
      :series="series"
    ></apexcharts>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "Chart",
  props: { visualData: Array },
  components: {
    apexcharts: VueApexCharts,
  },
  data: function () {
    return {
      chartOptions: {
        chart: {
          id: "Healthcare district",
        },
        xaxis: {
          categories: [],
        },
      },
      series: [
        {
          name: "Orders total",
          data: [],
        },
        {
          name: "Injections total",
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
      let resVaccinations = [];
      for (let i = 0; i < data.length; i++) {
        // key changes by request/response
        resKey[i] = data[i][Object.keys(data[i])[0]];
        resOrders[i] = data[i].orders;
        resVaccinations[i] = data[i].injections;
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
          data: resVaccinations,
        }
      ];
    },
  },
};
</script>
