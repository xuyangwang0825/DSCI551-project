<template>
  <div id="UploadCSV">
    <app-content></app-content>
  </div>
</template>

<script>
import Content from "../components/Csv_content";
export default {
  data() {
    return {};
  },
  components: {
    "app-content": Content,
  },
  methods: {},
};
</script>

<style>
.el-header,
.el-footer {
  text-align: center;
  height: 100px;
}

.el-aside {
  background-color: #545c64;
  color: #333;
  text-align: center;
}

.el-main {
  background-color: #d3dce6;
  text-align: center;
}
#UploadCSV{
  margin-top: 50px;
}
</style>
