<template>
  <div id="VideoRecord">
    <app-content></app-content>
  </div>
</template>

<script>
import Video_record_comp from "../components/Video_record_comp";
export default {
  data() {
    return {};
  },
  components: {
    "app-content": Video_record_comp,
  },
  methods: {},
};
</script>

<style>
  .el-header, .el-footer {
    text-align: center;
    height: 100px;
  }
  
  .el-aside {
    background-color: #545c64;
    color: #333;
    text-align: center;
  }
  
  .el-main {
    background-color: #D3DCE6;
    text-align: center;
  }
  #UploadVideo{
    margin-top: 50px;
  }
</style>
