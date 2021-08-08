<template>
  <div class="example">
    <apexcharts
      width="100%"
      height="350"
      type="bar"
      :options="chartOptions"
      :series="series"
    ></apexcharts>
  </div>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "Chart",
  props: { districtData: Array },
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
          name: "Vaccinations total",
          data: [],
        },
      ],
    };
  },
  watch: {
    districtData(val) {
      this.changeData(val);
    },
  },
  methods: {
    changeData(districtData) {
      console.log(districtData)
      let apiDistricts = [];
      let apiOrders = [];
      let apiVaccinations = [];
      for (let i = 0; i < districtData.length; i++) {
        apiDistricts[i] = districtData[i].healthcaredistrict;
        apiOrders[i] = districtData[i].orders;
        apiVaccinations[i] = districtData[i].injections;
      }
      this.chartOptions = {
        xaxis: {
          categories: apiDistricts,
        },
      };
      this.series = [
        {
          data: apiOrders,
        },
        {
          data: apiVaccinations,
        }
      ];
    },
  },
};
</script>
