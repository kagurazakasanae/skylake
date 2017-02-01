# Skylake WebServer

### Version 0.1

> ## Warning: This project is still in developing progress, it may(should) be unstable, do not use this on production environment.
> ## 警告：这个项目仍在开发中，应(ken)该(ding)会不稳定，请不要在正式环境中使用。
 
Skylake is a python-based non-blocking(only on unix),low performance webserver. 

Skylake是一个Python语言编写的非阻塞式(仅限unix下)的低性能webserver。

In this version, it only supports static files and CGI

在当前版本,仅做支持静态文件服务器或CGI服务器

To customize server, edit "SkylakeConfig.py", find "def get_server_config():", these are configurations of this webserver. An configuration has already been putted in it. It's possible to run this server just by changing 'LOG_PATH' and 'HOME_PATH' to yours

To run this server, run "test.py"

