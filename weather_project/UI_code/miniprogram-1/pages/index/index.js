//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    weather:null
  },
  submit: function (e) {
    var city = e.detail.value.city
    console.log(city)
    this.getWeather(city)
  },
  onLoad: function () {
    //var city = null
    //var city = app.globalData.userInfo.city.toLowerCase()
    //this.getWeather(city)
  },
  onGotUserInfo: function (e) {
    var that = this
    /*if (that.userCity != null)
    {
      console.log(that.userCity)
      wx.showModal({
        title: '提示',
        content: '已得到您的居住地址！不需要重复获取',
        success: function (res) {
          if (res.confirm) {//这里是点击了确定以后
            console.log('用户点击确定')
          } else {//这里是点击了取消以后
            console.log('用户点击取消')
          }
        }
      })
      return
    }*/
    console.log(e.detail.errMsg)
    console.log(e.detail.userInfo)
    console.log(e.detail.rawData)
    that.userCity = e.detail.userInfo.city.toLowerCase()
    if (that.userCity == '')
    {
      wx.showModal({
        title: '提示',
        content: '您的地区还未添加/还未更新，请直接输入城市后点击“查询其他城市天气”',
        success: function (res) {
          if (res.confirm) {//这里是点击了确定以后
            console.log('用户点击确定')
          } else {//这里是点击了取消以后
            console.log('用户点击取消')
          }
        }
      })
      return
    }
    this.getWeather(that.userCity)
  },
  getWeather: function (city) {
    var that = this;
    if(city=='')
    {
      wx.showModal({
        title: '提示',
        content: '您未输入任何城市！，请重新输入，如北京、上海、广州等',
        success: function (res) {
          if (res.confirm) {//这里是点击了确定以后
            console.log('用户点击确定')
          } else {//这里是点击了取消以后
            console.log('用户点击取消')
          }
        }
      })
      return
    }
    wx.request({
      //url: 'http://175.24.55.162:5000/weather?city=' + city,
      url: 'https://serverzy.top/weather?city=' + city,
      success: (res) => {
        console.log(res);
        if ((res.data) == null)
        {
          wx.showModal({
            title: '提示',
            content: '您输入的城市不存在，请输入其他城市，如北京、上海、广州等',
            success: function (res) {
              if (res.confirm) {//这里是点击了确定以后
                console.log('用户点击确定')
              } else {//这里是点击了取消以后
                console.log('用户点击取消')
              }
            }
          })
        }
        if (res.data) {
          that.setData(
            { weather: res.data }
          )
        }
      }
    })
  }
})
