// pages/search/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    active: 0,
    active_id: 40,
    pc_set: [],
    tc_set: [],
  },

  onLoad: function (options) {
    var that = this
    var host=wx.getStorageSync('hostpIp')
    wx.request({
      url: host+'/api/search/getCates',
      method: 'GET',
      success(res) {
        // console.log(res.data)
        var cate_set = res.data
        that.setData({
          pc_set: cate_set
        })
      }
    })
    this.getCateList()
  },

//重新回到该页时会保证最新数据
  onShow: function () {
    var that = this
    var host=wx.getStorageSync('hostIp')
    wx.request({
      url: host+'/api/search/getCates',
      method: 'GET',
      success(res) {
        // console.log(res.data)
        var cate_set = res.data
        that.setData({
          pc_set: cate_set
        })
      }
    })
    this.getCateList()
  },

  changeActive: function (e) {
    //console.log(e);
    var cur_index = e.target.dataset.id
    var cur_pcId = e.target.dataset.tcid
    // console.log(e.target.dataset);
    this.setData({
      active: cur_index,
      active_id: cur_pcId
    })
    this.getCateList()
  },

  getCateList: function () {
    var that = this
    var host=wx.getStorageSync('hostIp')
    // console.log(that.data.active_id);
    wx.request({
      url: host+'/api/search/getCates',
      method: 'POST',
      data: {
        "tcId": that.data.active_id
      },
      success(res) {
        var data_list = res.data
        that.setData({
          tc_set: data_list
        })
      }
    })
  }
})