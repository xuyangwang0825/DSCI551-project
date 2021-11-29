import Vue from 'vue';
import VueRouter from 'vue-router'
import UploadVideo from '../view/UploadVideo'
import UploadCSV from '../view/UploadCSV'
import VideoRecord from '../view/VideoRecord'
import VideoResultDetail from '../view/VideoResultDetail'
import JSONDataPreview from '../view/JSONDataPreview'

VueRouter.prototype.goBack = function () {
  this.isBack = true;
  window.history.go(-1);
};
Vue.use(VueRouter);

const router = new VueRouter({
    routes: [
        {
          path: "/",
          component: UploadVideo,
        },
        {
          path: "/upload_csv",
          component: UploadCSV,
        },
        {
          path: "/upload_video",
          component: UploadVideo,
        },
        {
          path: "/show_video_record",
          component: VideoRecord,
        },
        {
          path: "/video_result_detail",
          component: VideoResultDetail
        },
        {
          path: "/json_data_preview",
          component: JSONDataPreview
        }
    ],
    mode: "history"
})


export default router;
