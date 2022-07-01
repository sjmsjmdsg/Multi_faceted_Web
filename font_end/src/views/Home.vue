<template>
  <div class="hello">
    <div style="width: 100%;height: 1em;"></div>
    <div style="width: 90%;height:auto;margin-left: 5%;">
      <el-card shadow="never" :body-style="{ padding: '5px' }" style="height: 2.5em;">
        <div style="float: left;">
          <span>{{valueOfShowNum}} out of {{totalNum}} results&nbsp;</span>
          <el-select v-model="valueOfShowNum" clearable placeholder="请选择" size="mini">
            <el-option v-for="item in optionsOfShowNum" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
          <span>&nbsp;per page</span>
        </div>
        <div style="float:right;">
          <span>Sort by&nbsp;</span>
          <el-select v-model="valueOfSort" clearable placeholder="请选择" size="mini">
            <el-option v-for="item in optionsOfSort" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </div>
      </el-card>
    </div>

    <!--两条示例-->
    <!-- <div style="width: 90%;height:auto;margin-left: 5%;margin-top:1%">
      <el-card shadow="hover" :body-style="{ padding: '20px' }" style="height: auto;">
        <el-row>
          <div>
            <div style="float: left;font-weight: 700;font-size: 16px;">
              <span>CVE-2021-41160</span>
            </div>
            <div style="float: right;font-size: 16px;">
              <span>FreeRDP security bypass</span>
            </div>
          </div>
        </el-row>
        <el-row>
          <div style="text-align:justify;line-height: 1.5;font-size: 14px;color: #595959;" v-html="ttest">
          </div>
        </el-row>
        <el-row>
          <el-tag size="small" style="float: left;margin-right: 1em;" effect="dark">FreeRDP</el-tag>
          <el-tag size="small" style="float: left;" effect="dark">Out-of-bound write</el-tag>
          <el-tag size="small" style="float: right;" type="danger" effect="dark">8.8 High</el-tag>
        </el-row>
      </el-card>
    </div>
    <div style="width: 90%;height:auto;margin-left: 5%;margin-top:1%">
      <el-card shadow="hover" :body-style="{ padding: '20px' }" style="height: auto;">
        <el-row>
          <div>
            <div style="float: left;font-weight: 700;font-size: 16px;">
              <span>CVE-2021-41160</span>
            </div>
            <div style="float: right;font-size: 16px;">
              <span>FreeRDP security bypass</span>
            </div>
          </div>
        </el-row>
        <el-row>
          <div style="text-align:justify;line-height: 1.5;font-size: 14px;color: #595959;">
            FreeRDP is a free implementation of the Remote Desktop Protocol (RDP), released under the Apache license. In
            affected versions a malicious server might trigger out of bound writes in a connected client. Connections
            using GDI or SurfaceCommands to send graphics updates to the client might send `0` width/height or out of
            bound rectangles to trigger out of bound writes. With `0` width or heigth the memory allocation will be `0`
            but the missing bounds checks allow writing to the pointer at this (not allocated) region. This issue has
            been
            patched in FreeRDP 2.4.1.
          </div>
        </el-row>
        <el-row>
          <el-tag size="small" style="float: left;margin-right: 1em;" effect="dark">FreeRDP</el-tag>
          <el-tag size="small" style="float: left;" effect="dark">Out-of-bound write</el-tag>
          <el-tag size="small" style="float: right;" type="danger" effect="dark">8.8 High</el-tag>
        </el-row>
      </el-card>
    </div> -->


    <!--以下非示例-->
    <div style="width: 90%;height:auto;margin-left: 5%;margin-top:1%" v-for="(item,index) in this.latestCves"
      :key="index" v-loading="loading">
      <el-card shadow="hover" :body-style="{ padding: '20px' }" style="height: auto;">
        <el-row>
          <div>
            <div style="float: left;font-weight: 700;font-size: 16px;">
              <span>{{item.cveid}}</span>
            </div>
            <div style="float: right;font-size: 16px;">
              <!-- <span>{{item.title}}</span> -->
              <!-- <el-button :type="edbType" icon="el-icon-location-outline" circle size="mini" @click="gotoPage(item.urls.exploitdb_link)"></el-button>
              <el-button :type="ibmType" icon="el-icon-location" circle size="mini" @click="gotoPage(item.urls.ibm_link)></el-button>
              <el-button :type="nvdType" icon="el-icon-location-outline" circle size="mini" @click="gotoPage(item.urls.nvd_link)></el-button>
              <el-button :type="openwlType" icon="el-icon-location" circle size="mini" @click="gotoPage(item.urls.openwall_link)></el-button> -->
              <el-tooltip placement="top">
                <div slot="content">ExploitDB</div>
                <el-button v-if="item.urls.exploitdb_link!='None'" type="success" icon="el-icon-location-outline" circle
                  size="mini" @click="gotoPage(item.urls.exploitdb_link)" @mouseover.native="hover"></el-button>
                <el-button v-else type="info" icon="el-icon-location-outline" circle size="mini"
                  @click="gotoPageWarn('ExploitDB')">
                </el-button>
              </el-tooltip>

              <el-tooltip placement="top">
                <div slot="content">IBM</div>
                <el-button v-if="item.urls.ibm_link!='None'" type="success" icon="el-icon-location" circle size="mini"
                  @click="gotoPage(item.urls.ibm_link)"></el-button>
                <el-button v-else type="info" icon="el-icon-location" circle size="mini" @click="gotoPageWarn('IBM')">
                </el-button>
              </el-tooltip>

              <el-tooltip placement="top">
                <div slot="content">NVD</div>
                <el-button v-if="item.urls.nvd_link!='None'" type="success" icon="el-icon-location-outline" circle
                  size="mini" @click="gotoPage(item.urls.nvd_link)"></el-button>
                <el-button v-else type="success" icon="el-icon-location-outline" circle size="mini"
                  @click="gotoPageWarn('NVD')"></el-button>
              </el-tooltip>

              <el-tooltip placement="top">
                <div slot="content">OpenWall</div>
                <el-button v-if="item.urls.openwall_link!='None'" type="success" icon="el-icon-location" circle
                  size="mini" @click="gotoPage(item.urls.openwall_link)"></el-button>
                <el-button v-else type="info" icon="el-icon-location" circle size="mini"
                  @click="gotoPageWarn('OpenWall')">
                </el-button>
              </el-tooltip>
            </div>
          </div>
        </el-row>
        <el-row>
          <div style=" float: left;font-size: 16px;">
            <span>{{item.title}}</span>
          </div>
        </el-row>
        <el-row>
          <div style="text-align:justify;line-height: 1.5;font-size: 14px;color: #595959;" v-html="item.desc">
            <!-- {{item.desc}} -->
            <!-- {{test}} -->
            <!-- An <span class="vultype">out-of-bounds write</span> issue was addressed with improved bounds checking . -->
          </div>
        </el-row>
        <!-- <el-row>
          <el-tag size="small" style="float: left;margin-right: 1em;" effect="dark" v-if="item.component!=null">
            {{item.component}}</el-tag>
          <el-tag size="small" style="float: left;" effect="dark" v-if="item.root!=null">{{item.root}}</el-tag>
          <el-tag size="small" style="float: right;" type="danger" effect="dark" v-if="item.severity!=null">
            {{item.cvss_score}}
            {{item.severity}}
          </el-tag>
        </el-row> -->
      </el-card>
    </div>
    <!-- <div class="test" style="height: 500px;width: 500px;">
    </div> -->
  </div>
</template>

<script>
  import Index from './Index.vue'
  import Tools from '../utils/tools.js'
  import $ from 'jquery'
  const axios = require('axios')
  const localforage = require('localforage')

  export default {
    name: 'home',
    components: {
      Index
    },
    data() {
      return {
        test: 'An <span class="vultype">out-of-bounds write</span> issue was addressed with improved bounds checking .',
        ttest: " <span style='background-color:#1890ff;color:white'>FreeRDP</span> is a free implementation of the <span style='color:white;background-color:#13c2c2'>Remote Desktop Protocol (RDP)</span>, released under the <span style='color:white;background-color:#b37feb'>Apache</span> license. Inaffected versions a malicious server might trigger <span style='color:white;background-color:#73d13d'>out of bound writes in a connected client</span>. <span style='color:white;background-color:#d4b106  '>Connections using GDI or SurfaceCommands to send graphics updates to the client might send `0` width/height or out of bound rectangles to trigger out of bound writes</span>. <span style='color:white;background-color:#ff7875'>With `0` width or heigth the memory allocation will be `0` but the missing bounds checks allow writing to the pointer at this (not allocated) region</span>. This issue has been patched in FreeRDP <span style='color:white;background-color:#85a5ff'>2.4.1</span>.",
        // CVE来源按钮样式
        edbType: 'info',
        ibmType: 'info',
        nvdType: 'info',
        openwlType: 'info',

        loading: true,
        optionsOfShowNum: [{ // 每页可供选择的展示条数
          value: '5',
          label: '5'
        }, {
          value: '10',
          label: '10'
        }, {
          value: '20',
          label: '20'
        }, {
          value: '30',
          label: '30'
        }],
        valueOfShowNum: '20',
        totalNum: 0,
        optionsOfSort: [{ // 排序方式
          value: 'Relevance',
          label: 'Relevance'
        }, {
          value: 'Date',
          label: 'Date'
        }, {
          value: 'Hots',
          label: 'Hots'
        }],
        valueOfSort: 'Relevance',

        latestCves: [],

        // 菜单
        productMenu: [],
        vulTypeMenu: [],
        vulCompMenu: [],
        rootMenu: [],
        vectorMenu: [],
        impactMenu: [],
        cveMenu: [],
        cweMenu: [],
        capecMenu: [],
      }
    },
    created() {

    },
    mounted() {
      var that = this
      localforage.getItem('latestCveList').then(function (v) {
        console.log("v:", v)
        if (v == null) { // 没有找到
          console.log('重新获取or第一次获取')
          that.getLatestCve()
        } else {
          console.log('无需重新获取')
          // console.log("latestCveList:", v)
          that.loading = false
          that.latestCves = v
          that.totalNum = v.length
        }
      }).catch(function (err) {
        console.log('获取初始数据时出错：', err)
      })

      //调试用
      // this.loading = false
      // this.getLatestCve()
    },
    beforeDestroy() {

    },
    methods: {
      //获取最新的CVE数据
      getLatestCve() {
        console.log('*****getLatestCve*****')
        var that = this
        axios.post('home/cvelatest').then(res => {
          if (res.status == 200) {
            console.log("最新的CVE数据为：", res.data)
            that.latestCves = res.data
            that.totalNum = res.data.length
            localforage.setItem('latestCveList', res.data)

            that.loading = false
            setTimeout(() => {
              // 执行以下语句，将刷新Index组件中的菜单
              Tools.$emit('getMenuNew', 'msg')
            }, 2000)
            var List = []
            localforage.setItem('searchAns', List) //  searchAns存储搜索结果
          }
        }).catch(err => {
          console.log("出错！具体错误为：", err)
        })
      },

      gotoPage(url) { // 用户点击该条CVE的数据库来源时
        // console.log('url:', url)
        var url = url
        // var html = this.getHtmlByUrls()
        // document.querySelector('.test').innerHTML = html
        // this.$alert('', '标题名称', {
        //   title: '测试',
        //   confirmButtonText: '确定',
        //   dangerouslyUseHTMLString: true,
        //   callback: action => {
        //     this.$message({
        //       type: 'info',
        //       message: `action: ${action}`
        //     });
        //   }
        // })
        window.open(url)
        // this.getHtmlByUrls()
      },

      getHtmlByUrls() {
        console.log('*****getHtmlByUrls*****')
        var that = this
        axios.post('home/gethtml').then(res => {
          if (res.status == 200) {
            console.log("最新的HTML数据为：", res.data)
          }
        }).catch(err => {
          console.log("getHtmlByUrls出错！具体错误为：", err)
        })
      },


      gotoPageWarn(database) { // 当该条CVE不存在于点击的数据库中时，给出提示
        var data = database
        this.$message({
          message: 'No matching data has been found in this database: ' + data,
          type: 'warning'
        })
        // that.$message.error('没有查询到相应的数据');
      },

      // 与 CVE 页面的LearnMore 不同，点击此按钮
      learnMore(cveid) {
        console.log('home cveid', cveid)

      },

      // 将字符串按照 ; 分割，并生成 metaList
      splitStr(str, metaList) { // 将字符串按照 ; 分割，并生成 metaList
        var splchar = ';'
        var tmpList = []
        if (str) { // 字符串存在
          if (str.indexOf(splchar) == -1) { // 字符串不存在分隔符
            metaList.push(str)
          } else {
            tmpList = str.split(splchar)
            for (var i = 0; i < tmpList.length; i++) {
              metaList.push(tmpList[i])
            }
          }
        }
      },

      // 去重后再按照字母表顺序排序
      removeAndSort(arr) {
        var list = arr.sort() // 排序
        var ret = this.unique(list)
        return ret
      },

      // 字符串数组去重
      unique(arr) {
        return arr.filter(function (item, index, arr) {
          //当前元素，在原始数组中的第一个索引==当前索引值，否则返回当前元素
          return arr.indexOf(item, 0) === index
        })
      },
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .el-row {
    margin-bottom: 10px;
  }

  .vultype {
    color: aquamarine;
    font-size: 48px;
  }
</style>