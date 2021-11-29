<template>
  <el-menu
    default-active="2"
    class="el-menu-vertical-demo"
    @open="handleOpen"
    @close="handleClose"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
  >
    <el-submenu index="1">
      <template slot="title">
        <i class="el-icon-location"></i>
        <span>Exploring Data</span>
      </template>
      <el-menu-item-group title="CSV">
        <el-menu-item index="1-1">Explore Data</el-menu-item>
      </el-menu-item-group>
      <el-menu-item-group title="Video">
        <el-menu-item index="1-2">
          <router-link to="/show_video_record" >Explore Data</router-link>
        </el-menu-item>
      </el-menu-item-group>
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