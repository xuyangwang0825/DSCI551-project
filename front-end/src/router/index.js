import Vue from 'vue';
import VueRouter from 'vue-router'
import loading from '../components/loading/loading';
import App from '../App'


VueRouter.prototype.goBack = function () {
  this.isBack = true;
  window.history.go(-1);
};
Vue.use(VueRouter);

const router = new VueRouter({
    routes: [
        {path: "/App", component: App, meta: {title: "眼疾辅助诊断系统"},},
    ],
    mode: "history"
})

router.beforeEach((to, from, next) => {
  loading.show();
  next();
});

// router.afterEach(route => {
//   loading.hide();
// });

export default router;
