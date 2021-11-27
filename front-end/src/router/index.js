import Vue from 'vue';
import VueRouter from 'vue-router'
import App from '../App'


VueRouter.prototype.goBack = function () {
  this.isBack = true;
  window.history.go(-1);
};
Vue.use(VueRouter);

const router = new VueRouter({
    routes: [
        {path: "/App", component: App,},
    ],
    mode: "history"
})


export default router;
