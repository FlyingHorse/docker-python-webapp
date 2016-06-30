# docker-python-webapp
第一个基于docker的python webapp.  python + mysql

>其中webapp源于[廖雪峰教程](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001397616003925a3d157284cd24bc0952d6c4a7c9d8c55000)
中示例，这里将其部署到docker

##安装docker
##部署mysql容器
###启动mysql容器

>docker run --name mysql -v /Users/liuyangyang/workspace/datadir:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7

###登录mysql容器创建数据库

>docker exec -it mysql bash

###查看mysql容器ip

>docker network inspect bridge

##配置python中web app
##run python app
