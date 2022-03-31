// index.js
Page({
  data: {
    bgImage: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/backGround.63auyo6meuk0.webp",
    icon_camera: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/camera.2fh3b8wvhtz4.webp",
    icon_search: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/search.16og5blts6io.webp",
    icon_reset: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/rb.3ddr0cwe94u0.webp",
    tab_two: "/pages/search/index",
    search_info: "",
  },

  onShow: function (params) {
    this.setData({
      search_info: ""
    })
  },
  toSearch: function (e) {
    var stat = wx.getStorageSync('use_status')
    // console.log(this.data.search_info);
    var info = this.data.search_info
    wx.request({
      url: 'http://127.0.0.1:4093/api/search/text',
      method: 'POST',
      data: {
        'stat': stat,
        'content': info
      },
      success(res) {
        wx.setStorageSync('result', res.data)
        wx.navigateTo({
          url: '/explore/pages/result/index',
        })
      }
    })
  },

  //监听输入框的数据并实时更新
  inputListener: function (e) {
    var info = e.detail.value;
    // console.log(info);
    this.setData({
      search_info: info
    })
  },

  resetInput: function () {
    this.setData({
      search_info: ""
    })
  },

  topTop: function () {
    wx.showModal({
      title: '文字搜索',
      content: '若使用该功能，请先登录',
      cancelText: '游客模式',
      confirmText: '登录',
      success(res) {
        if (res.confirm) {
          console.log('跳转到登录页面')
          wx.navigateTo({
            url: '/pages/userCenter/login',
          })
        } else if (res.cancel) {
          console.log('进入游客模式')
          wx.setStorageSync('username', '游客')
          wx.setStorageSync('use_status', 'visitor')
        }
      }
    })
  }
})