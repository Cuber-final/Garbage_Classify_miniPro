// pages/userCenter/login.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    avatar: "https://cdn.jsdelivr.net/gh/Cuber-final/myblog_statics@master/mini_pro/user.1xn7dwcjf000.webp",
  },

  formApi(btn_id, form_data) {
    var username = form_data["input_username"]
    // console.log(username)
    var password = form_data["input_password"]
    // console.log(password)
    if (btn_id == "login-btn") {
      console.log("login");
      wx.request({
        method: 'POST',
        url: 'http://127.0.0.1:4093/api/login',
        data: {
          "username": username,
          "password": password
        },
        success(res) {
          var fb_msg = res.data['fb_msg']
          console.log(fb_msg)
          var toast_msg = "用户名或密码错误，请检查"
          if (fb_msg == 'success') {
            toast_msg = "登录成功"
            wx.setStorageSync('username', username)
            wx.setStorageSync('use_status', "user")
            wx.switchTab({
              url: '/pages/home/index',
            })
          }
          wx.showToast({
            title: toast_msg,
            icon: 'none',
            duration: 1500,
          })
        },
        fail(res) {
          console.log("调用接口失败");
        }
      })
    } else {
      console.log("register");
      wx.request({
        method: 'POST',
        url: 'http://127.0.0.1:4093/api/register',
        data: {
          "username": username,
          "password": password
        },
        success(res) {
          var fb_msg = res.data['fb_msg']
          console.log(fb_msg)
          var toast_msg = "用户名已存在"
          if (fb_msg == 'success') {
            toast_msg = "注册成功"
            wx.setStorageSync('username', username)
            wx.setStorageSync('use_status', "user")
            wx.switchTab({
              url: '/pages/home/index',
            })
          }
          wx.showToast({
            title: toast_msg,
            icon: 'none',
            duration: 1500,
          })
        },
        fail(res) {
          console.log("调用接口失败");
        }
      })
    }
  },

  formSubmit(e) {
    // 通过提交按钮的ID来区分登录与注册的使用
    // console.log(e.detail.target["id"])
    //获取表单的数据
    var btn_id = e.detail.target["id"]
    var form_data = e.detail.value
    this.formApi(btn_id, form_data)
  },

  formReset(e) {
    console.log('form发生了reset事件，携带数据为：', e.detail.value)
    this.setData({
      chosen: ''
    })
  }
})