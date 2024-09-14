### 五、vless节点搭建

#### 1，确保已经开启权限

第一步需要做的就是开启可以运行自己应用的权限。`Additional services` -> `Run your own applications` -> `Enabled` 如果不开启这一项，自己的用户目录下的所有文件都无法添加可执行权限。

#### 2，配置端口号

- 按顺序打开添加端口号`Port reservation`->`Add port`->`Random`->`add`

#### 3，ssh 进入服务器

```shell
#s6.serv00.com可能会因为被墙连不上,可以用web6.serv00.com或者cache6.serv00.com
ssh -p 22 <Login>@<SSH/SFTP服务器地址> 
```

如果不会使用终端可采用其他ssh工具或者[webssh](https://ssh.hax.co.id/)，只需要输入账号密码端口即可

#### 4，拉取代码到指定目录

```shell
cd ~/domains && git clone https://github.com/yixiu001/serv00-script.git && cd serv00-script && bash vless.sh
```

#### 5，执行命令

```shell
cd ~/domains/$USER.serv00.net/vless && ./check_vless.sh -p <端口号>
```

#### 6，复制信息中返回的vless信息并粘贴到v2ray中使用

```shell
# 退出登录，重新进行ssh连接再使用pm2
exit
```

#### 7，配置定时任务维护节点

在面板中依次打开`Cron jobs`->`Add cron job`->`Specify time`选择每小时执行一次`Hourly`->`Command`中输入以下命令

```shell
cd ~/domains/$USER.serv00.net/vless && ./check_vless.sh
```

### 六、其他常用命令

#### 1，删除vless节点代码以及进程关闭

```shell
pm2 delete vless && rm -rf ~/domains/serv00-script && rm -rf ~/domains/$USER.serv00.net/vless
```

#### 2，查看当前vless节点状态

```shell
pm2 status
# 如果状态异常可以执行以下命令重启
cd ~/domains/$USER.serv00.net/vless && ./check_vless.sh
```

#### 3，查看错误日志

如果出现异常可以执行以下命令查看日志截图发到[TG群聊](https://t.me/yxjsjl)解决

```shell
pm2 logs
```

后续其他命令修改待更新！！！
