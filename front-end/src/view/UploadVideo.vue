<template>
  <div id="uv">
    <el-container>
      <el-aside width="360px"><app-sidebar></app-sidebar></el-aside>
      <el-main>
        <el-container>
          <el-header><app-header></app-header></el-header>
          <app-content></app-content>
        </el-container>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import Header from "../components/Csv_header";
import Content from "../components/Csv_content";
import Sidebar from "../components/Sidebar";
export default {
  data() {
    return {};
  },
  components: {
    "app-header": Header,
    "app-content": Content,
    "app-sidebar": Sidebar,
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
</style>
