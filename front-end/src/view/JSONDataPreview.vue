<template>
  <div id="JSONDataPreview">
    <app-content></app-content>
  </div>
</template>

<script>
import JSON_data_preview from "../components/JSON_data_preview";
export default {
  data() {
    return {};
  },
  components: {
    "app-content": JSON_data_preview,
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
#JSONDataPreview{
  margin-top: 50px;
}
</style>
