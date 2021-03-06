define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./apidoc/main.js",
    "group": "C__Users_jimmy_pan_Documents_Project_SVN_Estation_terminal_tool_t_server_apidoc_main_js",
    "groupTitle": "C__Users_jimmy_pan_Documents_Project_SVN_Estation_terminal_tool_t_server_apidoc_main_js",
    "name": ""
  },
  {
    "type": "post",
    "url": "/terminal/",
    "title": "list sys log",
    "group": "TerminalServer_Terminal",
    "name": "_________",
    "description": "<p>使用正则表达式搜索指定目录</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>发送到哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>哪个web会话发送来的消息</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"ls_sys_log\",\"param\":{\"start_time\":\"2016-05-05 00:00:01\",\"start_pos\":0,\"count\":50}}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>false or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_Terminal"
  },
  {
    "type": "post",
    "url": "/terminal/",
    "title": "cat",
    "group": "TerminalServer_Terminal",
    "name": "cat",
    "description": "<p>打开指定文件</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>发送到哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>哪个web会话发送来的消息</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"cat\",\"param\":\"d:/ez/unzip/note.txt\"}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>false or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_Terminal"
  },
  {
    "type": "post",
    "url": "/terminal/",
    "title": "dir",
    "group": "TerminalServer_Terminal",
    "name": "dir",
    "description": "<p>列出指定路径的目录(单层)</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>发送到哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>哪个web会话发送来的消息</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "dir ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"dir\",\"param\":{\"path\":\"d:\\\\ez\\\\app\\\\\",\"pattern\":\"*.txt\"}}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>false or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_Terminal"
  },
  {
    "type": "post",
    "url": "/terminal/",
    "title": "download",
    "group": "TerminalServer_Terminal",
    "name": "download",
    "description": "<p>让终端到制定url下载指定文件并放到指定位置</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>发送到哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>哪个web会话发送来的消息</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"download\",\"param\":{\"url\":\"http://123.123.123.123/download.zip\",\"path\":\"d:/ez/unzip/download.zip\"}}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>false or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_Terminal"
  },
  {
    "type": "post",
    "url": "/terminal/",
    "title": "execute cmd",
    "group": "TerminalServer_Terminal",
    "name": "execute_cmd",
    "description": "<p>执行指定cmd命令</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>发送到哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>哪个web会话发送来的消息</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"cmd\",\"param\":\"mkdir 123\"}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>false or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_Terminal"
  },
  {
    "type": "post",
    "url": "/terminal/",
    "title": "grep",
    "group": "TerminalServer_Terminal",
    "name": "grep",
    "description": "<p>搜索指定文件</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>发送到哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>哪个web会话发送来的消息</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"grep\",\"param\":{\"reg\":\".*?zip\",\"path\":\"d:/ez/unzip/*.log\"}}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>false or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_Terminal"
  },
  {
    "type": "post",
    "url": "/terminal/",
    "title": "mysql语句",
    "group": "TerminalServer_Terminal",
    "name": "mysql__",
    "description": "<p>推送mysql语句到终端</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>发送到哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>哪个web会话发送来的消息</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"mysql\",\"param\":{\"query\":\"select * from t_app_version;\"}}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>false or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_Terminal"
  },
  {
    "type": "post",
    "url": "/terminal/",
    "title": "sqlite语句",
    "group": "TerminalServer_Terminal",
    "name": "sqlite__",
    "description": "<p>推送sqlite命令到终端</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>发送到哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>哪个web会话发送来的消息</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"sqlite\",\"param\":{\"query\":\"select * from t_app_version;\"}}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>false or false</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册",
          "content": "{\"result\":true}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_Terminal"
  },
  {
    "type": "post",
    "url": "/terminal/",
    "title": "upload",
    "group": "TerminalServer_Terminal",
    "name": "upload",
    "description": "<p>让终端发送指定文件到指定url</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>发送到哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>哪个web会话发送来的消息</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"upload\",\"param\":{\"path\":[\"filepath1\",\"filepath2\"],\"url\":\"http://123.123.123.123/upload\",\"filename\":\"zipFile.zip\"}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>false or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_Terminal"
  },
  {
    "type": "ws",
    "url": "/server/",
    "title": "cat_resp",
    "group": "TerminalServer_server",
    "name": "cat_response",
    "description": "<p>cat的回复</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>来自哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>发给哪个web会话，可空</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"cat\",\"param\":\"结果一大串\\\\r\\\\n结果一大串\"}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>true or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_server"
  },
  {
    "type": "ws",
    "url": "/server/",
    "title": "cmd_resp",
    "group": "TerminalServer_server",
    "name": "cmd_response",
    "description": "<p>执行cmd的回复</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>来自哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>发给哪个web会话，可空</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"cmd_resp\",\"param\":\"结果一大串\\\\r\\\\n结果一大串\"}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>true or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_server"
  },
  {
    "type": "ws",
    "url": "/server/",
    "title": "dir_resp",
    "group": "TerminalServer_server",
    "name": "dir_response",
    "description": "<p>dir的回复</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>来自哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>发给哪个web会话，可空</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"dir_resp\",\"param\":[{\"type\":\"file\",\"name\":\"app.exe\",\"create_date\":\"2016-05-01 00:00:00\",\"update_date\":\"2016-05-01 00:00:00\",\"size\":\"12mb\",\"file_ver\":\"1.1.2.3\"}]}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>true or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_server"
  },
  {
    "type": "ws",
    "url": "/server/",
    "title": "download_fin",
    "group": "TerminalServer_server",
    "name": "download_fin",
    "description": "<p>下载文件结束</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>来自哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>发给哪个web会话，可空</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"download_fin\",\"param\":false}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>true or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_server"
  },
  {
    "type": "ws",
    "url": "/server/",
    "title": "grep_resp",
    "group": "TerminalServer_server",
    "name": "grep_response",
    "description": "<p>grep的回复</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>来自哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>发给哪个web会话，可空</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"grep_resp\",\"param\":\"结果结果结果\"}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>true or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_server"
  },
  {
    "type": "ws",
    "url": "/server/",
    "title": "list_sys_log_resp",
    "group": "TerminalServer_server",
    "name": "list_sys_log_response",
    "description": "<p>系统日志回复</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>来自哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>发给哪个web会话，可空</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"dir_resp\",\"param\":[{\"time\":\"2016-05-01 00:00:00\",\"level\":\"error\",\"title\":\"application error\",\"content\":\"一大堆\"}]}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>true or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_server"
  },
  {
    "type": "ws",
    "url": "/server/",
    "title": "reg",
    "group": "TerminalServer_server",
    "name": "reg",
    "description": "<p>终端向T_server注册</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>来自哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>发给哪个web会话，可空</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"reg\",\"param\":\"518067N123\"}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>true or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_server"
  },
  {
    "type": "ws",
    "url": "/server/",
    "title": "sql_resp",
    "group": "TerminalServer_server",
    "name": "sql_response",
    "description": "<p>查询mysql或sqlite的回复</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>来自哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>发给哪个web会话，可空</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"sql_resp\",\"param\":[{\"id\":\"123\",\"name\":\"name123\",\"desc\":\"查询出来的数据\"}]}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>true or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_server"
  },
  {
    "type": "ws",
    "url": "/server/",
    "title": "upload_fin",
    "group": "TerminalServer_server",
    "name": "upload_fin",
    "description": "<p>上传文件结束</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tid",
            "description": "<p>来自哪台终端</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "wid",
            "description": "<p>发给哪个web会话，可空</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cid",
            "description": "<p>命令id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": ""
          },
          {
            "group": "Parameter",
            "type": "Object",
            "optional": false,
            "field": "param",
            "description": "<p>参数，需要base64编码</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "注册 ",
          "content": "{\"tid\":\"518067N33\",\"wid\":\"w123\",\"cid\":\"c123\",\"cmd\":\"upload_fin\",\"param\":false}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Boolean",
            "optional": false,
            "field": "result",
            "description": "<p>true or false</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./app.comment.py",
    "groupTitle": "TerminalServer_server"
  }
] });
