<template>
  <div>
    <h3>{{ title }}</h3>
    <apexcharts
      width="75%"
      type="donut"
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
        colors: ["#601a4a", "#ee442f", "#63acbe"],
        labels: [],
      },
      series: [],
    };
  },
  watch: {
    visualData(val) {
      this.changeData(val);
    },
  },
  methods: {
    changeData(data) {
      let resGender = [];
      let resCount = [];
      for (let i = 0; i < data.length; i++) {
        resGender[i] = data[i].gender;
        resCount[i] = data[i].count;
      }
      this.chartOptions = {
        labels: resGender,
      },
      this.series = resCount;
    },
  },
};
</script>