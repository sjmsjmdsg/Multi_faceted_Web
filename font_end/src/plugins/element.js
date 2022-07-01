import Vue from 'vue'
import 'echarts-wordcloud'

import {
  Container,
  Header,
  Aside,
  Main,
  Footer,
  Row,
  Col,
  Input,
  Button,
  Tree,
  Menu,
  MenuItem,
  MenuItemGroup,
  Submenu,
  Radio,
  RadioGroup,
    Checkbox,
    CheckboxGroup,
    Pagination,
  Select,
  Option,
  OptionGroup,
  Card,
  Tag,
  Tabs,
  TabPane,
  Divider,
  Loading,
  Message,
  MessageBox,
  Table,
  TableColumn,
  Tooltip,
  Notification,
  Popover,
  Empty
} from 'element-ui'

Vue.use(Empty)
Vue.use(Popover)
Vue.use(Tooltip)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Loading.directive)
Vue.use(MenuItemGroup)
Vue.use(Divider)
Vue.use(Tabs)
Vue.use(TabPane)
Vue.use(Tag)
Vue.use(Card)
Vue.use(Option)
Vue.use(OptionGroup)
Vue.use(Select)
Vue.use(Radio)
Vue.use(RadioGroup)
Vue.use(Checkbox)
Vue.use(CheckboxGroup)
Vue.use(Pagination)
Vue.use(Menu)
Vue.use(MenuItem)
Vue.use(Submenu)
Vue.use(Tree)
Vue.use(Button)
Vue.use(Header)
Vue.use(Container)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Footer)
Vue.use(Row)
Vue.use(Col)
Vue.use(Input)


// 把弹窗组件挂载到vue的原型对象上
Vue.prototype.$message = Message
// 在vue原型对象上挂载confirm
Vue.prototype.$confirm = MessageBox.confirm
Vue.prototype.$alert = MessageBox.alert

Vue.prototype.Notification = Notification