<template>
  <el-container class="home-container">
    <el-header>
      <el-row :gutter="10">
        <!--1.网站LOGO-->
        <el-col :xs="3" :sm="3" :md="3" :lg="3" :xl="3">
          <div style="height: 6em;width: 100%;position: relative;">
            <div style="height: 100%;width: 100%;position: absolute;top:40px;left:0;right: 0;bottom: 0;margin: auto;">
              <a style="font-family: 'Microsoft YaHei';font-size: 16px;line-height: 1.5em;color: #fafafa;">Multi-faceted</a>
              <br>
<!--              <a style="font-family: 'Microsoft YaHei';font-size: 16px;font-style:italic;line-height: 1.5;color: #f0f0f0;">-->
              <a style="font-family: 'Microsoft YaHei';font-size: 16px;line-height: 1.5em;color: #fafafa;">
                Vulnerability Search</a>
            </div>
          </div>
        </el-col>
        <!--2.搜索框与菜单-->
        <el-col :xs="16" :sm="16" :md="16" :lg="16" :xl="16">
          <div style="height: 6em;width: 100%;">
            <div style="height: 40%;width: 50%;margin-left: 1.8em;">
              <el-input size="mini" v-model="mainSearchKey" placeholder="Product, Vulnerability Type..."
                suffix-icon="el-icon-search" style="margin-top: 1em;" @blur="searchKey">
              </el-input>
            </div>
            <div style="height: 60%;width: 100%;margin-left: 1.8em;" id="main-menu">
              <el-menu default-active="/cve" class="el-menu-demo" mode="horizontal" background-color="#303133"
                text-color="#fff" active-text-color="cornflowerblue" :router="true">
                <el-menu-item index="/cve" @click="reloadPage">Home</el-menu-item>
              </el-menu>
            </div>
            <div>

            </div>
          </div>
        </el-col>
        <!--3.分享按钮-->
        <el-col :xs="5" :sm="5" :md="5" :lg="5" :xl="5">
          <div style="height: 6em;width: 100%;position: relative;">
            <div id="share-div"
              style="height: 80%;width: 100%;position: absolute;top:50%;left:0;transform: translate(0, -50%);text-align: right ;">
              <p style="margin-bottom: 0;"> <i class="iconfont
              icon-fenxiang-copy"></i>
                <i class="iconfont
              icon-tuite"></i>
                <i class="iconfont
              icon-instagram"></i>
                <i class="iconfont
              icon-ticon-facebookfacebook11
              "></i>
                <i class="iconfont
              icon-boke1
              "></i>
                <i class="iconfont
              icon-boke
              "></i></p>

              <p style="font-family: 'Microsoft YaHei';font-size: 12px;color: #d9d9d9;">
                Contact:Frank.Sun@data61.csiro.au</p>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-header>
    <el-container>
         <el-aside>


          <div id="select" style="background-color: #595959;">
            <el-select v-model="productname" placeholder="Product Name" clearable>
              <el-option v-for="item in this.productMenu" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>

            <el-select v-model="vulcomponent" collapse-tags placeholder="Vul Component" clearable>
              <el-option v-for="item in this.vulCompMenu" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>

            <el-select v-model="vultype" placeholder="Vul Type" clearable>
              <el-option v-for="item in this.vulTypeMenu" :key=" item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <el-select v-model="impact" placeholder="Impact" clearable>
              <el-option v-for="item in this.impactMenu" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <el-select v-model="vector" placeholder="Vector" clearable>
              <el-option v-for="item in this.vectorMenu" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <el-select v-model="root" placeholder="Root" clearable>
              <el-option v-for="item in this.rootMenu" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <el-select v-model="cve" placeholder="CVE" clearable>
              <el-option v-for="item in this.cveMenu" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <el-select v-model="cwe" placeholder="CWE" clearable>
              <el-option v-for="item in this.cweMenu" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <el-select v-model="capec" placeholder="CAPEC" clearable>
              <el-option v-for="item in this.capecMenu" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </div>
          <!-- <div id="brDiv">
          </div> -->
          <div id="submit">
            <el-tooltip placement="top" effect="dark" content="Submit your choices above, click here">
              <el-button type="text" @click="getNewCve">Submit</el-button>
            </el-tooltip>

          </div>
          <div id="multiChoice">
            <el-row>
              <div class="asideTag"><span>Score</span></div>
              <el-input v-model="score1" size="mini" class="scoreInput">{{score1}}</el-input>
              <span style="padding-left: 8%;padding-right: 8%;">to</span>
              <el-input v-model="score2" size="mini" class="scoreInput">{{score2}}</el-input>
            </el-row>
            <el-row>
              <div class="asideTag"><span>Severity</span></div>
              <div class="asideSmallDiv">
                <el-radio-group v-model="radio_groups['severity']" size="mini">
                  <el-radio label="LOW" @click.native.prevent="resetRadio('LOW', 'severity')">LOW&nbsp;</el-radio>
                  <el-radio label="MEDIUM" @click.native.prevent="resetRadio('MEDIUM', 'severity')">MEDIUM</el-radio>
                  <el-radio label="HIGH" @click.native.prevent="resetRadio('HIGH', 'severity')">HIGH</el-radio>
                  <el-radio label="Unknow" @click.native.prevent="resetRadio('Unknow', 'severity')">UNKNOW</el-radio>
                </el-radio-group>
              </div>
            </el-row>
            <el-row>
              <div class="asideTag"><span>Access</span></div>
              <div class="asideSmallDiv">
                <el-radio-group v-model="radio_groups['access']" size="mini">
                  <el-radio label="LOCAL" @click.native.prevent="resetRadio('LOCAL', 'access')">LOCAL</el-radio>
                  <el-radio label="REMOTE" @click.native.prevent="resetRadio('REMOTE', 'access')">REMOTE</el-radio>
                  <el-radio label="PHYSICAL" @click.native.prevent="resetRadio('PHYSICAL', 'access')">PHYSICAL</el-radio>
                  <el-radio label="CONTENT" @click.native.prevent="resetRadio('CONTENT', 'access')">CONTENT</el-radio>
                </el-radio-group>
              </div>
            </el-row>
            <el-row>
              <div class="asideTag"><span>Interaction</span></div>
              <div class="asideSmallDiv">
                <el-radio-group v-model="radio_groups['interaction']" size="mini">
                  <el-radio label="True" @click.native.prevent="resetRadio('True', 'interaction')">TRUE</el-radio>
                  <el-radio label="False" @click.native.prevent="resetRadio('False', 'interaction')">False</el-radio>
                  <el-radio label="Unknow" @click.native.prevent="resetRadio('Unknow', 'interaction')">UNKNOW</el-radio>
                </el-radio-group>
              </div>
            </el-row>
            <el-row>
              <div class="asideTag"><span>Authentication</span></div>
              <div class="asideSmallDiv">
                <el-radio-group v-model="radio_groups['authentication']" size="mini">
                  <el-radio label="MULTIPLE" @click.native.prevent="resetRadio('MULTIPLE', 'authentication')">MULTIPLE</el-radio>
                  <el-radio label="SINGLE" @click.native.prevent="resetRadio('SINGLE', 'authentication')">SINGLE</el-radio>
                  <el-radio label="NONE" @click.native.prevent="resetRadio('NONE', 'authentication')">NONE</el-radio>
                </el-radio-group>
              </div>
            </el-row>
            <el-row>
              <div class="asideTag"><span>Attack Complex</span></div>
              <div class="asideSmallDiv">
                <el-radio-group v-model="radio_groups['attackComplex']" size="mini">
                  <el-radio label="LOW" @click.native.prevent="resetRadio('LOW', 'attackComplex')">LOW&nbsp;</el-radio>
                  <el-radio label="MEDIUM" @click.native.prevent="resetRadio('MEDIUM', 'attackComplex')">MEDIUM</el-radio>
                  <el-radio label="HIGH" @click.native.prevent="resetRadio('HIGH', 'attackComplex')">HIGH</el-radio>
                  <el-radio label="Unknow" @click.native.prevent="resetRadio('Unknow', 'attackComplex')">UNKNOW</el-radio>
                </el-radio-group>
              </div>
            </el-row>
            <el-row>
              <div class="asideTag"><span>Confidentiality</span></div>
              <div class="asideSmallDiv">
                <el-radio-group v-model="radio_groups['confidentiality']" size="mini">
                  <el-radio label="NONE" @click.native.prevent="resetRadio('NONE', 'confidentiality')">NONE</el-radio>
                  <el-radio label="PARTIAL" @click.native.prevent="resetRadio('PARTIAL', 'confidentiality')">PARTIAL</el-radio>
                  <el-radio label="COMPLETE" @click.native.prevent="resetRadio('COMPLETE', 'confidentiality')">COMPLETE</el-radio>
                </el-radio-group>
              </div>
            </el-row>
            <el-row>
              <div class="asideTag"><span>Integrity</span></div>
              <div class="asideSmallDiv">
                <el-radio-group v-model="radio_groups['integrity']" size="mini">
                  <el-radio label="NONE" @click.native.prevent="resetRadio('NONE', 'integrity')">NONE</el-radio>
                  <el-radio label="PARTIAL" @click.native.prevent="resetRadio('PARTIAL', 'integrity')">PARTIAL</el-radio>
                  <el-radio label="COMPLETE" @click.native.prevent="resetRadio('COMPLETE', 'integrity')">COMPLETE</el-radio>
                </el-radio-group>
              </div>
            </el-row>
            <el-row>
              <div class="asideTag"><span>Avaliability</span></div>
              <div class="asideSmallDiv">
                <el-radio-group v-model="radio_groups['avaliability']" size="mini">
                  <el-radio label="NONE" @click.native.prevent="resetRadio('NONE', 'avaliability')">NONE</el-radio>
                  <el-radio label="PARTIAL" @click.native.prevent="resetRadio('PARTIAL', 'avaliability')">PARTIAL</el-radio>
                  <el-radio label="COMPLETE" @click.native.prevent="resetRadio('COMPLETE', 'avaliability')">COMPLETE</el-radio>
                </el-radio-group>
              </div>
            </el-row>
          </div>
          <div style="width: 100%;height: 1em;background-color:#595959 ;"></div>

        </el-aside>

        <el-main>

          <router-view></router-view>

        </el-main>
    </el-container>

    <el-footer>
      <div style="height: 1.2em;width: 100%;"></div>
      <div style="height: auto;width: 100%;">
        <el-button size="mini"><i class="iconfont icon-fenxiang"></i> Share this site</el-button>
        <el-button size="mini"><i class="iconfont icon-zhuyi"></i> Feedback</el-button>
        <el-button size="mini"><i class="iconfont icon-bangzhu"></i> FAQ</el-button>
        <el-button size="mini"><i class="iconfont icon-icon-github"></i> GitHub</el-button>
        <el-button size="mini"><i class="iconfont icon-renyuan"></i> About Us</el-button>
        <el-button size="mini"><i class="iconfont icon-yinsi"></i> Privacy</el-button>
      </div>
      <div style="height: 1em;width: 100%;"></div>
      <div style="height:auto;width: 100%;text-align: center;color: #bfbfbf;font-size: 14px;line-height: 1.5;">
        This site is developed by a volunteer team, for none-commercial use only.Support our research.<br />
        We acknowledge Aboriginal and Torres Strait Islander people as the Traditional Custodians of the land and
        acknowledge and pay respect to their Elders, past and present.<br />
        We also acknowledge the efforts of doctors, nurses, and other healthcare professionals, in fight against this
        pandemic.<br />
        The translations are still being tested. Please be aware that there may be mistranslations.
      </div>
      <div style="height: 1em;width: 100%;"></div>
<!--      <div-->
<!--        style="height: 4em;width: 100%;text-align: center;color: #f0f0f0;font-size: 14px;line-height: 1.5;position: relative;">-->
<!--        <div-->
<!--          style="background: cornflowerblue;height: 100%;width: 10%;position: absolute;top: 0;left: 0;bottom: 0;right: 0;margin: auto;">-->

<!--          <div style="width: 90%;margin-left: 5%;">-->
<!--            <i class="iconfont icon-ren"></i>-->
<!--          </div>-->
<!--          <div style="width: 90%;background-color: #595959;margin-left: 5%;">-->
<!--            <span>{{clicknum}}</span>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
      <div style="height: 1em;width: 100%;"></div>
    </el-footer>
  </el-container>
</template>

<script>
  // @ is an alias to /src
  import qs from 'qs'
  import Tools from '../utils/tools.js'
  const axios = require('axios')
  const localforage = require('localforage')

  // 引入 CVE.vue页面，以方便调用其中的方法
  import CVE from './CVE.vue'


  export default {
    name: 'index',
    components: {
      CVE
    },
    data() {
      return {
        mainSearchKey: '',  // 顶端的搜索关键词，提示用户输入产品名、漏洞类型
        lastMainSearchKey: '',  // 上次搜索的字符串，用于避免重复搜索

        score1: '', // 查询分数的起始条件
        score2: '', // 查询分数的终止条件
        severity: '', // 单选的严重程度
        access: '', // 单选的攻击途径
        interaction: '',
        authentication: '',
        attackComplex: '',
        confidentiality: '',
        integrity: '',
        avaliability: '',

        radio_groups: {'severity': '', 'access': '','interaction': '',
          'authentication': '',
          'attackComplex': '',
          'confidentiality': '',
          'integrity': '',
          'avaliability': '',},


        productMenuIni: [],
        vulTypeMenuIni: [],
        vulCompMenuIni: [],
        rootMenuIni: [],
        vectorMenuIni: [],
        impactMenuIni: [],
        cveMenuIni: [],
        cweMenuIni: [],
        capecMenuIni: [],

        menuDict: {},
        searchCVEs: [],

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
        // 选定的菜单
        productname: '',
        vulcomponent: '',
        vultype: '',
        impact: '',
        vector: '',
        root: '',
        cve: '',
        cwe: '',
        capec: '',

        // 底部栏
        clicknum: 0,
      }
    },
    create() {

    },
    mounted() {
      // console.log("*****index mounted*****")
      // var num = localStorage.getItem('clicknum')
      // // console.log('num', num)
      // if (num) {
      //   this.clicknum = num
      // } else {
      //   this.getClickNum()
      // }
      Tools.$on('setMenu', (msg) => {
        // console.log('msg',msg)
        this.setMenu(msg)
      })

      Tools.$on('setSearchCVES', (msg) => {
        // console.log('msg',msg)
        this.setSearchCVES(msg)
      })
    },
    methods: {
      resetRadio(e, group_name) {
        e === this.radio_groups[group_name] ? this.radio_groups[group_name] = '' : this.radio_groups[group_name] = e
      },

      ttt(item, key, keyPath) {
        console.log('item:', item)
        console.log('key:', key)
        console.log('keyPath:', keyPath)
      },
      reloadPage(){
        window.location.reload();
      },

      selectChange() {
        console.log('值发生改变')
        // this.getNewCve()
      },

      getClickNum() {
        console.log('*****getClickNum*****')
        var that = this
        axios.post('/common/getclicknum').then(res => {
          if (res.status == 200) {
            that.clicknum = res.data.clicknums
            localStorage.setItem('clicknum', that.clicknum)
            console.log('网站访问次数：', res.data)
          }
        }).catch(err => {
          console.log('出错！具体错误为：', err)
        })
      },

      listobject2list(targetlist) {
        var returnList = []
        for (var i=0;i<targetlist.length;i++) {
          returnList.push(targetlist[i].value)
        }
        return returnList
      },

      setSearchCVES(cveList) {
        for (var i=0;i<cveList.length;i++) {
          this.searchCVEs.push(cveList[i].cveid)
        }
      },

      setMenu(menu) {
        var that = this
        that.productMenuIni = this.listobject2list(menu.productMenu)
        that.vulTypeMenuIni = this.listobject2list(menu.vulTypeMenu)
        that.vulCompMenuIni = this.listobject2list(menu.vulCompMenu)
        that.rootMenuIni = this.listobject2list(menu.rootMenu)
        that.vectorMenuIni = this.listobject2list(menu.vectorMenu)
        that.impactMenuIni = this.listobject2list(menu.impactMenu)
        that.cveMenuIni = this.listobject2list(menu.cveMenu)
        that.cweMenuIni = this.listobject2list(menu.cweMenu)
        that.capecMenuIni = this.listobject2list(menu.capecMenu)
        that.menuDict = menu.menuDict

        that.productMenu = menu.productMenu
        that.vulTypeMenu = menu.vulTypeMenu
        that.vulCompMenu = menu.vulCompMenu
        that.rootMenu = menu.rootMenu
        that.vectorMenu = menu.vectorMenu
        that.impactMenu = menu.impactMenu
        that.cveMenu = menu.cveMenu
        that.cweMenu = menu.cweMenu
        that.capecMenu = menu.capecMenu
      },

      searchKey(inkey) {
        console.log('*****searchKey*****')

        var key = this.mainSearchKey
        console.log('关键字是：', this.mainSearchKey)
        if (key != '') {
          if (key == this.lastMainSearchKey) {
            // console.log('避免重复')
          } else {
            this.lastMainSearchKey = key
            // this.$message({
            //   message: 'Send successfully, please wait patiently for a few seconds',
            //   type: 'success',
            //   duration: 2000,
            // });

            var that = this
            axios.post('/common/searchbystr2', qs.stringify({ key: that.mainSearchKey })).then(res => {
              if (res.status == 200) {
                console.log('搜索返回的结果：', res.data)
                if (res.data == '后端获取到的searchStr为空' || res.data.searchcves.length == 0) {
                  that.$alert('No matching data has been found', 'An error occurred', {
                    confirmButtonText: 'I know',
                  });
                } else { // 有搜索结果
                  // this.$message({
                  //   message: 'Lookup successful, you are going to the detail page',
                  //   type: 'success',
                  //   duration: 3000,
                  // });

                  for (var i=0;i<res.data.searchcves.length;i++) {
                    that.searchCVEs.push(res.data.searchcves[i].cveid)
                  }
                  // 给侧边栏的菜单重新赋值
                  var menu = res.data.menu
                  that.productMenuIni = this.listobject2list(menu.productMenu)
                  that.vulTypeMenuIni = this.listobject2list(menu.vulTypeMenu)
                  that.vulCompMenuIni = this.listobject2list(menu.vulCompMenu)
                  that.rootMenuIni = this.listobject2list(menu.rootMenu)
                  that.vectorMenuIni = this.listobject2list(menu.vectorMenu)
                  that.impactMenuIni = this.listobject2list(menu.impactMenu)
                  that.cveMenuIni = this.listobject2list(menu.cveMenu)
                  that.cweMenuIni = this.listobject2list(menu.cweMenu)
                  that.capecMenuIni = this.listobject2list(menu.capecMenu)
                  that.menuDict = menu.menuDict

                  that.productMenu = menu.productMenu
                  that.vulTypeMenu = menu.vulTypeMenu
                  that.vulCompMenu = menu.vulCompMenu
                  that.rootMenu = menu.rootMenu
                  that.vectorMenu = menu.vectorMenu
                  that.impactMenu = menu.impactMenu
                  that.cveMenu = menu.cveMenu
                  that.cweMenu = menu.cweMenu
                  that.capecMenu = menu.capecMenu

                  localStorage.setItem('showAns', 'true')
                  localforage.setItem('searchAns', res.data.searchcves).then(function (v) {
                    console.log("setitem:", res.data.searchcves)
                    if (that.$route.path != '/cve') {
                      that.$router.push({ name: 'CVE' }) // 跳转页面
                    } else { // 当在CVE页面重新搜索时，重新获取数据渲染页面
                      Tools.$emit('findSearchAns', '1')
                    }
                  }).catch(function (err) {
                    // localforage.setItem('searchAns')
                    console.log(err)
                  })
                }
              }
            }).catch(err => {
              console.log('出错！具体错误为：', err)
            })
          }

        }
        else {
          this.$message({
            message: 'Your input is empty!',
            type: 'warning'
          });
        }
      },

      getNewCveNew() {
        console.log('*****getNewCveNew*****')

        var searchAnsCves = []
        var filterdCves = Set()

        localforage.getItem('searchAns').then(function (value) {
          // 当离线仓库中的值被载入时，此处代码运行
          // console.log('cve searchAns', value)
          if (value == null) {
            searchAnsCves = []
          } else {
            searchAnsCves = value
            for (var i=0;i<searchAnsCves.length;i++) {
              filterdCves.add(searchAnsCves[i].cveid)
            }

            if (this.productname != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.product[this.productname].length;i++) {
                tempset.add(this.menuDict.product[this.productname][i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.vultype != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.type[this.vultype].length;i++) {
                tempset.add(this.menuDict.type[this.vultype][i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.vulcomponent != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.component[this.vulcomponent].length;i++) {
                tempset.add(this.menuDict.component[this.vulcomponent][i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.impact != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.impact[this.impact].length;i++) {
                tempset.add(this.menuDict.impact[this.impact][i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.vector != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.vector[this.vector].length;i++) {
                tempset.add(this.menuDict.vector[this.vector][i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.root != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.root[this.root].length;i++) {
                tempset.add(this.menuDict.root[this.root][i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.cve != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.cveid[this.cve].length;i++) {
                tempset.add(this.menuDict.cveid[this.cve][i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.cwe != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.cwe[this.cwe].length;i++) {
                tempset.add(this.menuDict.cwe[this.cwe][i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.capec != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.capec[this.capec].length;i++) {
                tempset.add(this.menuDict.capec[this.capec][i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }

            if (this.severity != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.severity.length;i++) {
                tempset.add(this.menuDict.severity[i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.access != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.access.length;i++) {
                tempset.add(this.menuDict.access[i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.interaction != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.interaction.length;i++) {
                tempset.add(this.menuDict.interaction[i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.authentication != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.auth.length;i++) {
                tempset.add(this.menuDict.severity[i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.severity != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.severity.length;i++) {
                tempset.add(this.menuDict.severity[i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.severity != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.severity.length;i++) {
                tempset.add(this.menuDict.severity[i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.severity != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.severity.length;i++) {
                tempset.add(this.menuDict.severity[i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }
            if (this.severity != '') {
              var tempset = Set()
              for (var i=0;i<this.menuDict.severity.length;i++) {
                tempset.add(this.menuDict.severity[i])
              }
              var intersection = new Set([...filterdCves].filter(x => tempset.has(x)))
              filterdCves = intersection
            }

          }
        }).catch(function (err) {
          // 当出错时，此处代码运行
          console.log(err);
        })

      },


      getNewCve() { // 多条件搜索
        console.log('*****getNewCve*****')
        const formdata = new FormData() // 构造表单以提交上传的文件资质
        var searchAnsCves = []

        var transProductname = this.productname
        var transVulType = this.vultype
        var transVulComp = this.vulcomponent
        var transImpact = this.impact
        var transVector = this.vector
        var transRoot = this.root

        formdata.append('allcveids', this.searchCVEs.join(';'))

        formdata.append('productname', transProductname)
        formdata.append('vulcomponent', transVulComp)
        formdata.append('vultype', transVulType)
        formdata.append('impact', transImpact)
        formdata.append('vector', transVector)
        formdata.append('root', transRoot)

        formdata.append('score1', this.score1)
        formdata.append('score2', this.score2)
        formdata.append('severity', this.radio_groups['severity'])
        formdata.append('access', this.radio_groups['access'])
        formdata.append('interaction', this.radio_groups['interaction'])
        formdata.append('authentication', this.radio_groups['authentication'])
        formdata.append('attackComplex', this.radio_groups['attackComplex'])
        formdata.append('confidentiality', this.radio_groups['confidentiality'])
        formdata.append('integrity', this.radio_groups['integrity'])
        formdata.append('avaliability', this.radio_groups['avaliability'])

        var that = this
        // console.log('token:', token)
        axios.post('/common/getnewcve', formdata, { 'Content-Type': 'multipart/form-data', authorization: localStorage.getItem('token') || '' }
        ).then(res => {
          console.log('getNewCve 返回res：', res)
          if (res.data.findcves.length == 0) {
            that.$alert('No matching data has been found', 'An error occurred', {
              confirmButtonText: 'I know',
            });
          }
          // 给侧边栏的菜单重新赋值
          var menu = res.data.menu
          that.productMenu = menu.productMenu
          that.vulTypeMenu = menu.vulTypeMenu
          that.vulCompMenu = menu.vulCompMenu
          that.rootMenu = menu.rootMenu
          that.vectorMenu = menu.vectorMenu
          that.impactMenu = menu.impactMenu
          that.cveMenu = menu.cveMenu
          that.cweMenu = menu.cweMenu
          that.capecMenu = menu.capecMenu

          localStorage.setItem('showAns', 'true')
          localforage.setItem('searchAns', res.data.findcves).then(function (v) {
            if (that.$route.path != '/cve') {
              that.$router.push({ name: 'CVE' }) // 跳转页面
            } else { // 当在CVE页面重新搜索时，重新获取数据渲染页面
              Tools.$emit('findSearchAns', '1')
            }
          })

          // that.$message({ message: '讲师资质上传成功！', type: 'success' })
        }).catch(err => {
          console.log('getNewCve出错！具体错误为：', err)
        })



      },

      getNewCveChange() { // 多条件搜索
        console.log('*****getNewCve*****')

        this.Notification({
          title: 'Success!',
          type: 'success',
          duration: 1000,
          message: 'Submitted successfully, please be patient for a few seconds.',
          position: 'bottom-left'
        });

        const formdata = new FormData() // 构造表单以提交上传的文件资质
        var searchAnsCves = []

        localforage.getItem('searchAns').then(function (value) {
          // 当离线仓库中的值被载入时，此处代码运行
          // console.log('cve searchAns', value)
          if (value == null) {
            searchAnsCves = []
          } else {
            searchAnsCves = value
          }
        }).catch(function (err) {
          // 当出错时，此处代码运行
          console.log(err);
        })

        var cveids = []
        for (var i = 0; i < searchAnsCves.length; i++) {
          cveids.push(searchAnsCves[i]['cveid'])
        }

        formdata.append('allcveids', searchAnsCves.join(';'))

        var transProductname = this.productname != '' ? this.productname : this.productMenuIni.join(';')
        var transVulType = this.vultype != '' ? this.vultype : this.vulTypeMenuIni.join(';')
        var transVulComp = this.vulcomponent != '' ? this.vulcomponent : this.vulCompMenuIni.join(';')
        var transImpact = this.impact != '' ? this.impact : this.impactMenuIni.join(';')
        var transVector = this.vector != '' ? this.vector : this.vectorMenuIni.join(';')
        var transRoot = this.root != '' ? this.root : this.rootMenuIni.join(';')

        formdata.append('productname', transProductname)
        formdata.append('vulcomponent', transVulComp)
        formdata.append('vultype', transVulType)
        formdata.append('impact', transImpact)
        formdata.append('vector', transVector)
        formdata.append('root', transRoot)

        formdata.append('score1', this.score1)
        formdata.append('score2', this.score2)
        formdata.append('severity', this.severity)
        formdata.append('access', this.access)
        formdata.append('interaction', this.interaction)
        formdata.append('authentication', this.authentication)
        formdata.append('attackComplex', this.attackComplex)
        formdata.append('confidentiality', this.confidentiality)
        formdata.append('integrity', this.integrity)
        formdata.append('avaliability', this.avaliability)

        var that = this
        // console.log('token:', token)
        axios.post('/common/getnewcve', formdata, { 'Content-Type': 'multipart/form-data', authorization: localStorage.getItem('token') || '' }
        ).then(res => {
          console.log('getNewCve 返回res：', res)
          if (res.data.findcves.length == 0) {
            that.$alert('No matching data has been found', 'An error occurred', {
              confirmButtonText: 'I know',
            });
          }
          // 给侧边栏的菜单重新赋值
          var menu = res.data.menu
          that.productMenu = menu.productMenu
          that.vulTypeMenu = menu.vulTypeMenu
          that.vulCompMenu = menu.vulCompMenu
          that.rootMenu = menu.rootMenu
          that.vectorMenu = menu.vectorMenu
          that.impactMenu = menu.impactMenu
          that.cveMenu = menu.cveMenu
          that.cweMenu = menu.cweMenu
          that.capecMenu = menu.capecMenu

          localStorage.setItem('showAns', 'true')
          localforage.setItem('searchAns', res.data.findcves).then(function (v) {
            if (that.$route.path != '/cve') {
              that.$router.push({ name: 'CVE' }) // 跳转页面
            } else { // 当在CVE页面重新搜索时，重新获取数据渲染页面
              Tools.$emit('findSearchAns', '1')
            }
          })

          // that.$message({ message: '讲师资质上传成功！', type: 'success' })
        }).catch(err => {
          console.log('getNewCve出错！具体错误为：', err)
        })
      },

      getMenuNew() {
        console.log('*****getMenuNew*****')
        var that = this
        axios.post('/common/getmenu').then(res => {
          var js = res.data
          localforage.setItem('menudata', js)
          console.log('左侧边栏的菜单为：', res.data)
          if (res.status == 200) {
            that.productMenu = js.productMenu
            that.vulTypeMenu = js.vulTypeMenu
            that.vulCompMenu = js.vulCompMenu
            that.rootMenu = js.rootMenu
            that.vectorMenu = js.vectorMenu
            that.impactMenu = js.impactMenu
            that.cveMenu = js.cveMenu
            that.cweMenu = js.cweMenu
            that.capecMenu = js.capecMenu
          }
        }).catch(err => {
          console.log('出错！具体错误为：', err)
        })

      },


      // 将字符串按照 ; 分割，并生成 metaList
      splitStr(str, metaList) { // 将字符串按照 ; 分割，并生成 metaList
        if (metaList.length) {
          metaList.splice(0, metaList.length)//清空
        }
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
    }
  }
</script>

<style scoped>
  .home {
    background-color: gray;
  }

  .home-container {
    height: 100%;
  }

  .el-header {
    background-color: #303133;
    height: 6em !important;
  }

  .el-main {
    height: 1170px;
  }

  /* >>>.el-input__inner {
    background-color: #f0f0f0;
  } */

  >>>.el-input--mini .el-input__inner {
    height: 24px;
  }

  /* aspects menu选择框的样式 */
  >>>#select .el-input__inner {
    background-color: #595959;
    color: azure;
    border: 0px;
    font-weight: 700;
  }

  /*侧边栏提交按钮的样式*/
  >>>#submit .el-button--text {
    color: #bfbfbf;
    background-color: #303133;
  }

  #submit {
    background-color: #303133;
  }

  .el-aside {
    height: 1170px;
    background-color: #595959;
    padding: 0px;
    font-size: 0.875em;
    width:15% !important;
  }

  .el-main {
    padding: 0px;
    background-color: #fafafa;
    /* height: 100%; */
    font-size: 0.875em;
    width:85% !important;
  }

  .el-footer {
    background-color: #303133;
    height: auto !important;
    ;
  }

  >>>#main-menu .el-menu--horizontal>.el-menu-item {
    height: 3.6em;
    /* line-height: 4.375em; */
    font-size: 1em;
    font-family: fantasy;
  }

  .el-submenu {
    text-align: left;
    font-size: 0.875em;
    /* font-family: "Helvetica Neue"; */
    font-family: sans-serif;
  }

  >>>.el-submenu__title {
    height: 3em;
    line-height: 3em;
  }

  .el-submenu .el-menu-item {
    height: 36px;
    line-height: 36px;
    min-width: 0px;
    font-size: 12px;
  }

  #share-div i {
    font-size: 1em;
    /* 控制图标的大小 */
    color: #f0f0f0;
    /*控制图标的颜色*/
    margin-left: 0.5em;

  }

  .el-row {
    margin-bottom: 20px;
  }

  /* 侧边可以输入分数、严重性程度的DIV */
  #multiChoice {
    width: 100%;
    height: auto;
    background-color: #595959;
    color: #d9d9d9;
  }

  /* 调整侧边多选DIV中row之间的距离 */
  #multiChoice .el-row {
    margin-bottom: 0px;
  }

  #brDiv {
    width: 100%;
    height: 1.5em;
    background-color: #bfbfbf;
  }

  /* score输入框的样式 */
  .scoreInput {
    width: 30%;
  }

  /* 侧边可选条件的TAG样式 */
  .asideTag {
    text-align: left;
    font-weight: 700;
    color: #fafafa;
    font-size: 1em;
    line-height: 3;
  }

  .asideTag span {
    margin-left: 1.5em;
  }

  .el-radio-group {
    text-align: left;
    /* margin-left: 1.5em; */
  }

  .el-checkbox-group {
    text-align: left;
    /* margin-left: 1.5em; */
  }

  /*调整单选框内字体的大小*/
  >>>.el-radio__label {
    font-size: 12px;
    line-height: 1.5;
    color: #d9d9d9;
  }

  .asideSmallDiv {
    margin-left: 1.4em;
  }

  /* 调整底部栏按钮的样式 */
  .el-footer .el-button--mini {
    padding: 5px 7px;
  }

  .el-footer .el-button {
    background: #f0f0f0;
    border: none;
  }
</style>