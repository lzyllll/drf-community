# 示例
virtualenv venv
source venv/bin/activate
(venv) $ python -m pip install -U pip setuptools
(venv) $ pip install -U -r requirements.txt
(venv) $ python manage.py migrate
(venv) $ python manage.py runserver


# url设计 restful
- 文件相关 **DONE**
    - response
        - 其他：
            - /file/           GET 查看文件编号
            - /file/<int:pk>   GET 下载文件  
            - /image/    根据x,y(列表) 生成 mathplot图片，保存在临时内存，然后返回，自动下载
            - /file/load       POST content-type:multipart   
        - 文件相关的请求头
            - content-disposition
            - content-type
            - as-attachment
    - request
        - ``` python
            file = request.File.get()
            url = '自定义的保存路径'
            f = open(file.name,'wb')
            for a in f.chunks():
                f.write(a)
            f.close()
          ```

### 普通用户组

- 所有post,delete put 请求，都需authenticate权限
- 大部分 safe_method 都可以使用
    - 登录  **DONE**
        - 获取token，之后前端在请求头上加上
        - 使用drf中的 auth-token方法就行了
        - POST http://127.0.0.1:8000/api/login/  
    - 查看用户  **DONE**
        - 查询所有用户：GET /users/                 
        - 查询指定用户：GET /users/<int:pk>/        
        - 查看个人详细信息：GET /users/<int:pk>/detail/
            - (权限：isowner)
    - 用户所拥有的代码片段  **DONE**
        - /snippet/             
        - /snippet/<int:pk>/    

    - 活动
        - 活动相关
            - 查询所有活动：GET /activities/
            - 查看指定活动：GET /activities/<int:pk>/
            - 查看自身参加的活动：GET /activities/user/<int:user_id>/
        - 活动请求相关
            - 查看自己的活动请求情况：GET /activities/<int:pk>/request (参数：user_id,登录后，会自动根据request.user设置当前登录用户)
            - 申请活动请求：POST /activities/<int:pk>/request (参数：user_id,会自动根据request.user设置当前登录用户)
            - 取消活动请求：DELETE /activities/<int:pk>/request (参数：user_id,会自动根据request.user设置当前登录用户)

    - 查看社团 **DONE**
        - 查看所有社团：GET /departments/
        - 查看指定社团信息：GET /departments/<int:pk>/
        - 查看指定社团信息的成员：GET /departments/<int:pk>/members/
    - 社团申请请求 **DONE**
        - 查看所有的社团请求：GET /departments/<int:pk>/requests/
        - 添加请求：POST GET /departments/<int:pk>/requests/

    - 查看公共公告 
        - 所有的公告 GET /announcements/
        - 指定的公告 GET /announcements/<int:pk>
    - 查看社团的公告
        - 需要加入社团 在view中，会根据request.user 设置 dep_id,
            - 如果没有，会返回{detail:"你还没有加入社团"}
        - 所有公告 GET /departments/announcements/
        - 指定公告 GET /departments/announcements/<int:pk>

### 社团管理员用户组
- 所有功能都需要 isCommunityManager 权限
    - 成员  **DONE**
        - 删除成员：DELETE /departments/<int:pk>/members/<int:user_id>/
    - 社团请求 **DONE**
        - 查看所有的社团请求：GET /departments/<int:pk>/requests/
        - 允许申请社团的请求：POST /departments/<int:pk>/requests/<int:request_id>/approve
        - 拒绝申请社团的请求：POST /departments/<int:pk>/requests/<int:request_id>/reject
    - 公告
        - 本社团的公告
             - 发布公告 POST /departments/announcements/
             - 更改公告 PUT /departments/announcements/<int:pk>
             - 删除公告 DELETE /departments/announcements/<int:pk>
        - 查看社团管理员发布的公告
            - 所有公告   GET/departments/admin-announcements/
            - 指定的公告 GET/departments/admin-announcements/<int:pk>/
    - 打假条：
        
        


### 总管理员
- 权限：admin
- 拥有所有的权限
- 发布公共公告
    - 发布公告 GET /announcements/
    - 更改公告 PUT /announcements/<int:pk>
    - 删除公告 DELETE /announcements/<int:pk>
- 发布给社团管理员的公告
    - 发布公告 GET /admin-announcements/
    - 更改公告 PUT /admin-announcements/<int:pk>
    - 删除公告 DELETE /admin-announcements/<int:pk>


# 中间件
- connection-pools 连接池
- cosf 跨域，需要在setting中设置，允许的ip
- pageinator 分页,只有使用django混合类的方法，才会调用
- cache-redis 缓存
    - 查 检查是否有缓存，没有就更新
    - 增，删，改  删除缓存
- router_config
    - 读写分离
        - request.method in safemethod      读方法，使用A
        - request.method not in safemethod   写方法使用 B
        - 主从复制

# model设计

- user 使用django的
    - username: 用户名，用于登录的唯一标识符。
    - password: 密码，经过哈希加密后存储。
    - email: 邮箱地址。

- group 使用django的

- permission 使用django的

- TOEKN 使用drf的权限认证模块


- department 社团表 **DONE**
    - pk
    - name
    - description
    - created 
    - admin_user_pk

- DepartMember 用户参加的社团表
    - pk
    - user_pk
    - department_pk
    - joined_date
    - 不允许重复(user_pk和department_pk的组合)

- DepartMemberRequest
    - pk
    - user_pk
    - department_pk
    - request_date
    - status
    - 不允许重复(user_pk和department_pk的组合)

- activity
    - pk
    - name
    - begin_date
    - end_date
    - score
    - description

- UserActivityRequest
    - pk
    - content
    - user_pk
    - activity_pk
    - publish_date

- UserActivty
    - pk
    - user_pk
    - activity_pk
    - joined_date

- DepartmentAnnouncements
    - pk
    - content
    - title
    - department_pk

- PublicAnnouncements
    - pk
    - content
    - title
    
- AdminAnnouncements
    - pk
    - content
    - title


# 返回json，序列化设计

其他的全部返回全部字段,直接meta，设置数据库就够了
然后设置对应只可读字段

特殊的需要联表：
- 查询本人参加的活动
    - user的所有字段
    - 所参加活动的id（group_concat）  serializers.PrimaryKeyRelatedField(many=True, queryset=Activity.bjects.all())



