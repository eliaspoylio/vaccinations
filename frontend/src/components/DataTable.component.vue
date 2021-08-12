<template>
  <table>
    <tr>
      <td>How many orders have arrived total</td>
      <td>{{ tData[0] }}</td>
    </tr>
    <tr>
      <td>How many vaccines have arrived total</td>
      <td>{{ tData[1] }}</td>
    </tr>
    <tr>
      <td>How many of the vaccinations have been used</td>
      <td>{{ tData[2] }}</td>
    </tr>
    <tr>
      <td>How many bottles have expired</td>
      <td>{{ tData[3] }}</td>
    </tr>
    <tr>
      <td>How many vaccines expired before the usage</td>
      <td>{{ tData[4] }}</td>
    </tr>
    <tr>
      <td>How many vaccines are left to use</td>
      <td>{{ tData[5] }}</td>
    </tr>
    <tr>
      <td>How many vaccines are going to expire in the next 10 days</td>
      <td>{{ tData[6] }}</td>
    </tr>
    <tr>
      <td>How many ordes arrived on this day</td>
      <td>{{ tData[7] }}</td>
    </tr>
  </table>
</template>

<script>
export default {
  name: "Chart",
  props: { tableData: Array },
  components: {},
  data: function () {
    return {
      tData: [],
    };
  },
  watch: {
    tableData(val) {
      this.tData=val;
    },
  },
};
</script>
