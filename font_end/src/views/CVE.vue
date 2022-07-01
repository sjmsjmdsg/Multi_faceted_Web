<template>
  <div class="hello">
    <div v-show="!isLearnMore">
      <div style="width: 100%;height: 1em;"></div>
      <div style="width: 90%;height:auto;margin-left: 5%;">
        <el-card shadow="never" :body-style="{ padding: '5px' }" style="height: 2.5em;">
          <div style="float: left;">
            <span>{{valueOfShowNum}} out of {{totalNum}} results&nbsp;</span>
            <el-select v-model="valueOfShowNum" clearable placeholder="Please select" size="mini">
              <el-option v-for="item in optionsOfShowNum" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <span>&nbsp;per page</span>
          </div>
          <el-pagination
              small
              layout="prev, pager, next"
              :page-count="Math.ceil(totalNum/valueOfShowNum)" @current-change="changePages" style="float: left; margin-left:15%;">
          </el-pagination>
          <div style="float:right;">
            <span>Sort by&nbsp;</span>
            <el-select v-model="valueOfSort" clearable placeholder="Please select" size="mini">
              <el-option v-for="item in optionsOfSort" :key="item.value" :label="item.label" :value="item.value"
                :disabled="item.disabled">
              </el-option>
            </el-select>
          </div>
        </el-card>
      </div>

      <div v-loading="loadingCVE">
      <div style="width: 90%;height:auto;margin-left: 5%;margin-top:1%" v-for="(item,index) in this.searchAnsCves.slice((this.currentPage-1)*this.valueOfShowNum, this.currentPage*this.valueOfShowNum)"
        :key="index">
        <el-card shadow="hover" :body-style="{ padding: '20px' }" style="height: auto;" @cick="test()">
          <el-row>
            <div>
              <div style="float: left;font-weight: 700;font-size: 16px;">
                <span>{{item.cveid}}</span>
              </div>

              <div style="float: right;font-size: 16px;">
                <el-tooltip placement="top" style="margin-left: 5px;">
                  <div slot="content">ExploitDB</div>
                  <el-popover placement="left" width="400" trigger="click">
                    <div v-if="item.urls.exploitdb_link!='None'">测试测试测试测试</div>
                    <div v-else>Sorry, no matching data has been found in this database </div>
                    <el-button slot="reference" v-if="item.urls.exploitdb_link!='None'" type="success"
                      icon="el-icon-location-outline" circle size="mini">
                    </el-button>
                    <el-button slot="reference" v-else type="info" icon="el-icon-location-outline" circle size="mini">
                    </el-button>
                  </el-popover>
                </el-tooltip>

                <el-tooltip placement="top" style="margin-left: 5px;">
                  <div slot="content">IBM</div>
                  <el-popover placement="left" width="400" trigger="click">
                    <div v-if="item.urls.ibm_link!='None'">测试测试测试测试</div>
                    <div v-else>Sorry, no matching data has been found in this database </div>
                    <!-- <el-button v-if="item.urls.ibm_link!='None'" type="success" icon="el-icon-location" circle size="mini"
                    @click="gotoPage(item.urls.ibm_link,'IBM')"></el-button> -->
                    <el-button slot="reference" v-if="item.urls.ibm_link!='None'" type="success" icon="el-icon-location"
                      circle size="mini"></el-button>
                    <el-button slot="reference" v-else type="info" icon="el-icon-location" circle size="mini">
                    </el-button>
                  </el-popover>
                </el-tooltip>

                <el-tooltip placement="top" style="margin-left: 5px;">
                  <div slot="content">NVD</div>
                  <el-popover placement="left" width="400" trigger="click">
                    <div v-if="item.urls.nvd_link!='None'">测试测试测试测试</div>
                    <div v-else>Sorry, no matching data has been found in this database </div>
                    <!-- <el-button slot="reference">click 激活</el-button> -->
                    <el-button slot="reference" v-if="item.urls.nvd_link!='None'" type="success"
                      icon="el-icon-location-outline" circle size="mini">
                    </el-button>
                    <el-button slot="reference" v-else type="success" icon="el-icon-location-outline" circle
                      size="mini"></el-button>
                  </el-popover>
                </el-tooltip>


                <el-tooltip placement="top" style="margin-left: 5px;">
                  <div slot="content">OpenWall</div>
                  <el-popover placement="left" width="400" trigger="click">
                    <div v-if="item.urls.openwall_link!='None'">测试测试测试测试</div>
                    <div v-else>Sorry, no matching data has been found in this database </div>
                    <!-- <el-button v-if="item.urls.openwall_link!='None'" type="success" icon="el-icon-location" circle
                    size="mini" @click="gotoPage(item.urls.openwall_link,'OpenWall')"></el-button> -->
                    <el-button slot="reference" v-if="item.urls.openwall_link!='None'" type="success"
                      icon="el-icon-location" circle size="mini"></el-button>
                    <el-button slot="reference" v-else type="info" icon="el-icon-location" circle size="mini">
                    </el-button>
                  </el-popover>
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
            </div>
          </el-row>

          <el-row style="margin-bottom: 0;">
            <el-button type="text" style="float: right;" @click="learnMore(item.cveid)"><span
                style="font-size: 12px;">>>Learn
                More</span>
            </el-button>
          </el-row>
        </el-card>
      </div>
    </div>
    </div>

    <div style="height: 1.6em;margin-left: 5%;margin-top: 1%;width: 90%;" v-show="isLearnMore">
      <el-button type="text" style="float: left;" @click="gotoCveList">
        << back</el-button>
          <el-button type="text" style="float: right;" @click="gotoNextCve" v-if='this.searchAnsCves.length>1'>next >>
          </el-button>
    </div>

    <!--点击 learn more 后可查看该条记录的详细信息-->
    <div v-show="isLearnMore" style="margin-left: 5%;margin-top: 1%;width: 90%;">
      <el-tabs type="border-card" @tab-click="shiftTab">
        <el-tab-pane label="Content">
          <el-row>
            <div>
              <div style="float: left;font-weight: 700;font-size: 16px;">
                <span>{{this.selectCve.cveid}}</span>
              </div>
              <div style="float: right;font-size: 16px;">
                <span>{{this.selectCve.title}}</span>
              </div>
            </div>
          </el-row>

          <el-row class="contentTags">
            Description:
          </el-row>
          <el-row>
            <div
              style="text-align:justify;line-height: 1.5;font-size: 14px;color: #595959;margin-left:2%;margin-right: 2%;"
              v-html="this.selectCve.desc">
              <!-- {{this.selectCve.desc}} -->
            </div>
          </el-row>

          <el-row class="contentTags">
            Basic:
          </el-row>
          <el-row class="aloneRow">
            <el-col :span="12">
              <span class="miniContentTags">-Publish Date: </span><span
                class="text">{{this.selectCve.publish_date}}</span>
            </el-col>
            <el-col :span="12">
              <span class="miniContentTags">-CWE: </span><span>{{this.selectCve.cwe}}</span>
            </el-col>
          </el-row>

          <el-row class="contentTags">
            Vulnerability Matrix:
          </el-row>
          <el-row class="aloneRow">
            <span class="miniContentTags">-CVSS 2.0: </span><span class="text">{{this.selectCve.cvss_score}}
              {{this.selectCve.severity}}</span>
          </el-row>
          <el-row class="aloneRow">
            <el-col :span="12">
              <span class="miniContentTags">-Access Vector: </span><span class="text">{{this.selectCve.access}}</span>
            </el-col>
            <el-col :span="12">
              <span class="miniContentTags">-Confidentiality Impact:
              </span><span>{{this.selectCve.impact_confidence}}</span>
            </el-col>
          </el-row>
          <el-row class="aloneRow">
            <el-col :span="12">
              <span class="miniContentTags">-Access Complexity: </span><span
                class="text">{{this.selectCve.attack_complex}}</span>
            </el-col>
            <el-col :span="12">
              <span class="miniContentTags">-Integrity Impact:
              </span><span>{{this.selectCve.impact_integer}}</span>
            </el-col>
          </el-row>
          <el-row class="aloneRow">
            <el-col :span="12">
              <span class="miniContentTags">-Authentication: </span><span class="text">{{this.selectCve.auth}}</span>
            </el-col>
            <el-col :span="12">
              <span class="miniContentTags">-Availability Imapct:
              </span><span>{{this.selectCve.impact_available}}</span>
            </el-col>
          </el-row>

          <el-row class="contentTags">
            Vulnerability Key Aspects:
          </el-row>
          <el-row class="aloneRow">
            <span class="miniContentTags">-Product: </span><span class="text">{{this.selectCve.product}}</span>
          </el-row>
          <el-row class="aloneRow">
            <span class="miniContentTags">-Version: </span><span class="text">{{this.selectCve.version}}</span>
          </el-row>
          <el-row class="aloneRow">
            <span class="miniContentTags">-Vulnerability component: </span><span>{{this.selectCve.component}}</span>
          </el-row>
          <el-row class="aloneRow">
            <span class="miniContentTags">-Vulnerability Type: </span><span>{{this.selectCve.type}}</span>
          </el-row>
          <el-row class="aloneRow">
            <span class="miniContentTags">-Root Cause: </span><span>{{this.selectCve.root}}</span>
          </el-row>
          <el-row class="aloneRow">
            <span class="miniContentTags">-Attack Vector: </span><span>{{this.selectCve.vector}}</span>
          </el-row>
          <el-row class="aloneRow">
            <span class="miniContentTags">-Impact: </span><span>{{this.selectCve.impact}}</span>
          </el-row>
        </el-tab-pane>


        <!--Dashboard绘图页面-->
        <el-tab-pane label="Dashboard">
          <el-tabs v-model="dashboard">
            <el-tab-pane label="Product" name="0">
              <el-row class="dashAloneRow">
                <span class="miniContentTags">Product: </span>
                <el-select v-model="productChoice" placeholder="请选择" clearable size="mini" @change="getPictures">
                  <!-- <el-option v-for="item in optionsOfProduct" :key="item.value" :label="item.label" :value="item.value">
                  </el-option> -->
                  <el-option-group v-for="group in optionsOfProduct" :key="group.label" :label="group.label">
                    <el-option v-for="item in group.options" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                  </el-option-group>
                </el-select>
              </el-row>
              <div style="height: 1em;">
              </div>
              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                  Most Frequent Version
                  </span>
                  <div id="MostFrequentVersion" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Type
                  </span>
                  <div id="MostFrequentVulType" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Component
                  </span>
                  <div id="MostFrequentVulComp" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

              </el-row>


              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Root
                  </span>
                  <div id="MostFrequentRoot" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Vector
                  </span>
                  <div id="MostFrequentVector" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Impact
                  </span>
                  <div id="MostFrequentImpact" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

              </el-row>


              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="Severity" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="Access" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="Interaction" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="Auth" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="AttackComplex" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactConfidence" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="ImpactInteger" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactAvailable" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="PublishDate" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row>
                <el-divider></el-divider>
              </el-row>

              <el-row>
                <div id="TimeLine" class="rectangle" v-loading="loading">
                </div>
              </el-row>

              <el-row>
                <div id="C3BMIndex" class="rectangle" v-loading="loading">
                </div>
              </el-row>
            </el-tab-pane>

            <el-tab-pane label="Version" name="1">
              <el-row class="dashAloneRow">
                <span class="miniContentTags">Version: </span>
                <el-select v-model="versionChoice" placeholder="请选择" clearable size="mini" @change="getPictures">

                  <el-option v-for="item in optionsOfVersion" :key="item" :label="item" :value="item">
                  </el-option>
                </el-select>
              </el-row>
              <div style="height: 1em;">
              </div>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                  Most Frequent Product
                </span>
                  <div id="MostFrequentProductOfVersion" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Type
                  </span>
                  <div id="MostFrequentVulTypeOfVersion" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Component
                  </span>
                  <div id="MostFrequentVulCompOfVersion" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Root
                  </span>
                  <div id="MostFrequentRootOfVersion" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Vector
                  </span>
                  <div id="MostFrequentVectorOfVersion" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Impact
                  </span>
                  <div id="MostFrequentImpactOfVersion" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="SeverityVersion" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="AccessVersion" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="InteractionVersion" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="AuthVersion" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="AttackComplexVersion" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactConfidenceVersion" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="ImpactIntegerVersion" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactAvailableVersion" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="PublishDateVersion" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row>
                <el-divider></el-divider>
              </el-row>

              <el-row>
                <div id="TimeLineVersion" class="rectangle" v-loading="loading">
                </div>
              </el-row>

              <el-row>
                <div id="C3BMIndexVersion" class="rectangle" v-loading="loading">
                </div>
              </el-row>
            </el-tab-pane>

            <el-tab-pane label="VulComp" name="3">
              <el-row class="dashAloneRow">
                <span class="miniContentTags">Vulnerability Component: </span>
                <el-select v-model="vulcompChoice" placeholder="请选择" clearable size="mini" @change="getPictures">

                  <el-option v-for="item in optionsOfComp" :key="item" :label="item" :value="item">
                  </el-option>
                </el-select>
              </el-row>
              <div style="height: 1em;">
              </div>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                  Most Frequent Product
                </span>
                  <div id="MostFrequentProductOfComp" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Version
                  </span>
                  <div id="MostFrequentVersionOfComp" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Type
                  </span>
                  <div id="MostFrequentVulTypeOfComp" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Root
                  </span>
                  <div id="MostFrequentRootOfComp" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Vector
                  </span>
                  <div id="MostFrequentVectorOfComp" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Impact
                  </span>
                  <div id="MostFrequentImpactOfComp" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>


              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="SeverityComp" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="AccessComp" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="InteractionComp" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="AuthComp" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="AttackComplexComp" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactConfidenceComp" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="ImpactIntegerComp" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactAvailableComp" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="PublishDateComp" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row>
                <el-divider></el-divider>
              </el-row>

              <el-row>
                <div id="TimeLineComp" class="rectangle" v-loading="loading">
                </div>
              </el-row>

              <el-row>
                <div id="C3BMIndexComp" class="rectangle" v-loading="loading">
                </div>
              </el-row>
            </el-tab-pane>

            <el-tab-pane label="VulType" name="2">
              <el-row class="dashAloneRow">
                <span class="miniContentTags">Vulnerability Type: </span>
                <el-select v-model="vultypeChoice" placeholder="请选择" clearable size="mini" @change="getPictures">

                  <el-option v-for="item in optionsOfType" :key="item" :label="item" :value="item">
                  </el-option>
                </el-select>
              </el-row>
              <div style="height: 1em;">
              </div>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                  Most Frequent Product
                </span>
                  <div id="MostFrequentProductOfType" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Version
                  </span>
                  <div id="MostFrequentVersionOfType" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Component
                  </span>
                  <div id="MostFrequentVulCompOfType" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Root
                  </span>
                  <div id="MostFrequentRootOfType" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Vector
                  </span>
                  <div id="MostFrequentVectorOfType" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Impact
                  </span>
                  <div id="MostFrequentImpactOfType" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="SeverityType" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="AccessType" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="InteractionType" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="AuthType" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="AttackComplexType" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactConfidenceType" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="ImpactIntegerType" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactAvailableType" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="PublishDateType" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row>
                <el-divider></el-divider>
              </el-row>

              <el-row>
                <div id="TimeLineType" class="rectangle" v-loading="loading">
                </div>
              </el-row>

              <el-row>
                <div id="C3BMIndexType" class="rectangle" v-loading="loading">
                </div>
              </el-row>
            </el-tab-pane>

            <el-tab-pane label="Root" name="4">
              <el-row class="dashAloneRow">
                <span class="miniContentTags">Root: </span>
                <el-select v-model="rootChoice" placeholder="请选择" clearable size="mini" @change="getPictures">

                  <el-option v-for="item in optionsOfRoot" :key="item" :label="item" :value="item">
                  </el-option>
                </el-select>
              </el-row>
              <div style="height: 1em;">
              </div>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                  Most Frequent Product
                </span>
                  <div id="MostFrequentProductOfRoot" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Version
                  </span>
                  <div id="MostFrequentVersionOfRoot" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Type
                  </span>
                  <div id="MostFrequentVulTypeOfRoot" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Component
                  </span>
                  <div id="MostFrequentVulCompOfRoot" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Vector
                  </span>
                  <div id="MostFrequentVectorOfRoot" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Impact
                  </span>
                  <div id="MostFrequentImpactOfRoot" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="SeverityRoot" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="AccessRoot" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="InteractionRoot" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="AuthRoot" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="AttackComplexRoot" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactConfidenceRoot" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="ImpactIntegerRoot" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactAvailableRoot" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="PublishDateRoot" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row>
                <el-divider></el-divider>
              </el-row>

              <el-row>
                <div id="TimeLineRoot" class="rectangle" v-loading="loading">
                </div>
              </el-row>

              <el-row>
                <div id="C3BMIndexRoot" class="rectangle" v-loading="loading">
                </div>
              </el-row>
            </el-tab-pane>

            <el-tab-pane label="Vector" name="5">
              <el-row class="dashAloneRow">
                <span class="miniContentTags">Vector: </span>
                <el-select v-model="vectorChoice" placeholder="请选择" clearable size="mini" @change="getPictures">

                  <el-option v-for="item in optionsOfVector" :key="item" :label="item" :value="item">
                  </el-option>
                </el-select>
              </el-row>
              <div style="height: 1em;">
              </div>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                  Most Frequent Product
                </span>
                  <div id="MostFrequentProductOfVector" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Version
                  </span>
                  <div id="MostFrequentVersionOfVector" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Type
                  </span>
                  <div id="MostFrequentVulTypeOfVector" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Component
                  </span>
                  <div id="MostFrequentVulCompOfVector" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Root
                  </span>
                  <div id="MostFrequentRootOfVector" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Impact
                  </span>
                  <div id="MostFrequentImpactOfVector" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="SeverityVector" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="AccessVector" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="InteractionVector" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="AuthVector" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="AttackComplexVector" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactConfidenceVector" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <div id="ImpactIntegerVector" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="ImpactAvailableVector" class="square" v-loading="loading">
                  </div>
                </el-col>
                <el-col :span="8">
                  <div id="PublishDateVector" class="square" v-loading="loading">
                  </div>
                </el-col>
              </el-row>

              <el-row>
                <el-divider></el-divider>
              </el-row>

              <el-row>
                <div id="TimeLineVector" class="rectangle" v-loading="loading">
                </div>
              </el-row>

              <el-row>
                <div id="C3BMIndexVector" class="rectangle" v-loading="loading">
                </div>
              </el-row>
            </el-tab-pane>

            <el-tab-pane label="Impact" name="6">
              <el-row class="dashAloneRow">
                <span class="miniContentTags">Impact: </span>
                <el-select v-model="impactChoice" placeholder="请选择" clearable size="mini" @change="getPictures">

                  <el-option v-for="item in optionsOfImpact" :key="item" :label="item" :value="item">
                  </el-option>
                </el-select>
              </el-row>
              <div style="height: 1em;">
              </div>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                  Most Frequent Product
                </span>
                  <div id="MostFrequentProductOfImpact" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Version
                  </span>
                  <div id="MostFrequentVersionOfImpact" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Type
                  </span>
                  <div id="MostFrequentVulTypeOfImpact" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Component
                  </span>
                  <div id="MostFrequentVulCompOfImpact" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Root
                  </span>
                  <div id="MostFrequentRootOfImpact" class="square" v-loading="loadingChart">
                  </div>
                </el-col>

                <el-col :span="8">
                  <span class="miniContentTags">
                    Most Frequent Vector
                  </span>
                  <div id="MostFrequentVectorOfImpact" class="square" v-loading="loadingChart">
                  </div>
                </el-col>
              </el-row>
            </el-tab-pane>
          </el-tabs>

          <el-row :gutter="20">
            <el-col :span="8">
              <div id="SeverityImpact" class="square" v-loading="loading">
              </div>
            </el-col>
            <el-col :span="8">
              <div id="AccessImpact" class="square" v-loading="loading">
              </div>
            </el-col>
            <el-col :span="8">
              <div id="InteractionImpact" class="square" v-loading="loading">
              </div>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="8">
              <div id="AuthImpact" class="square" v-loading="loading">
              </div>
            </el-col>
            <el-col :span="8">
              <div id="AttackComplexImpact" class="square" v-loading="loading">
              </div>
            </el-col>
            <el-col :span="8">
              <div id="ImpactConfidenceImpact" class="square" v-loading="loading">
              </div>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="8">
              <div id="ImpactIntegerImpact" class="square" v-loading="loading">
              </div>
            </el-col>
            <el-col :span="8">
              <div id="ImpactAvailableImpact" class="square" v-loading="loading">
              </div>
            </el-col>
            <el-col :span="8">
              <div id="PublishDateImpact" class="square" v-loading="loading">
              </div>
            </el-col>
          </el-row>

          <el-row>
            <el-divider></el-divider>
          </el-row>

          <el-row>
            <div id="TimeLineImpact" class="rectangle" v-loading="loading">
            </div>
          </el-row>

          <el-row>
            <div id="C3BMIndexImpact" class="rectangle" v-loading="loading">
            </div>
          </el-row>
        </el-tab-pane>

        <!--数据库aspect对比-->
        <el-tab-pane label="Compare">
          <el-table :data="tableData" style="width: 100%" v-loading="loadingForTable">
            <el-table-column prop="database" label="Database" width="100">
            </el-table-column>
            <el-table-column label="Vulnerability Aspects">
              <el-table-column prop="product" label="Vulnerable Product" width="150">
              </el-table-column>
              <el-table-column prop="version" label="Vulnerable Version" width="150">
              </el-table-column>
              <el-table-column prop="component" label="Vulnerable Component" width="180">
              </el-table-column>
              <el-table-column prop="type" label="Vulnerable Type" width="150">
              </el-table-column>
              <el-table-column prop="root" label="Root Cause" width="120">
              </el-table-column>
              <el-table-column prop="vector" label="Attack Vector" width="120">
              </el-table-column>
              <el-table-column prop="impact" label="Imapct" width="120">
              </el-table-column>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
      <el-button type="text" style="float: left;" @click="gotoCveList">
        << back</el-button>
          <el-button type="text" style="float: right;" @click="gotoNextCve" v-if='this.searchAnsCves.length>1'>next
            >>
          </el-button>
    </div>

  </div>
</template>

<script>
  const axios = require('axios')
  import Tools from '../utils/tools.js'
  const localforage = require('localforage')
  import qs from 'qs'
  import $ from 'jquery'

  // import localforage from 'localforage'
  import * as echarts from 'echarts'
  import 'echarts-wordcloud'

  window.jQuery = $
  window.$ = $

  export default {
    data() {
      return {

        showAns: false, // 是否有搜索结果可展示

        searchAnsCves: [], // 搜索返回的结果
        selectCve: {
          'access': '',
          'attack_complex': '',
          'auth': '',
          'capec': '',
          'component': null,
          'cveid': '',
          'cvss_score': '',
          'cwe': '',
          'desc': '',
          'exploit_signture': '',
          'id': '',
          'impact': '',
          'impact_available': '',
          'impact_confidence': '',
          'impact_integer': '',
          'interaction': '',
          'product': '',
          'publish_date': '',
          'remedy': '',
          'root': null,
          'severity': null,
          'title': '',
          'type': '',
          'vector': '',
          'version': ''
        }, // 当前选中CVE
        selectId: 0, // 当前选中CVE的cveid
        isLearnMore: false, // 是否进入该条CVE的详情页面
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
        currentPage: 1,
        totalNum: 0,
        optionsOfSort: [{ // 排序方式
          value: 'Relevance',
          label: 'Relevance'
        }],
        valueOfSort: 'Relevance',
        tab: 0, // content和dashboard切换是是否显示下方的next和back
        dashboard: '0', // Dashboard标签页内选择的页面


        optionsOfAspect: [
            '',
            'OfVersion',
            'OfType',
            'OfComp',
            'OfRoot',
            'OfVector',
            'OfImpact'
        ],

        optionOfBar:[
          '',
          'Version',
          'Type',
          'Comp',
          'Root',
          'Vector',
          'Impact'
        ],

        optionsOfAspectType: ['product', 'version', 'vultype', 'vulcomp', 'root', 'vector', 'impact'],

        /*以下为dashboard子页面下的选项*/
        optionsOfProduct: [ // 选择要展示饼图的product，每一个元素的格式为{value:'选项1',label:'黄金糕'}
          {
            label: '1st',
            options: []
          }, {
            label: '2nd',
            options: []
          }
        ],
        productChoice: '',
        versionChoice:'',
        vultypeChoice:'',
        vulcompChoice:'',
        rootChoice:'',
        vectorChoice:'',
        impactChoice:'',
        versionOfproducts: [], // 根据version筛选出的products
        optionsOfVersion: [],
        optionsOfType: [],
        optionsOfComp: [],
        optionsOfRoot: [],
        optionsOfVector: [],
        optionsOfImpact: [],

        /*以下为饼图绘图实例*/
        productChart:null,
        versionChart: null,
        typeChart: null,
        vulCompChart: null,
        rootChart: null,
        vectorChart: null,
        impactChart: null,
        /*以下为饼图绘图数据*/
        productList: [],
        productS: 1,
        versionList: [],
        versionS: 1,
        typeList: [],
        typeS: 1,  // 是否有数据可以绘制，默认有
        typeListX: [],
        typeListY: [],
        vulCompList: [],
        vulCompS: 1,
        vulCompListX: [],
        vulCompListY: [],
        rootList: [],
        rootS: 1,
        rootListX: [],
        rootListY: [],
        vectorList: [],
        vectorS: 1,
        vectorListX: [],
        vectorListY: [],
        impactList: [],
        impactS: 1,
        impactListX: [],
        impactListY: [],
        loadingChart: false,


        // 柱状图加载
        loading: false,
        /*以下为柱状图绘图实例*/
        severityChart: null,
        accessChart: null,
        interactionChart: null,
        authChart: null,
        attackComplexChart: null,
        impactConfidenceChart: null,
        impactIntegerChart: null,
        impactAvailableChart: null,
        publishDateChart: null,
        /*以下为柱状图绘图数据*/
        severityX: [],
        severityData: [],
        accessX: [],
        accessData: [],
        interactX: [],
        interactData: [],
        authX: [],
        authData: [],
        attackComplexX: [],
        attackComplexData: [],
        impactConfidenceX: [],
        impactConfidenceData: [],
        impactIntegerX: [],
        impactIntegerData: [],
        impactAvailableX: [],
        impactAvailableData: [],
        publishDateX: [],
        publishDateData: [],

        /*以下为折线图绘图实例*/
        timeLineChart: null,
        c3bIndexChart: null,
        /*以下为折线图绘图数据*/
        timeLineX: [],
        timeLineData: [],
        c3bmX: [],
        c3bmData: [],


        /*3、数据库aspect对比*/
        tableData: [], // 表格渲染数据
        loadingForTable: false,

        edbType: 'info',
        ibmType: 'info',
        nvdType: 'info',
        openwlType: 'info',


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
        loadingCVE: false
      }
    },
    mounted() {
      console.log('cve mounted')
      // var show = localStorage.getItem('showAns')
      // if (show == 'true') { // 有搜索结果
      //   this.showAns = true
      //   this.findSearchAns()
      // } else {
      //   this.findLastCves()
      // }
      this.findLastCves()
      Tools.$on('findSearchAns', (msg) => {
        // console.log('msg',msg)
        this.findSearchAns()
        this.showAns = true
      })

      // this.MostFrequentVersion();
      // this.MostFrequentVulType();
      // this.MostFrequentVulComp();
      // this.MostFrequentRoot();
      // this.MostFrequentVector();
      // this.MostFrequentImpact();
      // this.Severity();
      // this.Access();
      // this.Interaction();
      //
      // this.TimeLine();
      // this.C3BMIndex();
    },
    methods: {
      changePages(value) {
        this.currentPage=value
      },

      findLastCves() {
        console.log('*****findLastCves*****')
        var that = this
        that.loadingCVE = true
        localforage.getItem('latestCveList').then(function (v) {
          console.log("v:", v)
          if (v == null) { // 没有找到
            console.log('重新获取or第一次获取')
            that.getLatestCve()
          } else {
            that.loadingCVE = false
            that.searchAnsCves = v
            that.totalNum = v.length
            Tools.$emit('setSearchCVES', v)
            localforage.getItem('latestCveMenu').then(function (v1) {
              if (v1 == null) {
                that.getLatestCve()
              }else {
                console.log('无需重新获取')
                Tools.$emit('setMenu', (v1))
              }
            }).catch(function (err) {
              console.log('获取初始数据时出错：', err)
            })
          }
        }).catch(function (err) {
          console.log('获取初始数据时出错：', err)
          that.loadingCVE = false
        })
      },

      getLatestCve() {
        console.log('*****getLatestCve*****')
        var that = this
        that.loadingCVE = true
        axios.post('home/cvelatest').then(res => {
          if (res.status == 200) {
            console.log("最新的CVE数据为：", res.data.latestcves)
            that.searchAnsCves = res.data.latestcves
            that.totalNum = res.data.latestcves.length
            Tools.$emit('setSearchCVES', res.data.latestcves)
            localforage.setItem('latestCveList', res.data.latestcves)
            localforage.setItem('latestCveMenu', res.data.menu)
            Tools.$emit('setMenu', res.data.menu)
            that.loadingCVE = false
            // setTimeout(() => {
            //   // 执行以下语句，将刷新Index组件中的菜单
            //   Tools.$emit('getMenuNew', 'msg')
            // }, 2000)
            var List = []
            localforage.setItem('searchAns', List) //  searchAns存储搜索结果
          }
        }).catch(err => {
          console.log("出错！具体错误为：", err)
          that.loadingCVE = false
        })
      },

      findSearchAns() {
        console.log('*****findSearchAns*****')
        this.isLearnMore = false
        var List
        var that = this // 不能用 this.searchAnsCves，会找不到，无敌大坑！
        that.loadingCVE = true
        localforage.getItem('searchAns').then(function (value) {
          // 当离线仓库中的值被载入时，此处代码运行
          // console.log('cve searchAns', value)
          if (value == null) {
            that.searchAnsCves = []
          } else {
            that.searchAnsCves = value
            that.totalNum = value.length
          }
          that.loadingCVE = false
        }).catch(function (err) {
          // 当出错时，此处代码运行
          console.log(err);
          that.loadingCVE = false
        })
      },

      learnMore(cveid) { // 是否进入该条CVE的详情页面，如进入，将隐藏最初的卡片而进入标签页
        console.log('*****learnMore*****')

        this.isLearnMore = true
        // console.log('查看详情的cveid是：', cveid)
        var list = this.searchAnsCves // 当搜索结果较少时，直接遍历搜索结果数组
        console.log('查看searchAnsCves是：', this.searchAnsCves)
        var len = list.length
        if (len <= 1000) {
          for (var i = 0; i < len; i++) {
            var tmp = list[i]
            if (tmp['cveid'] == cveid) {
              console.log('成功找到：', tmp)
              console.log('selectCvethis1是：', list[i])
              this.selectCve = list[i]
              this.selectId = i // 存储当前选中的CVE在整个List中的位置
            } else {
              continue
            }
          }
        } else { // 当搜索结果较多时，在数据库中搜索
          var that = this
          axios.post('/common/cveinfo', qs.stringify({ cveid: cveid })).then(res => {
            if (res.status == 200) {
              console.log('搜索返回的结果：', res.data)
              // that.selectCve = res.data
              that.selectCve = res.data
              console.log('selectCve是：', that.selectCve)
            }
          }).catch(err => {
            console.log('出错！具体错误为：', err)
          })
        }
        console.log('selectCvethis是：', this.selectCve)
        this.getOptionsOfProducts() // 确定products的待选项
        this.getOptionOfVersion()
        this.getOptionOfVulType()
        this.getOptionOfVulComp()
        this.getOptionOfRoot()
        this.getOptionOfVector()
        this.getOptionOfImpact()
        this.productList = []
        this.versionList = []
        this.vulCompList = []
        this.typeList = []
        this.rootList = []
        this.vectorList = []
        this.impactList = []
        this.getMorePicData()
      },

      changeChart(obj) { // 将aspects中的 ; 改为 ,
        // console.log('obj:', obj)
        obj.product = this.ifFindChar(obj.product)
        obj.version = this.ifFindChar(obj.version)
        obj.component = this.ifFindChar(obj.component)
        obj.type = this.ifFindChar(obj.type)
        obj.root = this.ifFindChar(obj.root)
        obj.vector = this.ifFindChar(obj.vector)
        obj.impact = this.ifFindChar(obj.impact)
        return obj
      },

      ifFindChar(str) { // 是否有;，有的话将;替换为,
        if (str) {
          if (str.indexOf(';') != -1) { // 没有找到;则跳过，有则将;替换成,
            str = str.replace(/;/g, ', ')
          }
        }
        return str
      },

      splitDic2List(meta) { // 将一个字典数组转化为两个List，字典格式为 { value: len, name: tmpList[i] }
        var x = []
        var y = []
        var ret = []
        // console.log('meta', meta)
        if (meta.length) { // meta数组不为空
          for (var i = 0; i < meta.length; i++) {
            var tmp = meta[i]
            x.push(tmp.value)
            y.push(tmp.name)
          }
        }
        console.log('x', x)
        console.log('y', y)
        ret.push(x)
        ret.push(y)

        return ret
      },

      gotoCveList() { // 点击back按钮时的响应事件
        console.log('*****gotoCveList*****')
        this.isLearnMore = false
        // console.log('isLearnMore:', this.isLearnMore)
      },

      gotoNextCve() { // 查看目前展开CVE的下一条记录
        console.log('*****gotoNextCve*****')
        var nextId = this.selectId + 1
        this.selectCve = this.searchAnsCves[nextId]
        this.selectId = nextId
        // if (this.tab == 1) {
        //   this.getMorePicData()
        //   this.getOptionsOfProducts()
        // }else if(this.tab==2){
        //   this.getCompareData()
        // }
        this.getMorePicData()
        this.getOptionsOfProducts()
        this.getOptionOfVersion()
        this.getOptionOfVulType()
        this.getOptionOfVulComp()
        this.getOptionOfRoot()
        this.getOptionOfVector()
        this.getOptionOfImpact()
        this.getCompareData()
      },

      shiftTab(tab, event) { // 点击顶层tab键，开始绘图
        console.log('*****shiftTab*****')
        // console.log(tab)
        // console.log(event)
        if (tab.index == '1') { // 当点击dashboard时，获取绘制图像的数据，当前在content页，变成dashboard页
          this.getMorePicData()
          this.getOptionsOfProducts()
          this.getOptionOfVersion()
          this.getOptionOfVulType()
          this.getOptionOfVulComp()
          this.getOptionOfRoot()
          this.getOptionOfVector()
          this.getOptionOfImpact()
          this.tab = 1
        } else if (tab.index == '0') { // 当前在dashboard页
          this.tab = 0
        } else if (tab.index == '2') { // 切换到compare页
          console.log('切换到compare页')
          this.getCompareData()

        }
      },


      /****************以下为绘图函数*********/
      getPictures(product) {
        // console.log('choose product:', product)
        if (product != '') {
          var param = product
          // if (this.versionOfproducts.indexOf(product) != -1) { // 该产品有对应的版本
          //   this.picPieOfVersion(param)
          // }
          this.picPieOfVersion(param)
          this.getBarPicData(param)
        }
      },


      getOptionsOfProducts() { // 给 optionsOfProduct赋值
        console.log('*****getOptionsOfProducts*****')
        this.optionsOfProduct[0].options.splice(0, this.optionsOfProduct[0].options.length)
        this.optionsOfProduct[1].options.splice(0, this.optionsOfProduct[1].options.length)
        this.versionOfproducts.splice(0, this.versionOfproducts.length) // version对应的products
        var products = this.selectCve.product // 产品aspects
        console.log('products:', this.selectCve)

        /*2、根据products来确定选择框待选项，当用户所选择的product没有相应version时，给用户提示，当version为Unkown时，整个version pie chart都为灰色*/

        var proOfVersion = this.splitStr2List(products)
        proOfVersion = proOfVersion.sort()
        // console.log('proOfVersion:', proOfVersion)
        var versions = this.selectCve.version // version aspects
        var versionOfproducts = []
        if (versions != 'Unknown') {
          var ret = this.str2dic0(versions)
          versionOfproducts = ret[ret.length - 1] // version中的products
          this.versionOfproducts = versionOfproducts
          // console.log('versionOfproducts:', versionOfproducts)
          var list1 = [] // 有版本信息的
          var list2 = [] // 无版本信息的
          for (var i = 0; i < proOfVersion.length; i++) {
            if (versionOfproducts.indexOf(proOfVersion[i]) != -1) { // 该product有对应的version
              // console.log('type:', typeof (this.optionsOfProduct[0].options))
              list1.push({ value: proOfVersion[i], label: proOfVersion[i] })
            }
            else {// 无版本信息
              list2.push({ value: proOfVersion[i], label: proOfVersion[i] })
            }
          }
          this.optionsOfProduct[0].options = list1
          this.optionsOfProduct[1].options = list2
        } else {
          var list = []
          for (var i = 0; i < proOfVersion.length; i++) {
            list.push({ value: proOfVersion[i], label: proOfVersion[i] })
          }
          this.optionsOfProduct[1].options = list
        }

      },


      getOptionOfVersion() {
        console.log('*****getOptionOfVersion*****')
        this.optionsOfVersion.splice(0, this.optionsOfVersion.length)
        var version = this.selectCve.version
        if (version != "") {
          this.optionsOfVersion = version.split(';')

        }
      },

      getOptionOfVulType() {
        console.log('*****getOptionOfVulType*****')
        this.optionsOfType.splice(0, this.optionsOfType.length)
        var type = this.selectCve.type
        if (type != "") {
          this.optionsOfType = type.split(';')

        }
      },

      getOptionOfVulComp() {
        console.log('*****getOptionOfVulComp*****')
        this.optionsOfComp.splice(0, this.optionsOfComp.length)
        var type = this.selectCve.component
        if (type != "") {
          this.optionsOfComp = type.split(';')

        }
      },

      getOptionOfRoot() {
        console.log('*****getOptionOfRoot*****')
        this.optionsOfRoot.splice(0, this.optionsOfRoot.length)
        var type = this.selectCve.root
        if (type != "") {
          this.optionsOfRoot = type.split(';')

        }
      },


      getOptionOfVector() {
        console.log('*****getOptionOfVector*****')
        this.optionsOfVector.splice(0, this.optionsOfVector.length)
        var type = this.selectCve.vector
        if (type != "") {
          this.optionsOfVector = type.split(';')

        }
      },


      getOptionOfImpact() {
        console.log('*****getOptionOfImpact*****')
        this.optionsOfImpact.splice(0, this.optionsOfImpact.length)
        var type = this.selectCve.impact
        if (type != "") {
          this.optionsOfImpact = type.split(';')

        }
      },

      // 单独绘制version饼图，该饼图根据所选择的product进行刷新
      picPieOfVersion(product) {
        console.log('*****picPieOfVersion*****')
        var currentCve = this.selectCve
        this.loadingChart = true
        axios.post('/common/multiinfo', qs.stringify({ product: product, aspect_type: this.optionsOfAspectType[parseInt(this.dashboard)] })).then(res => {
          if (res.status == 200) {
            console.log('current data:', res.data)
            this.list2PicNew(res.data, this.productList, 'product')
            this.list2PicNew(res.data, this.versionList, 'version')
            this.list2PicNew(res.data, this.typeList, 'vultype')
            this.list2PicNew(res.data, this.vulCompList, 'vulcomp')
            this.list2PicNew(res.data, this.rootList, 'root')
            this.list2PicNew(res.data, this.vectorList, 'vector')
            this.list2PicNew(res.data, this.impactList, 'impact')

            if (this.productChart != null && this.productChart != "" && this.productChart != undefined) {
              this.productChart.dispose();//销毁
            }
            try {
              this.MostFrequentProduct('MostFrequentProduct' + this.optionsOfAspect[parseInt(this.dashboard)])
              this.productList.splice(0, this.productList.length)
            } catch (error) {
              console.log(error)
            }

            if (this.versionChart != null && this.versionChart != "" && this.versionChart != undefined) {
              this.versionChart.dispose();//销毁
            }
            try {
              this.MostFrequentVersion('MostFrequentVersion' + this.optionsOfAspect[parseInt(this.dashboard)])
              this.versionList.splice(0, this.versionList.length)
            } catch (error) {
              console.log(error)
            }

            if (this.typeChart != null && this.typeChart != "" && this.typeChart != undefined) {
              this.typeChart.dispose();//销毁
            }
            try {
              this.MostFrequentVulType('MostFrequentVulType' + this.optionsOfAspect[parseInt(this.dashboard)])
              this.typeList.splice(0, this.typeList.length)
            } catch (error) {
              console.log(error)
            }


            if (this.vulCompChart != null && this.vulCompChart != "" && this.vulCompChart != undefined) {
              this.vulCompChart.dispose();//销毁
            }
            try {
              this.MostFrequentVulComp('MostFrequentVulComp' + this.optionsOfAspect[parseInt(this.dashboard)])
              this.vulCompList.splice(0, this.vulCompList.length)
            } catch (error) {
              console.log(error)
            }

            if (this.rootChart != null && this.rootChart != "" && this.rootChart != undefined) {
              this.rootChart.dispose();//销毁
            }
            try {
              this.MostFrequentRoot('MostFrequentRoot' + this.optionsOfAspect[parseInt(this.dashboard)])
              this.rootList.splice(0, this.rootList.length)
            } catch (error) {
              console.log(error)
            }

            if (this.vectorChart != null && this.vectorChart != "" && this.vectorChart != undefined) {
              this.vectorChart.dispose();//销毁
            }
            try {
              this.MostFrequentVector('MostFrequentVector' + this.optionsOfAspect[parseInt(this.dashboard)])
              this.vectorList.splice(0, this.vectorList.length)
            } catch (error) {
              console.log(error)
            }

            if (this.impactChart != null && this.impactChart != "" && this.impactChart != undefined) {
              this.impactChart.dispose();//销毁
            }
            try {
              this.MostFrequentImpact('MostFrequentImpact' + this.optionsOfAspect[parseInt(this.dashboard)])
              this.impactList.splice(0, this.impactList.length)
            } catch (error) {
              console.log(error)
            }
            this.loadingChart = false
          }
        }).catch(err => {
          console.log('出错！具体错误为：', err)
        })
      },


      picPieOfVersionOld(product) {
        console.log('*****picPieOfVersion*****')
        var currentCve = this.selectCve
        console.log('current cve:', currentCve)
        /*饼图*/
        var versionStr = currentCve.version
        console.log('versionStr', versionStr)
        if (versionStr == 'Unknown') {
          this.splitStr(versionStr, this.versionList)
        } else {
          var ret = this.str2dic0(versionStr)
          // console.log('pic ret:', ret)
          var len = ret.length
          var productList = ret[len - 1] // 产品列表
          var position = productList.indexOf(product) // 根据选择的product刷新对应的version数据
          this.list2Pic(ret[position], this.versionList)
        }
        if (this.versionChart != null && this.versionChart != "" && this.versionChart != undefined) {
          this.versionChart.dispose();//销毁
        }
        this.MostFrequentVersion()
        this.versionList.splice(0, this.versionList.length)//清空数组，防止因重复点击导致数组长度变长
        // version比较特殊，因为version需要和product对应起来才有意义
      },



      getMorePicData() {
        console.log('*****getMorePicData*****')
        var currentCve = this.selectCve

        // var productStr = currentCve.product
        // this.splitStr(productStr, this.productList)
        if (this.productChart != null && this.productChart != "" && this.productChart != undefined) {
          this.productChart.dispose();//销毁
        }
        if (this.productList.length) {
          try{
            this.MostFrequentProduct('MostFrequentProduct' + this.optionsOfAspect[parseInt(this.dashboard)])
            this.productList.splice(0, this.productList.length)
          } catch (error) {
            console.log(error)
          }
        }
        else {
          this.productS = 0
        }

        // var versionStr = currentCve.version
        // this.splitStr(versionStr, this.versionList)
        if (this.versionChart != null && this.versionChart != "" && this.versionChart != undefined) {
          this.versionChart.dispose();//销毁
        }
        if (this.versionList.length) {
          try {
            this.MostFrequentVersion('MostFrequentVersion' + this.optionsOfAspect[parseInt(this.dashboard)])
            this.versionList.splice(0, this.versionList.length)
          } catch (error) {
            console.log(error)
          }
        }
        else {
          this.versionS = 0
        }

        // console.log("2.MostFrequentVulType")
        // var typeStr = currentCve.type
        // this.splitStr(typeStr, this.typeList)
        if (this.typeChart != null && this.typeChart != "" && this.typeChart != undefined) {
          this.typeChart.dispose();//销毁
        }
        if (this.typeList.length) {
          try {
            this.MostFrequentVulType('MostFrequentVulType' + this.optionsOfAspect[parseInt(this.dashboard)])
            this.typeList.splice(0, this.typeList.length)
          } catch (error) {
            console.log(error)
          }
        }
        else {
          this.typeS = 0
        }


        // console.log("3.MostFrequentVulComp")
        // this.splitStr(currentCve.component, this.vulCompList)
        if (this.vulCompChart != null && this.vulCompChart != "" && this.vulCompChart != undefined) {
          this.vulCompChart.dispose();//销毁
        }
        if (this.vulCompList.length) {
          try {
            this.MostFrequentVulComp('MostFrequentVulComp' + this.optionsOfAspect[parseInt(this.dashboard)])
            this.vulCompList.splice(0, this.vulCompList.length)
          } catch (error) {
            console.log(error)
          }
        }
        else {
          this.vulCompS = 0
        }


        // console.log("4.MostFrequentRoot")
        // this.splitStr(currentCve.root, this.rootList)
        if (this.rootChart != null && this.rootChart != "" && this.rootChart != undefined) {
          this.rootChart.dispose();//销毁
        }
        if (this.rootList.length) {
          try {
            this.MostFrequentRoot('MostFrequentRoot' + this.optionsOfAspect[parseInt(this.dashboard)])
            this.rootList.splice(0, this.rootList.length)
          } catch (error) {
            console.log(error)
          }
        }
        else {
          this.rootS = 0
        }


        // console.log("5.MostFrequentVector")
        // this.splitStr(currentCve.vector, this.vectorList)
        if (this.vectorChart != null && this.vectorChart != "" && this.vectorChart != undefined) {
          this.vectorChart.dispose();//销毁
        }
        if (this.vectorList.length) {
          try {
            this.MostFrequentVector('MostFrequentVector' + this.optionsOfAspect[parseInt(this.dashboard)])
            this.vectorList.splice(0, this.vectorList.length)
          } catch (error) {
            console.log(error)
          }
        } else {
          this.vectorS = 0
        }


        // console.log("6.MostFrequentImpact")
        // this.splitStr(currentCve.impact, this.impactList)
        if (this.impactChart != null && this.impactChart != "" && this.impactChart != undefined) {
          this.impactChart.dispose();//销毁
        }
        if (this.impactList.length) {
          try {
            this.MostFrequentImpact('MostFrequentImpact' + this.optionsOfAspect[parseInt(this.dashboard)])
            this.impactList.splice(0, this.impactList.length)
          } catch (error) {
            console.log(error)
          }
        } else {
          this.impactS = 0
        }

      },

      // 将获取到的版本列表转化为绘制图形需要的格式
      list2Pic(list, metaList) {
        metaList.splice(0, metaList.length);//清空
        for (var i = 0; i < list.length; i++) {
          metaList.push({ value: 1, name: list[i] })
        }
      },

      // 将获取到的版本列表转化为绘制图形需要的格式
      list2PicNew(list, metaList, keyword) {
        metaList.splice(0, metaList.length);//清空
        for (var i = 0; i < list.length; i++) {
          if (list[i].aspect_2_ori.includes(keyword)) {
            metaList.push({ value: list[i].co_appear_time, name: list[i].aspect_2})
          }
        }
        console.log(metaList.length)
      },

      splitStr(str, metaList) { // 将字符串按照 ; 分割，并生成 metaList
        if (metaList.length) {
          metaList.splice(0, metaList.length);//清空
        }
        var splchar = ';'
        var tmpList = []
        if (str) { // 字符串存在
          if (str.indexOf(splchar) == -1) { // 字符串不存在分隔符
            var len = str.length
            metaList.push({ value: len, name: str })
          } else {
            tmpList = str.split(splchar)
            for (var i = 0; i < tmpList.length; i++) {
              var len = tmpList[i].length
              metaList.push({ value: len, name: tmpList[i] })
            }
          }
        }
        else {
          metaList = []
        }
      },

      splitStr2List(str) { // 将字符串按照 , 分割，返回一个数组
        var splchar = ';'
        var tmpList = []
        var retList = []
        if (str) { // 字符串存在
          if (str.indexOf(';') == -1 && str.indexOf(',') == -1) { // 字符串不存在分隔符且字符串不为空
            retList.push(str)
          } else {
            if (str.indexOf(',') != -1) { // 以,为分隔符
              str = str.replace(/, /g, ';')
            }
            tmpList = str.split(splchar)
            for (var i = 0; i < tmpList.length; i++) {
              retList.push(tmpList[i])
            }
          }
        }
        return retList
      },

      str2dic0(str) { // 字符串转字典数组，用于 bsdi bsd os:3.1, freebsd:1.0, freebsd:1.1此种格式，统计产品对应的版本号
        // 生成产品列表（去重）
        var proList = []
        var ret = []
        var spltchar = ';'
        if (str) {
          str = str.replace(/, /g, ';')
          // console.log('str:', str)
          if (str.indexOf(spltchar) == -1) {
            proList.push(str.split(':')[0])
            ret.push(str.split(':')[1])
          } else {
            var tmpList = str.split(spltchar)
            // console.log('tmpList:', tmpList)
            for (var i = 0; i < tmpList.length; i++) {
              proList.push(tmpList[i].split(':')[0])
            }

            proList = this.unique(proList) // 去重
            tmpList = tmpList.sort() // 排序
            proList = proList.sort()
            // console.log('tmpList', tmpList)
            // console.log('proList', proList)

            var position = 0 // 决定tmpList下次开始查找的位置，减少查找时间
            for (var i = 0; i < proList.length; i++) {
              var b = [] // 辅助数组
              var product = proList[i] // 当前产品
              var j = position
              for (j; j < tmpList.length; j++) {
                var end = tmpList[j].indexOf(':')
                if (tmpList[j].substring(0, end) == product) {
                  // console.log('tmpList[j]', tmpList[j].substring(0, end))
                  b.push(tmpList[j].split(':')[1])
                } else {
                  position = j; // 改变下次遍历的起始位置
                  break;  // 因为前面已经对tmpList排序了，当按照顺序查找不到对应的product时，直接跳出本次循环
                }
                ret[i] = b
              }
            }
          }
          ret[proList.length] = proList // ret数组的最后一个元素为该条cve的产品列表
          // console.log('ret:', ret)
          return ret
        }
      },

      unique(arr) {
        //Set数据结构，它类似于数组，其成员的值都是唯一的
        return Array.from(new Set(arr)); // 利用Array.from将Set结构转换成数组
      },

      str2dic(str, x, data, flag) { // 字符串转字典，x为横坐标
        if (x.length) {
          x.splice(0, x.length);//清空
        }
        if (data.length) {
          data.splice(0, data.length);//清空
        }
        str = str.replace("{", "")
        str = str.replace("}", "")
        var list = str.split(",")
        list.sort()
        for (var i = 0; i < list.length; i++) {
          var tmp = list[i].split(':')
          tmp[0] = tmp[0].replace("'", "")
          tmp[0] = tmp[0].replace("'", "")
          x.push(tmp[0])
          tmp[1] = tmp[1].replace("'", "")
          tmp[1] = tmp[1].replace("'", "")
          var ok = parseInt(tmp[1]) // 字符串转数字，注意没有 '' || "" 等符号
          data.push(ok)
        }
      },

      obj2list(obj, x, data, flag) {
        if (x.length) {
          x.splice(0, x.length);//清空
        }
        if (data.length) {
          data.splice(0, data.length);//清空
        }
        if (flag == 0) { // timeline
          for (var key in obj) {
            var k = key.replace("y", "")
            x.push(k)
            var item = obj[key]
            data.push(item)
          }
        } else if (flag == 1) { // c3bm
          for (var key in obj) {
            var k = key.replace("y", "")
            x.push(k)
            var item = obj[key]
            if (item == null) { // c3bm的值存在null的情况，且需要对值做进一步处理
              data.push(0)
            } else {
              var list = item.split(',')
              var ans = 0
              for (var i = 0; i < list.length; i++) {
                ans += parseFloat(list[i])
              }
              data.push(ans)
            }
          }
        } else {
          console.log("obj2list 出错")
        }
      },

      getBarPicData(product) {
        console.log('*****getBarPicData*****')
        var that = this
        // console.log('product:', product)
        that.loading = true
        if (product != '') {
          axios.post('common/bardata', qs.stringify({ product: product, aspect_type: this.optionsOfAspectType[parseInt(this.dashboard)]})).then(res => {
            if (res.status == 200) {
              console.log("最新的bardata数据为：", res.data)
              var ret = res.data
              if (ret == 0) {
                // 没有查询到相应的数据
                that.$message.error('No corresponding data was queried.');
                // that.versionList.length = 0
                that.severityX.length = 0
                that.severityData.length = 0
                that.accessX.length = 0
                that.accessData.length = 0
                that.interactX.length = 0
                that.interactData.length = 0
                that.authX.length = 0
                that.authData.length = 0
                that.attackComplexX.length = 0
                that.attackComplexData.length = 0
                that.impactConfidenceX.length = 0
                that.impactConfidenceData.length = 0
                that.impactIntegerX.length = 0
                that.impactIntegerData.length = 0
                that.impactAvailableX.length = 0
                that.impactAvailableData.length = 0
                that.publishDateX.length = 0
                that.publishDateData.length = 0
                that.timeLineX.length = 0
                that.timeLineData.length = 0
                that.c3bmX.length = 0
                that.c3bmData.length = 0
                // 和product相关的绘图函数
                // that.MostFrequentVersion()
                // that.MostFrequentVulType()
                // that.MostFrequentVulComp()
                // that.MostFrequentRoot()
                // that.MostFrequentVector()
                // that.MostFrequentImpact()
                that.Severity('Severity'+this.optionOfBar[parseInt(this.dashboard)])
                that.Access('Access'+this.optionOfBar[parseInt(this.dashboard)])
                that.Interaction('Interaction'+this.optionOfBar[parseInt(this.dashboard)])
                that.AttackComplex('AttackComplex'+this.optionOfBar[parseInt(this.dashboard)])
                that.ImpactConfidence('ImpactConfidence'+this.optionOfBar[parseInt(this.dashboard)])
                that.ImpactInteger('ImpactInteger'+this.optionOfBar[parseInt(this.dashboard)])
                that.ImpactAvailable('ImpactAvailable'+this.optionOfBar[parseInt(this.dashboard)])
                that.PublishDate('PublishDate'+this.optionOfBar[parseInt(this.dashboard)])
                that.TimeLine('TimeLine'+this.optionOfBar[parseInt(this.dashboard)])
                that.C3BMIndex('C3BMIndex'+this.optionOfBar[parseInt(this.dashboard)])
                // that.accessChart.dispose();//销毁
                // that.severityChart.dispose();//销毁
                // that.interactionChart.dispose();//销毁
                // that.timeLineChart.dispose();//销毁
                // that.c3bIndexChart.dispose();//销毁
              }
              else {
                // 柱状图数据赋值
                var accessStr = ret.bar.access
                that.str2dic(accessStr, that.accessX, that.accessData)
                if (that.accessChart != null && that.accessChart != "" && that.accessChart != undefined) {
                  that.accessChart.dispose();//销毁
                }
                var severityStr = ret.bar.severity
                that.str2dic(severityStr, that.severityX, that.severityData)
                if (that.severityChart != null && that.severityChart != "" && that.severityChart != undefined) {
                  that.severityChart.dispose();//销毁
                }
                var interactionStr = ret.bar.interaction
                that.str2dic(interactionStr, that.interactX, that.interactData)
                if (that.interactionChart != null && that.interactionChart != "" && that.interactionChart != undefined) {
                  that.interactionChart.dispose();//销毁
                }

                var authStr = ret.bar.auth
                that.str2dic(authStr, that.authX, that.authData)
                if (that.authChart != null && that.authChart != "" && that.authChart != undefined) {
                  that.authChart.dispose();//销毁
                }
                var attackcomplexStr = ret.bar.attackcomplex
                that.str2dic(attackcomplexStr, that.attackComplexX, that.attackComplexData)
                if (that.attackComplexChart != null && that.attackComplexChart != "" && that.attackComplexChart != undefined) {
                  that.attackComplexChart.dispose();//销毁
                }
                var impactconfidenceStr = ret.bar.impactconfidence
                that.str2dic(impactconfidenceStr, that.impactConfidenceX, that.impactConfidenceData)
                if (that.impactConfidenceChart != null && that.impactConfidenceChart != "" && that.impactConfidenceChart != undefined) {
                  that.impactConfidenceChart.dispose();//销毁
                }

                var impactintegerStr = ret.bar.impactinteger
                that.str2dic(impactintegerStr, that.impactIntegerX, that.impactIntegerData)
                if (that.impactIntegerChart != null && that.impactIntegerChart != "" && that.impactIntegerChart != undefined) {
                  that.impactIntegerChart.dispose();//销毁
                }
                var impactavailableStr = ret.bar.impactavailable
                that.str2dic(impactavailableStr, that.impactAvailableX, that.impactAvailableData)
                if (that.impactAvailableChart != null && that.impactAvailableChart != "" && that.impactAvailableChart != undefined) {
                  that.impactAvailableChart.dispose();//销毁
                }
                var publishdateStr = ret.bar.publishdate
                that.str2dic(publishdateStr, that.publishDateX, that.publishDateData)
                if (that.publishDateChart != null && that.publishDateChart != "" && that.publishDateChart != undefined) {
                  that.publishDateChart.dispose();//销毁
                }

                // 折线图数据赋值
                var timeLineObj = ret.timeline
                that.obj2list(timeLineObj, that.timeLineX, that.timeLineData, 0)
                if (that.timeLineChart != null && that.timeLineChart != "" && that.timeLineChart != undefined) {
                  that.timeLineChart.dispose();//销毁
                }
                var c3bmObj = ret.c3bm
                that.obj2list(c3bmObj, that.c3bmX, that.c3bmData, 1)
                if (that.c3bIndexChart != null && that.c3bIndexChart != "" && that.c3bIndexChart != undefined) {
                  that.c3bIndexChart.dispose();//销毁
                }

                // setTimeout(() => {
                //   that.gotoPaints()
                // }, 2)
                that.Severity('Severity'+this.optionOfBar[parseInt(this.dashboard)])
                that.Access('Access'+this.optionOfBar[parseInt(this.dashboard)])
                that.Interaction('Interaction'+this.optionOfBar[parseInt(this.dashboard)])
                that.Auth('Auth'+this.optionOfBar[parseInt(this.dashboard)])
                that.AttackComplex('AttackComplex'+this.optionOfBar[parseInt(this.dashboard)])
                that.ImpactConfidence('ImpactConfidence'+this.optionOfBar[parseInt(this.dashboard)])
                that.ImpactInteger('ImpactInteger'+this.optionOfBar[parseInt(this.dashboard)])
                that.ImpactAvailable('ImpactAvailable'+this.optionOfBar[parseInt(this.dashboard)])
                that.PublishDate('PublishDate'+this.optionOfBar[parseInt(this.dashboard)])
                that.TimeLine('TimeLine'+this.optionOfBar[parseInt(this.dashboard)])
                that.C3BMIndex('C3BMIndex'+this.optionOfBar[parseInt(this.dashboard)])
                this.loading = false
              }
            }
          }).catch(err => {
            console.log("出错！具体错误为：", err)
            this.loading = false
          })
        }
      },

      // 调用柱状图绘制函数
      gotoPaints() {
        this.Severity()
        this.Access()
        this.Interaction()
        this.TimeLine()
        this.C3BMIndex()
      },


      MostFrequentProduct(elementId) {
        // initialize the echarts instance
        this.productChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.productChart.setOption({
          // tooltip: {
          //   trigger: 'item'
          // },
          // legend: {
          //   orient: 'vertical',
          //   left: 'left',
          //   show: false
          // },
          // series: [
          //   {
          //     // name: 'Access From',
          //     type: 'pie',
          //     radius: '50%',
          //     data: this.productList,
          //     emphasis: {
          //       itemStyle: {
          //         shadowBlur: 10,
          //         shadowOffsetX: 0,
          //         shadowColor: 'rgba(0, 0, 0, 0.5)'
          //       }
          //     }
          //   }
          // ]

          series: [
            {
              type: "wordCloud",
              //用来调整词之间的距离
              gridSize: 10,
              //用来调整字的大小范围
              // Text size range which the value in data will be mapped to.
              // Default to have minimum 12px and maximum 60px size.
              sizeRange: [12, 24],
              // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45
              //用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
              // rotationRange: [-45, 0, 45, 90],
              // rotationRange: [ 0,90],
              rotationRange: [0, 0],
              //随机生成字体颜色
              // maskImage: maskImage,
              textStyle: {

                color: function () {
                  return (
                      "rgb(" +
                      Math.round(Math.random() * 255) +
                      ", " +
                      Math.round(Math.random() * 255) +
                      ", " +
                      Math.round(Math.random() * 255) +
                      ")"
                  );
                }

              },
              //位置相关设置
              // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
              // Default to be put in the center and has 75% x 80% size.
              left: "center",
              top: "center",
              right: null,
              bottom: null,
              width: "100%",
              height: "100%",
              //数据
              data: this.productList
            }
          ]
        });
      },


      MostFrequentVersion(elementId) {
        // initialize the echarts instance
        this.versionChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.versionChart.setOption({
        //   // title: {
        //   //   text: 'Most Frequent Version',
        //   //   // subtext: 'Most Frequent Version',
        //   //   // left: 'center',
        //   //   textStyle: {
        //   //     fontSize: 14
        //   //   }
        //   // },
        //   tooltip: {
        //     trigger: 'item'
        //   },
        //   legend: {
        //     orient: 'vertical',
        //     left: 'left',
        //     show: false
        //   },
        //   series: [
        //     {
        //       // name: 'Access From',
        //       type: 'pie',
        //       radius: '50%',
        //       data: this.versionList,
        //       emphasis: {
        //         itemStyle: {
        //           shadowBlur: 10,
        //           shadowOffsetX: 0,
        //           shadowColor: 'rgba(0, 0, 0, 0.5)'
        //         }
        //       }
        //     }
        //   ]


          series: [
            {
              type: "wordCloud",
              //用来调整词之间的距离
              gridSize: 10,
              //用来调整字的大小范围
              // Text size range which the value in data will be mapped to.
              // Default to have minimum 12px and maximum 60px size.
              sizeRange: [12, 24],
              // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45
              //用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
              // rotationRange: [-45, 0, 45, 90],
              // rotationRange: [ 0,90],
              rotationRange: [0, 0],
              //随机生成字体颜色
              // maskImage: maskImage,
              textStyle: {

                color: function () {
                  return (
                      "rgb(" +
                      Math.round(Math.random() * 255) +
                      ", " +
                      Math.round(Math.random() * 255) +
                      ", " +
                      Math.round(Math.random() * 255) +
                      ")"
                  );
                }

              },
              //位置相关设置
              // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
              // Default to be put in the center and has 75% x 80% size.
              left: "center",
              top: "center",
              right: null,
              bottom: null,
              width: "100%",
              height: "100%",
              //数据
              data: this.versionList
            }
          ]
        });
      },

      MostFrequentVulType(elementId) {
        this.typeChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.typeChart.setOption({
        //   // 以下为饼图的绘制
        //   // title: {
        //   //   text: 'Most Frequent Type',
        //   //   // subtext: 'Most Frequent Version',
        //   //   // left: 'center',
        //   //   textStyle: {
        //   //     fontSize: 14
        //   //   }
        //   // },
        //   tooltip: {
        //     trigger: 'item'
        //   },
        //   legend: {
        //     orient: 'vertical',
        //     left: 'left',
        //     show: false
        //   },
        //   series: [
        //     {
        //       // name: 'Access From',
        //       type: 'pie',
        //       radius: '50%',
        //       // data: [
        //       //   { value: 10, name: 'type1' },
        //       //   { value: 9, name: 'type2' },
        //       //   { value: 8, name: 'type3' },
        //       //   { value: 6, name: 'type4' },
        //       //   { value: 4, name: 'type5' }
        //       // ],
        //       data: this.typeList,
        //       emphasis: {
        //         itemStyle: {
        //           shadowBlur: 10,
        //           shadowOffsetX: 0,
        //           shadowColor: 'rgba(0, 0, 0, 0.5)'
        //         }
        //       }
        //     }
        //   ]

          series: [
            {
              type: "wordCloud",
              //用来调整词之间的距离
              gridSize: 10,
              //用来调整字的大小范围
              // Text size range which the value in data will be mapped to.
              // Default to have minimum 12px and maximum 60px size.
              sizeRange: [12, 24],
              // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45
              //用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
              // rotationRange: [-45, 0, 45, 90],
              // rotationRange: [ 0,90],
              rotationRange: [0, 0],
              //随机生成字体颜色
              // maskImage: maskImage,
              textStyle: {

                color: function () {
                  return (
                    "rgb(" +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ")"
                  );
                }

              },
              //位置相关设置
              // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
              // Default to be put in the center and has 75% x 80% size.
              left: "center",
              top: "center",
              right: null,
              bottom: null,
              width: "100%",
              height: "100%",
              //数据
              data: this.typeList
            }
          ]
        });
      },

      MostFrequentVulComp(elementId) {
        this.vulCompChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.vulCompChart.setOption({
          // title: {
          //   text: 'Most Frequent VulComp',
          //   // subtext: 'Most Frequent Version',
          //   // left: 'center',
          //   textStyle: {
          //     fontSize: 14
          //   }
          // },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            show: false
          },
          // series: [
          //   {
          //     // name: 'Access From',
          //     type: 'pie',
          //     radius: '50%',
          //     // data: [
          //     //   { value: 10, name: 'VulComp1' },
          //     //   { value: 9, name: 'VulComp2' },
          //     //   { value: 8, name: 'VulComp3' },
          //     //   { value: 6, name: 'VulComp4' },
          //     //   { value: 4, name: 'VulComp5' }
          //     // ],
          //     data: this.vulCompList,
          //     emphasis: {
          //       itemStyle: {
          //         shadowBlur: 10,
          //         shadowOffsetX: 0,
          //         shadowColor: 'rgba(0, 0, 0, 0.5)'
          //       }
          //     }
          //   }
          // ]


          series: [
            {
              type: "wordCloud",
              gridSize: 10,
              sizeRange: [12, 24],
              rotationRange: [0, 0],
              textStyle: {
                color: function () {
                  return (
                    "rgb(" +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ")"
                  );
                }
              },
              left: "center",
              top: "center",
              right: null,
              bottom: null,
              width: "100%",
              height: "100%",
              //数据
              data: this.vulCompList
            }
          ]
        });
      },

      MostFrequentRoot(elementId) {
        this.rootChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.rootChart.setOption({
          // title: {
          //   text: 'Most Frequent Root Cause',
          //   // subtext: 'Most Frequent Version',
          //   // left: 'center',
          //   textStyle: {
          //     fontSize: 14
          //   }
          // },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            show: false
          },
          // series: [
          //   {
          //     // name: 'Access From',
          //     type: 'pie',
          //     radius: '50%',
          //     // data: [
          //     //   { value: 10, name: 'Root1' },
          //     //   { value: 9, name: 'Root2' },
          //     //   { value: 8, name: 'Root3' },
          //     //   { value: 12, name: 'Root4' },
          //     //   { value: 4, name: 'Root5' }
          //     // ],
          //     data: this.rootList,
          //     emphasis: {
          //       itemStyle: {
          //         shadowBlur: 10,
          //         shadowOffsetX: 0,
          //         shadowColor: 'rgba(0, 0, 0, 0.5)'
          //       }
          //     }
          //   }
          // ]


          series: [
            {
              type: "wordCloud",
              gridSize: 10,
              sizeRange: [12, 24],
              rotationRange: [0, 0],
              textStyle: {
                color: function () {
                  return (
                    "rgb(" +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ")"
                  );
                }
              },
              left: "center",
              top: "center",
              right: null,
              bottom: null,
              width: "100%",
              height: "100%",
              //数据
              data: this.rootList
            }
          ]
        });
      },

      MostFrequentVector(elementId) {
        this.vectorChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.vectorChart.setOption({
          // title: {
          //   text: 'Most Frequent Vector',
          //   // subtext: 'Most Frequent Version',
          //   // left: 'center',
          //   textStyle: {
          //     fontSize: 14
          //   }
          // },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            show: false
          },
          // series: [
          //   {
          //     // name: 'Access From',
          //     type: 'pie',
          //     radius: '50%',
          //     // data: [
          //     //   { value: 10, name: 'Vector1' },
          //     //   { value: 9, name: 'Vector2' },
          //     //   { value: 8, name: 'Vector3' },
          //     //   { value: 6, name: 'Vector4' },
          //     //   { value: 4, name: 'Vector5' }
          //     // ],
          //     data: this.vectorList,
          //     emphasis: {
          //       itemStyle: {
          //         shadowBlur: 10,
          //         shadowOffsetX: 0,
          //         shadowColor: 'rgba(0, 0, 0, 0.5)'
          //       }
          //     }
          //   }
          // ]


          series: [
            {
              type: "wordCloud",
              gridSize: 10,
              sizeRange: [12, 24],
              rotationRange: [0, 0],
              textStyle: {
                color: function () {
                  return (
                    "rgb(" +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ")"
                  );
                }
              },
              left: "center",
              top: "center",
              right: null,
              bottom: null,
              width: "100%",
              height: "100%",
              //数据
              data: this.vectorList
            }
          ]
        });
      },

      MostFrequentImpact(elementId) {
        this.impactChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.impactChart.setOption({
          // title: {
          //   text: 'Most Frequent Impact',
          //   // subtext: 'Most Frequent Version',
          //   // left: 'center',
          //   textStyle: {
          //     fontSize: 14
          //   }
          // },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            show: false
          },
          // series: [
          //   {
          //     // name: 'Access From',
          //     type: 'pie',
          //     radius: '50%',
          //     // data: [
          //     //   { value: 10, name: 'Impact1' },
          //     //   { value: 9, name: 'Impact2' },
          //     //   { value: 8, name: 'Impact3' },
          //     //   { value: 6, name: 'Impact4' },
          //     //   { value: 4, name: 'Impact5' }
          //     // ],
          //     data: this.impactList,
          //     emphasis: {
          //       itemStyle: {
          //         shadowBlur: 10,
          //         shadowOffsetX: 0,
          //         shadowColor: 'rgba(0, 0, 0, 0.5)'
          //       }
          //     }
          //   }
          // ]


          series: [
            {
              type: "wordCloud",
              gridSize: 10,
              sizeRange: [12, 24],
              rotationRange: [0, 0],
              textStyle: {
                color: function () {
                  return (
                    "rgb(" +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ")"
                  );
                }
              },
              left: "center",
              top: "center",
              right: null,
              bottom: null,
              width: "100%",
              height: "100%",
              //数据
              data: this.impactList
            }
          ]
        });
      },

      Severity(elementId) {
        // initialize the echarts instance
        this.severityChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.severityChart.setOption({
          title: {
            text: 'Severity',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {},
          xAxis: {
            // data: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
            data: this.severityX,
            axisTick: {
              show: false
            },
            axisLine: {
              show: true,
            },
            axisLabel: {
              interval: 0,
              rotate: 45,
              textStyle: {
                fontSize: '10',
                itemSize: ''
              }
            },
          },
          yAxis: {},
          series: [
            {
              // name: 'sales',
              type: 'bar',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#83bff6' },
                  { offset: 0.5, color: '#188df0' },
                  { offset: 1, color: '#188df0' }
                ])
              },
              emphasis: {
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#2378f7' },
                    { offset: 0.7, color: '#2378f7' },
                    { offset: 1, color: '#83bff6' }
                  ])
                }
              },
              label: {
                show: true,
                position: 'top',
                // textStyle:{
                // }
              },
              // data: [0, 0, 12, 106, 271, 351]
              data: this.severityData
            }
          ]
        });
      },

      Access(elementId) {
        // initialize the echarts instance
        this.accessChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.accessChart.setOption({
          title: {
            text: 'Access',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {},
          xAxis: {
            // data: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
            data: this.accessX,
            // show:false
            axisTick: {
              show: false
            },
            axisLine: {
              show: true,
            },
            axisLabel: {
              interval: 0,
              rotate: 45,
              textStyle: {
                fontSize: '10',
                itemSize: ''
              }
            },
          },
          yAxis: {
          },
          series: [
            {
              // name: 'sales',
              type: 'bar', itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#83bff6' },
                  { offset: 0.5, color: '#188df0' },
                  { offset: 1, color: '#188df0' }
                ])
              },
              emphasis: {
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#2378f7' },
                    { offset: 0.7, color: '#2378f7' },
                    { offset: 1, color: '#83bff6' }
                  ])
                }
              },
              label: {
                show: true,
                position: 'top',
                // textStyle:{
                // }
              },
              // data: [0, 0, 12, 106, 271, 351]
              data: this.accessData
            }
          ]
        });
      },

      Interaction(elementId) {
        // initialize the echarts instance
        this.interactionChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.interactionChart.setOption({
          title: {
            text: 'Interaction',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {},
          xAxis: {
            // data: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
            data: this.interactX,
            axisTick: {
              show: false
            },
            axisLine: {
              show: true,
            },
            axisLabel: {
              interval: 0,
              rotate: 45,
              textStyle: {
                fontSize: '10',
                itemSize: ''
              }
            },
          },
          yAxis: {},
          series: [
            {
              // name: 'sales',
              type: 'bar',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#83bff6' },
                  { offset: 0.5, color: '#188df0' },
                  { offset: 1, color: '#188df0' }
                ])
              },
              emphasis: {
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#2378f7' },
                    { offset: 0.7, color: '#2378f7' },
                    { offset: 1, color: '#83bff6' }
                  ])
                }
              },
              label: {
                show: true,
                position: 'top',
                // textStyle:{
                // }
              },
              // data: [0, 0, 12, 106, 271, 351]
              data: this.interactData
            }
          ]
        });
      },


      Auth(elementId) {
        // initialize the echarts instance
        this.authChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.authChart.setOption({
          title: {
            text: 'Auth',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {},
          xAxis: {
            // data: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
            data: this.authX,
            axisTick: {
              show: false
            },
            axisLine: {
              show: true,
            },
            axisLabel: {
              interval: 0,
              rotate: 45,
              textStyle: {
                fontSize: '10',
                itemSize: ''
              }
            },
          },
          yAxis: {},
          series: [
            {
              // name: 'sales',
              type: 'bar',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#83bff6' },
                  { offset: 0.5, color: '#188df0' },
                  { offset: 1, color: '#188df0' }
                ])
              },
              emphasis: {
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#2378f7' },
                    { offset: 0.7, color: '#2378f7' },
                    { offset: 1, color: '#83bff6' }
                  ])
                }
              },
              label: {
                show: true,
                position: 'top',
                // textStyle:{
                // }
              },
              // data: [0, 0, 12, 106, 271, 351]
              data: this.authData
            }
          ]
        });
      },


      AttackComplex(elementId) {
        // initialize the echarts instance
        this.attackComplexChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.attackComplexChart.setOption({
          title: {
            text: 'AttackComplex',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {},
          xAxis: {
            // data: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
            data: this.attackComplexX,
            axisTick: {
              show: false
            },
            axisLine: {
              show: true,
            },
            axisLabel: {
              interval: 0,
              rotate: 45,
              textStyle: {
                fontSize: '10',
                itemSize: ''
              }
            },
          },
          yAxis: {},
          series: [
            {
              // name: 'sales',
              type: 'bar',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#83bff6' },
                  { offset: 0.5, color: '#188df0' },
                  { offset: 1, color: '#188df0' }
                ])
              },
              emphasis: {
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#2378f7' },
                    { offset: 0.7, color: '#2378f7' },
                    { offset: 1, color: '#83bff6' }
                  ])
                }
              },
              label: {
                show: true,
                position: 'top',
                // textStyle:{
                // }
              },
              // data: [0, 0, 12, 106, 271, 351]
              data: this.attackComplexData
            }
          ]
        });
      },


      ImpactConfidence(elementId) {
        // initialize the echarts instance
        this.impactConfidenceChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.impactConfidenceChart.setOption({
          title: {
            text: 'ImpactConfidence',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {},
          xAxis: {
            // data: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
            data: this.impactConfidenceX,
            axisTick: {
              show: false
            },
            axisLine: {
              show: true,
            },
            axisLabel: {
              interval: 0,
              rotate: 45,
              textStyle: {
                fontSize: '10',
                itemSize: ''
              }
            },
          },
          yAxis: {},
          series: [
            {
              // name: 'sales',
              type: 'bar',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#83bff6' },
                  { offset: 0.5, color: '#188df0' },
                  { offset: 1, color: '#188df0' }
                ])
              },
              emphasis: {
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#2378f7' },
                    { offset: 0.7, color: '#2378f7' },
                    { offset: 1, color: '#83bff6' }
                  ])
                }
              },
              label: {
                show: true,
                position: 'top',
                // textStyle:{
                // }
              },
              // data: [0, 0, 12, 106, 271, 351]
              data: this.impactConfidenceData
            }
          ]
        });
      },

      ImpactInteger(elementId) {
        // initialize the echarts instance
        this.impactIntegerChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.impactIntegerChart.setOption({
          title: {
            text: 'ImpactInteger',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {},
          xAxis: {
            // data: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
            data: this.impactIntegerX,
            axisTick: {
              show: false
            },
            axisLine: {
              show: true,
            },
            axisLabel: {
              interval: 0,
              rotate: 45,
              textStyle: {
                fontSize: '10',
                itemSize: ''
              }
            },
          },
          yAxis: {},
          series: [
            {
              // name: 'sales',
              type: 'bar',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#83bff6' },
                  { offset: 0.5, color: '#188df0' },
                  { offset: 1, color: '#188df0' }
                ])
              },
              emphasis: {
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#2378f7' },
                    { offset: 0.7, color: '#2378f7' },
                    { offset: 1, color: '#83bff6' }
                  ])
                }
              },
              label: {
                show: true,
                position: 'top',
                // textStyle:{
                // }
              },
              // data: [0, 0, 12, 106, 271, 351]
              data: this.impactIntegerData
            }
          ]
        });
      },


      ImpactAvailable(elementId) {
        // initialize the echarts instance
        this.impactAvailableChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.impactAvailableChart.setOption({
          title: {
            text: 'ImpactAvailable',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {},
          xAxis: {
            // data: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
            data: this.impactAvailableX,
            axisTick: {
              show: false
            },
            axisLine: {
              show: true,
            },
            axisLabel: {
              interval: 0,
              rotate: 45,
              textStyle: {
                fontSize: '10',
                itemSize: ''
              }
            },
          },
          yAxis: {},
          series: [
            {
              // name: 'sales',
              type: 'bar',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#83bff6' },
                  { offset: 0.5, color: '#188df0' },
                  { offset: 1, color: '#188df0' }
                ])
              },
              emphasis: {
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#2378f7' },
                    { offset: 0.7, color: '#2378f7' },
                    { offset: 1, color: '#83bff6' }
                  ])
                }
              },
              label: {
                show: true,
                position: 'top',
                // textStyle:{
                // }
              },
              // data: [0, 0, 12, 106, 271, 351]
              data: this.impactAvailableData
            }
          ]
        });
      },


      PublishDate(elementId) {
        // initialize the echarts instance
        this.publishDateChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.publishDateChart.setOption({
          title: {
            text: 'PublishDate',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {},
          xAxis: {
            // data: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
            data: this.publishDateX,
            axisTick: {
              show: false
            },
            axisLine: {
              show: true,
            },
            axisLabel: {
              interval: 0,
              rotate: 45,
              textStyle: {
                fontSize: '10',
                itemSize: ''
              }
            },
          },
          yAxis: {},
          series: [
            {
              // name: 'sales',
              type: 'bar',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#83bff6' },
                  { offset: 0.5, color: '#188df0' },
                  { offset: 1, color: '#188df0' }
                ])
              },
              emphasis: {
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#2378f7' },
                    { offset: 0.7, color: '#2378f7' },
                    { offset: 1, color: '#83bff6' }
                  ])
                }
              },
              label: {
                show: true,
                position: 'top',
                // textStyle:{
                // }
              },
              // data: [0, 0, 12, 106, 271, 351]
              data: this.publishDateData
            }
          ]
        });
      },

      TimeLine(elementId) {
        // initialize the echarts instance
        this.timeLineChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.timeLineChart.setOption({
          title: {
            text: 'TimeLine',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross',
              label: {
                backgroundColor: '#6a7985'
              }
            }
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [
            {
              type: 'category',
              boundaryGap: false,
              // data: ['02/01', '02/02', '02/03', '02/04', '02/05', '02/06', '02/07', '02/01', '02/02', '02/03', '02/04', '02/05', '02/06', '02/07', '02/08', '02/09', '02/10', '02/11', '02/12', '02/13', '02/14', '02/15', '02/16', '02/17', '02/18', '02/19', '02/20', '02/21', '02/22', '02/23', '02/24', '02/25', '02/26', '02/27', '02/28']
              data: this.timeLineX
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: [
            {
              // name: 'sales',
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 0
              },
              showSymbol: false,
              areaStyle: {
                opacity: 0.8,
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  {
                    offset: 0,
                    color: 'rgb(128, 255, 165)'
                  },
                  {
                    offset: 1,
                    color: 'rgb(1, 191, 236)'
                  }
                ])
              },
              emphasis: {
                focus: 'series'
              },
              // data: [120, 132, 101, 134, 90, 230, 210, 120, 132, 101, 134, 90, 230, 210, 120, 132, 101, 134, 90, 230, 210, 120, 132, 101, 134, 90, 230, 210, 30, 45, 66, 78, 90, 100, 109]
              data: this.timeLineData
            }
          ]
        });
      },

      C3BMIndex(elementId) {
        // initialize the echarts instance
        this.c3bIndexChart = echarts.init(document.getElementById(elementId));
        // Draw the chart
        this.c3bIndexChart.setOption({
          title: {
            text: 'C3BMIndex',
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross',
              label: {
                backgroundColor: '#6a7985'
              }
            }
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            // data: ['2018', '2019', '2020', '2021']
            type: 'category',
            boundaryGap: false,
            data: this.c3bmX
          },
          yAxis: [{
            type: 'value'
          }],
          series: [
            {
              // name: 'sales',
              type: 'line',
              smooth: true,
              lineStyle: {
                width: 0
              },
              showSymbol: false,
              areaStyle: {
                opacity: 0.8,
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  {
                    offset: 0,
                    color: 'rgb(55, 162, 255)'
                  },
                  {
                    offset: 1,
                    color: 'rgb(116, 21, 219)'
                  }
                ])
              },
              emphasis: {
                focus: 'series'
              },
              // data: [10, 15, 23, 37]
              data: this.c3bmData
            }
          ]
        });
      },


      /*3、以下为Compare页的函数*/
      getCompareData() {
        console.log('*****getCompareData*****')
        var that = this
        var cveid = this.selectCve.cveid

        console.log('getCompareData cveid:', cveid)
        // that.tableData.splice(0, that.tableData.length)
        that.tableData = []
        that.loadingForTable = true
        axios.post('common/comparedata', qs.stringify({ cveid: cveid })).then(res => {
          if (res.status == 200) {
            var ret = res.data
            // 遍历字典，将<@<符号替换成,
            for (var key in ret) {
              if (ret[key].indexOf('<@<')) {
                ret[key] = ret[key].replace(/<@</g, ', ')
              }
            }
            that.tableData.push({ database: 'EDB', product: ret.exploitdb_product, version: ret.exploitdb_version, component: ret.exploitdb_component, type: ret.exploitdb_vultype, root: ret.exploitdb_root, vector: ret.exploitdb_vector, impact: ret.exploitdb_impact })
            that.tableData.push({ database: 'IBM', product: ret.ibm_product, version: ret.ibm_version, component: ret.ibm_component, type: ret.ibm_vultype, root: ret.ibm_root, vector: ret.ibm_vector, impact: ret.ibm_impact })
            that.tableData.push({ database: 'NVD', product: ret.nvd_product, version: ret.nvd_version, component: ret.nvd_component, type: ret.nvd_vultype, root: ret.nvd_root, vector: ret.nvd_vector, impact: ret.nvd_impact })
            that.tableData.push({ database: 'OpenWall', product: ret.openwall_product, version: ret.openwall_version, component: ret.openwall_component, type: ret.openwall_vultype, root: ret.openwall_root, vector: ret.openwall_vector, impact: ret.openwall_impact })
            // 柱状图数据赋值
            that.loadingForTable = false
          }
        }).catch(err => {
          console.log("出错！具体错误为：", err)
          that.loadingForTable = false
        })
      },

      gotoPage(url, db) { // 用户点击该条CVE的数据库来源时
        // console.log('url:', url)
        var url = url
        // var html = this.getHtmlByUrls()
        // document.querySelector('.test').innerHTML = html
        this.$alert('', '标题名称', {
          title: db,
          confirmButtonText: 'OK',
          dangerouslyUseHTMLString: true,
          // callback: action => {
          //   this.$message({
          //     type: 'info',
          //     message: `action: ${action}`
          //   });
          // }
        })
        // window.open(url)
        // this.getHtmlByUrls()
      },
      gotoPageWarn(database) { // 当该条CVE不存在于点击的数据库中时，给出提示
        var data = database
        this.$message({
          message: 'No matching data has been found in this database: ' + data,
          type: 'warning'
        })
        // that.$message.error('没有查询到相应的数据');
      },
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .el-row {
    margin-bottom: 10px;
  }

  .contentTags,
  .miniContentTags {
    text-align: left;
    line-height: 1.5;
    font-size: 13px;
    font-weight: 600;
    font-family: sans-serif;
  }

  .miniContentTags {
    color: #595959;
  }

  .aloneRow {
    text-align: left;
    margin-left: 2%;
    line-height: 1.5;
  }

  .dashAloneRow {
    text-align: left;
    /* margin-left: 2%; */
    line-height: 1.5;
  }

  .text {
    line-height: 1.5;
    font-size: 14px;
    color: #595959;
  }

  >>>.el-tabs__item {
    font-size: 16px;
    font-family: sans-serif;
  }

  .square {
    width: 250px;
    height: 250px;
    margin: auto;
    /* background-color: #f5f5f5;
    border-radius: 50px; */
  }

  .rectangle {
    width: 800px;
    margin-left: 5%;
    height: 200px;
    /* background-color: darkkhaki; */
  }
</style>