// app.js
App({

  globals: {
    user_name: "user",
    stat1: "empty",
    stat2: "visitor",
    stat3: "user"
  },


  hint_login() {
    var stat = wx.getStorageSync('use_status')
    var that = this
    if (stat == this.globals.stat1) {
      wx.showModal({
        title: '登录提示',
        content: '请登录',
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
            wx.setStorageSync('username', 'visitor')
            wx.setStorageSync('use_status', that.globals.stat2)
          }
        }
      })
    }
  },

  onLaunch(options) {
    // 不能一次存多个不同的键值对
    try {
      wx.setStorageSync('username', '用户')
    } catch (e) {
      console.log("用户信息设置错误");
    };

    try {
      wx.setStorageSync('use_status', "empty")
    } catch (e) {
      console.log("使用身份设置错误");
    };
    // 设置延时弹窗提示
    setTimeout(this.hint_login, 2000)
  },
})