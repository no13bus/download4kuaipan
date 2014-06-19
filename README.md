download4kuaipan

===================

1.使用下面的命令直接安装必要的包
pip install -r requirement.txt

2.首先你要有金山快盘的账户 然后到这个[地址](http://www.kuaipan.cn/developers)申请快盘的开发平台的应用
创建应用后就能得到consumer_key consumer_secret。然后执行python Kuaipan_OAuth.py即可在命令行的提示下最终得到oauth_token oauth_token_secret
这2个值。然后将config.py里面的相关配置修改性下
