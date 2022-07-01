import axios from 'axios'
import qs from 'qs'
axios.defaults.timeout = 500000

//axios.defaults.baseURL = 'http://192.168.43.98:8080/videoplt'
// axios.defaults.baseURL = '192.168.31.135:8888'
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
// axios.defaults.headers.post['authorization'] = window.localStorage.getItem('token') || '';

// 报错1:has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
// 报错2：he value of the 'Access-Control-Allow-Origin' header in the response must not be the wildcard '*'
//解决跨域问题，后端springboot在对应的处理函数前加上@CrossOrigin注解，同时把这句的true改为false
axios.defaults.withCredentials = false

const http = {
  post: '',
  get: ''
}

http.post = function (api, data) {
  axios.defaults.headers.post.authorization = localStorage.getItem('token') || ''
  // console.log('authorization', localStorage.getItem('token'))
  const params = qs.stringify(data)
  return new Promise((resolve, reject) => {
    axios
      .post(api, params, { authorization: localStorage.getItem('token') || '' })
      .then(res => {
        resolve(res)
      })
      .catch(err => {
        // console.log('http./post', err.response);
        // if (err.response.status === '-1') this.$router.push('/login')
        if (err.data.code === '-1') this.$router.push('/login')
        else reject(err)
      })
  })
}

http.get = function (api, data) {
  axios.headers.post.authorization = window.localStorage.getItem('token') || ''
  const params = qs.stringify(data)
  return new Promise((resolve, reject) => {
    axios
      .get(api, params)
      .then(res => {
        // if (res.status === 401) this.$router.push('/login')
        if (res.data.code === '-1') this.$router.push('/login')
        else resolve(res)
      })
      .catch(err => {
        if (err.data.code === '-1') this.$router.push('/login')
        else reject(err)
      })
  })
}


export default http
// export const baseUrl = '192.168.31.135:8888'
// module.exports = {
//   // const baseUrl: 'http://192.168.180.18:8888/user'
// }