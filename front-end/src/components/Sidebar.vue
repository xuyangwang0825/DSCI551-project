<template>
    <el-menu
        default-active="2"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
        <el-submenu index="1">
        <template slot="title">
            <i class="el-icon-location"></i>
            <span>Navigator One</span>
        </template>
        <el-menu-item-group title="Group One">
            <el-menu-item index="1-1">Explore Raw Data</el-menu-item>
            <el-menu-item index="1-2">item one</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="Group Two">
            <el-menu-item index="1-3">item three</el-menu-item>
        </el-menu-item-group>
        </el-submenu>
        <el-menu-item index="2">
        <i class="el-icon-menu"></i>
        <span>Navigator Two</span>
        </el-menu-item>
        <el-menu-item index="3" disabled>
        <i class="el-icon-document"></i>
        <span>Navigator Three</span>
        </el-menu-item>
        <el-menu-item index="4">
        <i class="el-icon-setting"></i>
        <span>Navigator Four</span>
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
      }
    }
  }
</script>