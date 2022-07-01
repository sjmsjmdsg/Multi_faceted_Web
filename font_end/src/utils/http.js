// 封装axios的请求，返回重新封装的数据格式
// 对错误的统一处理
import axios from 'axios'
import errorHandle from './errorHandle'
const CancelToken = axios.CancelToken

class HttpRequest {
  constructor(baseUrl) {
    this.baseUrl = baseUrl
    this.pending = {} // 对象的key为每个正在请求的接口，value为取消该接口的方法
  }
  // 获取axios配置
  getInsideConfig () {
    const config = {
      baseURL: this.baseUrl,
      headers: {
        // 'Content-Type': 'application/json;charset=utf-8'
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
      },
      timeout: 10000
    }
    return config
  }
  removePending (key, isRequest = false) {
    // 同一接口重复请求
    if (this.pending[key] && isRequest) {
      this.pending[key]('取消重复请求')
    }
    // 如果不是同一接口重复请求，则删除pending对象里该请求对应的key
    delete this.pending[key]
  }
  // 设定拦截器
  interceptors (instance) {
    // 请求拦截器
    instance.interceptors.request.use((config) => {
      // Do something before request is sent
      let key = config.url + '&' + config.method
      this.removePending(key, true)
      config.cancelToken = new CancelToken((c) => {
        this.pending[key] = c
      })
      return config
    }, (err) => {
      // debugger
      errorHandle(err)
      // Do something with request error
      return Promise.reject(err)
    })

    // 响应请求的拦截器
    instance.interceptors.response.use((res) => {
      // Any status code that lie within the range of 2xx cause this function to trigger
      // Do something with response data
      let key = res.config.url + '&' + res.config.method
      // 响应结束后删除pending对象里该请求对应的key
      this.removePending(key)
      if (res.status === 200) {
        return Promise.resolve(res.data)
      } else {
        return Promise.reject(res)
      }
    }, (err) => {
      // Any status codes that falls outside the range of 2xx cause this function to trigger
      // Do something with response error
      // debugger
      errorHandle(err)
      return Promise.reject(err)
    })
  }
  // 创建实例
  request (options) {
    const instance = axios.create()
    const newOptions = Object.assign(this.getInsideConfig(), options)
    this.interceptors(instance)
    return instance(newOptions)
  }
  get (url, config) {
    const options = Object.assign({
      method: 'get',
      url: url
    }, config)
    return this.request(options)
  }
  post (url, data) {
    return this.request({
      method: 'post',
      url: url,
      data: data
    })
  }
}

export default HttpRequest