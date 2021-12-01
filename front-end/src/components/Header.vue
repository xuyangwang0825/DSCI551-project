<template>
  <el-card style="
          background-color: #545c64;
        ">
    <h1>{{ msg }}</h1>
  </el-card>
</template>
<script>
export default {
  name: "Header",
  data() {
    return {
      msg: "Managing ML data and models for TikTok-Like recommendation and advertising website",
      activeIndex: "1",
    };
  },
  methods: {},
};
</script>

<style scoped>
h1 {
  text-align: center;
  font-size: 20pt;
  color:aliceblue;
}
#header {
  background-color: #545c64;
  margin-left: 100px;
  min-width: 1300px;
  /* border-radius: 8px; */
  display: flex;
  flex-wrap: wrap;
  width: 90%;
  justify-content: center;
}
</style>


