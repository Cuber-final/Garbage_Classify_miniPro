// pages/userCenter/index.js
Page({

  /**
   * 页面的初始数据
   */

  data: {
    bimgA: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/history.1r170mg6lu1.webp",
    bimgB: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/notes.3gsxfncueww0.webp",
    avatar: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/user.1xn7dwcjf000.webp",
    wx_name: '',
    toHistory: "/explore/pages/history/index",
    toDocs: "/explore/pages/docs/index",
    toLogin: "/pages/userCenter/login",
    use_status: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    try {
      var value = wx.getStorageSync('username')
      var stat = wx.getStorageSync('use_status')
      // console.log(value)
      this.setData({
        wx_name: value,
        use_status: stat
      })
    } catch (e) {}
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    try {
      var value = wx.getStorageSync('username')
      var stat = wx.getStorageSync('use_status')
      // console.log(value)
      this.setData({
        wx_name: value,
        use_status: stat
      })
    } catch (e) {}
  },

  access: function (params) {
    if (this.data.use_status == 'visitor') {
      wx.showToast({
        title: '请先登录',
        icon: 'none',
        duration: 1500,
      })
    } else {
      wx.navigateTo({
        url: this.data.toHistory,
      })
    }
  }
})