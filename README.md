# 基于 Flask 的论坛
[点击访问论坛](http://www.skyroom.club)
> 测试账号 用户名：arm 密码：123

- 实现话题浏览和发表（支持 Markdown），评论回复，用户主页，个人信息维护功能
- 其中私信、@提醒、邮件密码找回功能，使用了基于Celery消息队列的邮件发送功能进行实现
- 通过配置多 worker和gevent协程的Gunicorn实现程序的负载均衡运行，并使用Supervisor进行进程管理
- 使用Redis实现登录Session和页面token在多进程下的数据共享，和用于缓存计算耗时长的数据结果
- 使用 Jinja2 的模板继承功能复用通用页面元素
- 通过MySQL进行数据储存，使用sqlalchemy实现了 ORM，支持JOIN操作解决N + 1问题，支持事务功能
- 使用Nginx做反向代理，提高静态资源、用户文件的访问性能
- 支持对 XSS、CSRF 和SQL 注入等攻击的防御
- 可用 bash自动部署脚本，实现在服务器的一键部署


----------

- 登录操作
![](https://raw.githubusercontent.com/Armrun/Flask--bbs1.1/master/git%E5%9B%BE/bbs_login.gif)

----------

- 修改个人信息
![](https://raw.githubusercontent.com/Armrun/Flask--bbs1.1/master/git%E5%9B%BE/web_set.gif)

----------

- 找回密码
![](https://raw.githubusercontent.com/Armrun/Flask--bbs1.1/master/git%E5%9B%BE/reset_pass.gif)





 
