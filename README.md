# Winterfell
一个小的英语笔记系统的server端

#模块
##用户模块

用户模块包含用户的一些基本功能,主要有:
<ul>
<li>用户注册</li>
<li>用户登录</li>
<li>修改信息</li>
<li>后台管理,包括删除账号,禁用账号</li>
</ul>

##词汇模块
词汇模块包含:
<ul>
<li>添加词汇,包括原词,释义,原句,例句,造句;例句和造句可以有多个</li>
<li>删除词汇</li>
<li>查询词汇</li>
	<ul>
	<li>根据原词查询</li>
	<li>根据添加时间查询</li>
	<li>根据添加的时间段查询</li>
	<li>根据释义查询</li>
	</ul>
</ul>

#数据库设计

使用mysql存储用户信息,user表如下:<br/>
<pre>
+---------------+-------------+------+-----+---------+----------------+
| Field         | Type        | Null | Key | Default | Extra          |
+---------------+-------------+------+-----+---------+----------------+
| user_id       | int         | NO   | MUL | NULL    |auto_increment  |
| user_name     | varchar(64) | NO   |     | NULL    |                |
| user_nicename | varchar(64) | NO   |     | NULL    |                |
| user_email    | varchar(64) | NO   |     | NULL    |                |
| user_pass     | varchar(64) | NO   |     | NULL    |                |
+---------------+-------------+------+-----+---------+----------------+
</pre>

在词汇存储中,例句,造句的个数都是不定的,所以采用NoSQL数据库,这里使用mongoDB数据库
在存储时,除了词汇的基本信息外,还应包括存储时间(采用系统时间),存储用户id

#技术栈

<ul>
<li>flask</li>
<li>mongodb</li>
<li>mysql</li>
</ul>

