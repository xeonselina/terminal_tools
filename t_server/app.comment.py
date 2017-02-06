"""
    @api {post} /terminal/ sqlite语句
    @apiGroup TerminalServer Terminal
    @apiName  sqlite语句

    @apiDescription 推送sqlite命令到终端
    @apiParam {String} tid 发送到哪台终端
    @apiParam {String} wid 哪个web会话发送来的消息
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    
    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"sqlite","param":{"query":"select * from t_app_version;"}}

    @apiSuccess {Boolean} result false or false 
    
    @apiSuccessExample {json} 注册
        {"result":true}
"""

"""
    @api {post} /terminal/ mysql语句
    @apiGroup TerminalServer Terminal

    @apiName  mysql语句

    @apiDescription 推送mysql语句到终端
    @apiParam {String} tid 发送到哪台终端
    @apiParam {String} wid 哪个web会话发送来的消息
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数，需要base64编码
    
    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"mysql","param":{"query":"select * from t_app_version;"}}

    @apiSuccess {Boolean} result false or false 
    
"""

"""
    @api {post} /terminal/ dir
    @apiGroup TerminalServer Terminal

    @apiName  dir

    @apiDescription 列出指定路径的目录(单层)
    @apiParam {String} tid 发送到哪台终端
    @apiParam {String} wid 哪个web会话发送来的消息
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    
    @apiParamExample {json} dir 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"dir","param":{"path":"d:\\ez\\app\\","pattern":"*.txt"}}

    @apiSuccess {Boolean} result false or false 
    
"""

"""
    @api {post} /terminal/ execute cmd
    @apiGroup TerminalServer Terminal

    @apiName  execute cmd

    @apiDescription 执行指定cmd命令
    @apiParam {String} tid 发送到哪台终端
    @apiParam {String} wid 哪个web会话发送来的消息
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    
    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"cmd","param":"mkdir 123"}

    @apiSuccess {Boolean} result false or false 
"""

"""
    @api {post} /terminal/ upload
    @apiGroup TerminalServer Terminal

    @apiName upload 

    @apiDescription 让终端发送指定文件到指定url
    @apiParam {String} tid 发送到哪台终端
    @apiParam {String} wid 哪个web会话发送来的消息
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    
    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"upload","param":{"path":["filepath1","filepath2"],"url":"http://123.123.123.123/upload"}

    @apiSuccess {Boolean} result false or false 
"""

"""
    @api {post} /terminal/ download
    @apiGroup TerminalServer Terminal

    @apiName download 

    @apiDescription 让终端到制定url下载指定文件并放到指定位置
    @apiParam {String} tid 发送到哪台终端
    @apiParam {String} wid 哪个web会话发送来的消息
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    
    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"download","param":{"url":"http://123.123.123.123/download.zip","path":"d:/ez/unzip/download.zip"}}

    @apiSuccess {Boolean} result false or false 
"""

"""
    @api {post} /terminal/ grep
    @apiGroup TerminalServer Terminal

    @apiName grep 

    @apiDescription 搜索指定文件
    @apiParam {String} tid 发送到哪台终端
    @apiParam {String} wid 哪个web会话发送来的消息
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    
    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"grep","param":{"reg":".*?zip","path":"d:/ez/unzip/*.log"}}

    @apiSuccess {Boolean} result false or false 
"""

"""
    @api {post} /terminal/ cat
    @apiGroup TerminalServer Terminal

    @apiName cat 

    @apiDescription 打开指定文件
    @apiParam {String} tid 发送到哪台终端
    @apiParam {String} wid 哪个web会话发送来的消息
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    
    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"cat","param":"d:/ez/unzip/note.txt"}

    @apiSuccess {Boolean} result false or false 
"""

"""
    @api {post} /terminal/ list sys log
    @apiGroup TerminalServer Terminal

    @apiName 列出系统日志和内容

    @apiDescription 使用正则表达式搜索指定目录
    @apiParam {String} tid 发送到哪台终端
    @apiParam {String} wid 哪个web会话发送来的消息
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    
    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"ls_sys_log","param":{"start_time":"2016-05-05 00:00:01","start_pos":0,"count":50}}

    @apiSuccess {Boolean} result false or false 
"""

"""
客户端发往服务器
"""

"""
    @api {ws} /server/ reg
    @apiGroup TerminalServer server

    @apiName reg
    @apiDescription 终端向T_server注册
    @apiParam {String} tid 来自哪台终端
    @apiParam {String} wid 发给哪个web会话，可空
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    @apiSuccess {Boolean} result true or false 

    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"reg","param":"518067N123"}

"""

"""
    @api {ws} /server/ sql_resp
    @apiGroup TerminalServer server
    @apiName sql response
    @apiDescription 查询mysql或sqlite的回复
    @apiParam {String} tid 来自哪台终端
    @apiParam {String} wid 发给哪个web会话，可空
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    @apiSuccess {Boolean} result true or false 

    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"sql_resp","param":[{"result": Ture,"data":{"id":"123","name":"name123","desc":"查询出来的数据"}}]}

"""

"""
    @api {ws} /server/ upload_fin
    @apiGroup TerminalServer server
    @apiName upload fin
    @apiDescription 上传文件结束
    @apiParam {String} tid 来自哪台终端
    @apiParam {String} wid 发给哪个web会话，可空
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    @apiSuccess {Boolean} result true or false 

    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"upload_fin","param":false}

"""

"""
    @api {ws} /server/ download_fin
    @apiGroup TerminalServer server
    @apiName download fin
    @apiDescription 下载文件结束
    @apiParam {String} tid 来自哪台终端
    @apiParam {String} wid 发给哪个web会话，可空
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    @apiSuccess {Boolean} result true or false 

    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"download_fin","param":false}
"""

"""
    @api {ws} /server/ dir_resp
    @apiGroup TerminalServer server
    @apiName dir response
    @apiDescription dir的回复
    @apiParam {String} tid 来自哪台终端
    @apiParam {String} wid 发给哪个web会话，可空
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    @apiSuccess {Boolean} result true or false 

    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"dir_resp","param":{"result":True,"msg":"err msg","list":[{"type":"file","name":"app.exe","full_name":"d:\\ez\\app.exe","create_date":"2016-05-01 00:00:00","update_date":"2016-05-01 00:00:00","size":"12mb"}]}}
"""

"""
    @api {ws} /server/ cmd_resp
    @apiGroup TerminalServer server
    @apiName cmd response 
    @apiDescription 执行cmd的回复
    @apiParam {String} tid 来自哪台终端
    @apiParam {String} wid 发给哪个web会话，可空
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    @apiSuccess {Boolean} result true or false 

    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"cmd_resp","param":"结果一大串\\r\\n结果一大串"}
"""

"""
    @api {ws} /server/ cat_resp
    @apiGroup TerminalServer server
    @apiName  cat response 
    @apiDescription cat的回复
    @apiParam {String} tid 来自哪台终端
    @apiParam {String} wid 发给哪个web会话，可空
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    @apiSuccess {Boolean} result true or false 

    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"cat","param":"结果一大串\\r\\n结果一大串"}
"""

"""
    @api {ws} /server/ grep_resp
    @apiGroup TerminalServer server
    @apiName grep response
    @apiDescription grep的回复
    @apiParam {String} tid 来自哪台终端
    @apiParam {String} wid 发给哪个web会话，可空
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    @apiSuccess {Boolean} result true or false 

    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"grep_resp","param":"结果结果结果"}
"""

"""
    @api {ws} /server/ list_sys_log_resp
    @apiGroup TerminalServer server
    @apiName list_sys_log response
    @apiDescription 系统日志回复
    @apiParam {String} tid 来自哪台终端
    @apiParam {String} wid 发给哪个web会话，可空
    @apiParam {String} cid 命令id 
    @apiParam {String} cmd 
    @apiParam {Object} param 参数
    @apiSuccess {Boolean} result true or false 

    @apiParamExample {json} 注册 
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"dir_resp","param":[{"time":"2016-05-01 00:00:00","level":"error","title":"application error","content":"一大堆"}]}
"""

"""
    @api {ws} /server/ heartbeat
    @apiGroup TerminalServer server
    @apiName heartbeat
    @apiDescription 终端心跳
    @apiParam {String} tid 来自哪台终端
    @apiParam {String} wid 发给哪个web会话，可空
    @apiParam {String} cid 命令id
    @apiParam {String} cmd
    @apiParam {Object} param 参数
    @apiSuccess {Boolean} result true or false

    @apiParamExample {json} 注册
            {"tid":"518067N33","wid":"w123","cid":"c123","cmd":"hb","param":null}
"""
