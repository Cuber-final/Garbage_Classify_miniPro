// app.js
App({

  globals: {
    user_name:"ssuser",
  },

  updateInfo(obj){
    this.globals.user_name=obj;
    console.log(this.globals.user_name);
  }
})

//登录成功后修改全局变量User_name，无需利用缓存机制