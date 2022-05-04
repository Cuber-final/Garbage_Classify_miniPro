// index.js
Page({
  data: {
    bgImage: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/homeBg.kxydtlsdm3k.webp",
    icon_camera: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/camera.2fh3b8wvhtz4.webp",
    icon_search: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/search.16og5blts6io.webp",
    icon_reset: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/rb.3ddr0cwe94u0.webp",
    tab_two: "/pages/search/index",
    search_info: "",
    postA: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/postA.webp",
    postB: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/postC.webp",
    postC: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/class_demo.webp"
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
    var host = wx.getStorageSync('hostIp')
    var username = wx.getStorageSync('username')
    wx.request({
      url: host + '/api/search/text',
      method: 'POST',
      data: {
        'stat': stat,
        'content': info,
        'username': username
      },
      success(res) {
        wx.setStorageSync('result', res.data)
        wx.navigateTo({
          url: '/explore/pages/result/index',
        })
      }
    })
  },

  camera: function () {
    wx.chooseImage({
      count: 1,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success(res) {
        // tempFilePath可以作为img标签的src属性显示图片
        const tempFilePaths = res.tempFilePaths
        var host = wx.getStorageSync('hostIp')
        // console.log(tempFilePaths);
        wx.uploadFile({
          url: host + '/api/search/camera',
          filePath: tempFilePaths[0],
          name: 'file',
          method: 'POST',
          formData: {
            // 设置用户
            'username': 'userB',
          },
          success(res) {
            // console.log(res);
            var data=JSON.parse(res.data)
            // console.log(data);
            wx.setStorageSync('result', data)
            // setTimeout(() => {}, 6000);
            wx.navigateTo({
              url: '/explore/pages/result/index',
            })
          }
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