<template>
  <div id="Video_record_comp">
    <el-dialog
      title="ML model is predicting"
      :visible.sync="dialogTableVisible"
      :show-close="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      :close-on-click-modal="false"
      :center="true"
    >
      <el-progress :percentage="percentage"></el-progress>
      <span slot="footer" class="dialog-footer">please wait for about 3 seconds</span>
    </el-dialog>

    <div id="CT">
      <div id="info_patient">
        <!-- 卡片放置表格 -->
        <el-card style="border-radius: 8px; background-color: #545c64;">
          <div slot="header" class="clearfix">
            <div style="color: #21b3b9;">
              <span>Video Data Preview</span>
            </div>
          </div>
          <el-tabs v-model="activeName">
            <el-tab-pane label="All Data" name="first">
              <!-- 表格存放特征值 -->
              <el-table
                :data="video_info_list"
                height="600"
                border
                style="width: 1200px; text-align: center"
                v-loading="loading"
                element-loading-text="In processing, please wait with patience"
                element-loading-spinner="el-icon-loading"
                lazy
                empty-text="No Data Available"
              >
                <el-table-column label="check detail" width="200px">
                  <template slot-scope="scope">
                    <router-link :to="{path:'video_result_detail', query:{id:scope.row[0]}}">
                      click me!
                    </router-link>
                  </template>
                </el-table-column>
                <el-table-column label="name" width="200px">
                  <template slot-scope="scope">
                    <span>{{ scope.row[0] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="content-type" width="200px">
                  <template slot-scope="scope">
                    <span>{{ scope.row[2] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="content-length" width="200px">
                  <template slot-scope="scope">
                    <span>{{ scope.row[3] }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="s3-path" width="400px">
                  <template slot-scope="scope">
                    <span>{{ scope.row[1] }}</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Content",
  data() {
    return {
      server_url: "http://127.0.0.1:5003",
      activeName: "first",
      active: 0,
      centerDialogVisible: true,
      url_1: "",
      url_2: "",
      textarea: "",
      srcList: [],
      srcList1: [],
      video_info_list: [],
      feat_list: [],
      url: "",
      visible: false,
      wait_return: "waiting for uploading",
      wait_upload: "waiting for uploading",
      loading: false,
      table: false,
      isNav: false,
      showbutton: true,
      percentage: 0,
      fullscreenLoading: false,
      opacitys: {
        opacity: 0,
      },
      dialogTableVisible: false,
    };
  },
  created: function () {
    document.title = "ML managing platform";
  },
  methods: {
    true_upload() {
      this.$refs.upload.click();
    },
    true_upload2() {
      this.$refs.upload2.click();
    },
    next() {
      this.active++;
    },
    // 获得目标文件
    getObjectURL(file) {
      var url = null;
      if (window.createObjcectURL != undefined) {
        url = window.createOjcectURL(file);
      } else if (window.URL != undefined) {
        url = window.URL.createObjectURL(file);
      } else if (window.webkitURL != undefined) {
        url = window.webkitURL.createObjectURL(file);
      }
      return url;
    },
    // 上传文件
    getVideoInfo() {
      axios
        .get(this.server_url + "/get_video_info")
        .then((response) => {
          this.feat_list = Object.keys(response.data.video_info);

          for (var i = 0; i < this.feat_list.length; i++) {
            this.video_info_list.push(response.data.video_info[this.feat_list[i]]);
          }
          this.notice1();
        });
    },
    myFunc() {
      if (this.percentage + 9 < 99) {
        this.percentage = this.percentage + 9;
      } else {
        this.percentage = 99;
      }
    },
    drawChart() {},
    notice1() {
      this.$notify({
        title: "get video data complete",
        message: "",
        duration: 0,
        type: "success",
      });
    },
  },
  mounted() {
    this.getVideoInfo();
  },
};
</script>

<style>
.el-button {
  padding: 12px 20px !important;
}

#hello p {
  font-size: 15px !important;
  /*line-height: 25px;*/
}

.n1 .el-step__description {
  padding-right: 20%;
  font-size: 14px;
  line-height: 20px;
  /* font-weight: 400; */
}
</style>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.dialog_info {
  margin: 20px auto;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.box-card {
  width: 680px;
  height: 200px;
  border-radius: 8px;
  margin-top: -20px;
}

.divider {
  width: 50%;
}

#CT {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 0px;
  margin-right: 0px;
}

#CT_image_1 {
  width: 90%;
  height: 60%;
  margin: 0px auto;
  padding: 0px auto;
  margin-right: 180px;
  margin-bottom: 0px;
  border-radius: 4px;
}

#CT_image {
  margin-bottom: 60px;
  margin-left: 30px;
  margin-top: 5px;
}

.image_1 {
  width: 400px;
  height: 500px;
  background: #ffffff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.img_info_1 {
  height: 30px;
  width: 400px;
  text-align: center;
  background-color: #21b3b9;
  line-height: 30px;
}

.demo-image__preview1 {
  width: 250px;
  height: 600px;
  margin: 20px 130px;
  float: left;
}

.demo-image__preview2 {
  width: 250px;
  height: 600px;

  margin: 20px 660px;
  margin-right: 430px;
  /* background-color: green; */
}

.error {
  margin: 100px auto;
  width: 50%;
  padding: 10px;
  text-align: center;
  color: #21B3B9;
  font-size: 25px;
}

.block-sidebar {
  position: fixed;
  display: none;
  left: 50%;
  margin-left: 600px;
  top: 350px;
  width: 60px;
  z-index: 99;
}

.block-sidebar .block-sidebar-item {
  font-size: 50px;
  color: lightblue;
  text-align: center;
  line-height: 50px;
  margin-bottom: 20px;
  cursor: pointer;
  display: block;
}

div {
  display: block;
}

.block-sidebar .block-sidebar-item:hover {
  color: #187aab;
}

.download_bt {
  /* padding: 10px 16px !important; */
  margin-left: -10px;
}
#upfile {
  width: 104px;
  height: 45px;
  background-color: #187aab;
  color: #fff;
  text-align: center;
  line-height: 45px;
  border-radius: 3px;
  box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.1), 0 2px 2px 0 rgba(0, 0, 0, 0.2);
  color: #fff;
  font-family: "Source Sans Pro", Verdana, sans-serif;
  font-size: 0.875rem;
}

.file {
  width: 200px;
  height: 130px;
  position: absolute;
  left: -20px;
  top: 0;
  z-index: 1;
  -moz-opacity: 0;
  -ms-opacity: 0;
  -webkit-opacity: 0;
  opacity: 0; /*css属性&mdash;&mdash;opcity不透明度，取值0-1*/
  filter: alpha(opacity=0);
  cursor: pointer;
}

#upload {
  position: relative;
  margin: 0px 0px;
}

#Video_record_comp {
  /* width: 90%; */
  /* height: 800px; */
  /* margin: 15px auto; */
  /* display: flex; */
  margin-top: 50px;
  min-width: 1200px;
}

.divider {
  background-color: #eaeaea !important;
  height: 2px !important;
  width: 100%;
  margin-bottom: 50px;
}

.divider_1 {
  background-color: #ffffff;
  height: 2px !important;
  width: 100%;
  margin-bottom: 20px;
  margin: 20px auto;
}

.steps {
  font-family: "lucida grande", "lucida sans unicode", lucida, helvetica,
    "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
  color: #21b3b9;
  text-align: center;
  margin: 15px auto;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}

.step_1 {
  /*color: #303133 !important;*/
  margin: 20px 26px;
}

#info_patient {
  margin-top: 10px;
  margin-right: 0px;
}
</style>


