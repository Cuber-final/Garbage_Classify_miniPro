// pages/userCenter/index.js
Page({

  /**
   * 页面的初始数据
   */

  data: {
    bimgA: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/history.1r170mg6lu1.webp",
    bimgB: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/notes.3gsxfncueww0.webp",
    avatar: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/user.1xn7dwcjf000.webp",
    toHistory: "",
    wx_name: "",
    toHistory: "/explore/pages/history/index",
    toDocs: "/explore/pages/docs/index"
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    try {
      var value = wx.getStorageSync('username')
      // console.log(value)
      this.setData({
        wx_name: value
      })
    } catch (e) {}
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {},
  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})