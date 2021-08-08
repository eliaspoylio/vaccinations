<template>
  <div class="example">
    <apexcharts
      width="500"
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
      //this.chartOptions.xaxis.categories = [];
      //this.series.data = [];
      let apiDistricts = [];
      let apiOrders = [];
      for (let i = 0; i < districtData.length; i++) {
        apiDistricts[i] = districtData[i].healthcaredistrict;
        apiOrders[i] = districtData[i].orders;
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
      ];
    },
  },
};
</script>
