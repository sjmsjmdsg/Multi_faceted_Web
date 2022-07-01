import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import axios from 'axios'

// 导入全局样式表
import './assets/css/global.css'
// 引入阿里巴巴矢量图标库的下载图标
import './assets/iconfont/iconfont.css';

// 配置axios默认的请求路径
// axios.defaults.baseURL = 'http://localhost:8000'
// axios.defaults.baseURL = 'http://192.168.56.1:8888'
// axios.defaults.baseURL = 'http://192.168.56.168:8888'
// axios.defaults.baseURL = 'http://10.234.184.6:8888'
// axios.defaults.baseURL = 'http://10.249.33.7:8888'
axios.defaults.baseURL = 'http://3.25.243.122/data/'
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
axios.defaults.withCredentials = true
// 全局注册，使用方法为 this.axios
Vue.prototype.$http = axios

// 使用localfrage，安装使用 npm install localforage
import localforage from "localforage"
localforage.config({ driver: localforage.INDEXEDDB })
Vue.prototype.$localforage = localforage



Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
