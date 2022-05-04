// explore/pages/history/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    res_list: [],
    res_msg: '历史记录'
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var username = wx.getStorageSync('username')
    this.getHistory(username)
  },
  getHistory: function (username) {
    var that = this
    var host = wx.getStorageSync('hostIp')
    wx.request({
      url: host + '/api/user/history',
      method: 'POST',
      data: {
        'username': username
      },
      success(res) {
        // console.log(res.data[0]['code']);
        var fb_code = res.data[0]['code']
        if (fb_code == 1) {
          that.setData({
            res_list: res.data
          })
        } else {
          that.setData({
            res_msg: '该用户无历史记录'
          })
        }
      }
    })
  }
})