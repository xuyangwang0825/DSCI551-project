<template>
  <el-menu
    default-active="2"
    class="el-menu-vertical-demo"
    @open="handleOpen"
    @close="handleClose"
    background-color="#ffffff"
    text-color="#40707a"
    active-text-color="#40707a"
  >
    <el-submenu index="1">
      <template slot="title">
        <i class="el-icon-location"></i>
        <span>Exploring Data</span>
      </template>
      <el-menu-item index="1-1">Explore CSV Data</el-menu-item>
      <el-menu-item index="1-2">
        <router-link to="/show_video_record" >Explore Video Data</router-link>
      </el-menu-item>
    </el-submenu>
    <el-menu-item index="2">
      <i class="el-icon-menu"></i>
      <router-link to="/upload_csv" >Upload CSV</router-link>
    </el-menu-item>
    <el-menu-item index="3">
      <i class="el-icon-setting"></i>
      <router-link to="/upload_video" >Upload Video</router-link>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  methods: {
    handleOpen(key, keyPath) {
      window.console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      window.console.log(key, keyPath);
    },
  },
};
</script>

<style scoped>
.router-link-active {
  color: #40707a;
}
a {
  text-decoration: none;
  color: #40707a;
}
</style>