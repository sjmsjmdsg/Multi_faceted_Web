import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '../views/Index.vue'
import Home from '../views/Home.vue'
import CVE from '../views/CVE.vue'
import CWE from '../views/CWE.vue'
import CAPEC from '../views/CAPEC.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/cve'
  },
  {
    path: '/index',
    name: 'Index',
    component: Index,
    redirect: '/cve',
    children: [
      // {
      //   path: '/home',
      //   name: 'Home',
      //   component: Home
      // },
      {
        path: '/cve',
        name: 'CVE',
        component: CVE
      },
      {
        path: '/cwe',
        name: 'CWE',
        component: CWE
      },
      {
        path: '/capec',
        name: 'CAPEC',
        component: CAPEC
      }
    ]
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  routes,
})

export default router
