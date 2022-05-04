// explore/pages/result/index.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    result: {},
    cateImg: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/",
    img_url: ""
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var result = wx.getStorageSync('result')
    // console.log(result);
    this.setData({
      result: result
    })
    var img_url = this.data.cateImg + result['pc_name'] + '.webp'
    this.setData({
      img_url: img_url
    })
    // console.log(result);
  },
  /**
   * 退出该页面时删除对应的搜索记录缓存
   */
  onUnload: function () {
    wx.removeStorageSync('result')
  },

})