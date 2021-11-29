<template>
  <div id="app">
    <el-container>
      <el-aside width="360px"><app-sidebar></app-sidebar></el-aside>
      <el-main>
        <el-header><app-header></app-header></el-header>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import Header from "./components/Header";
// import Content from "./components/Content";
import Sidebar from "./components/Sidebar";
export default {
  name: "DSCI551-project",
  data() {
    return {};
  },
  components: {
    "app-header": Header,
    // "app-content": Content,
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
