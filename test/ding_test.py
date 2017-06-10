#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

ding_url="https://oapi.dingtalk.com/robot/send?access_token=c6ecc4afe15d1e2e4bcb807531f22bdf07dae047bfc12f7ad55964a635d65b77"

msg_markdown={
    "msgtype": "markdown",
    "markdown": {
        "title": "ooooo",
        "text": """# Hello world \n
> A man who stands \n\n
**bold** \n
*italic* \n
[this is a link](http://www.baidu.com)\n\n
- item1\n\n
- item2\n\n
1. item1\n\n
2. item2\n\n
<font color="#FF0000">wwwwwww</font><br/>
<font size="18">big</font><br/>
<table>
<tr><th>Month</th><th>Savings</th></tr>
<tr><td>January</td><td>1100</td></tr>
</table>
"""
    }
}

msg= {
        "feedCard": {
            "links": [
                {
                    "title": "时代的火车向前开",
                    "messageURL": "https://mp.weixin.qq.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                    "picURL": "https://www.dingtalk.com/"
                    },
                {
                    "title": "时代的火车向前开2",
                    "messageURL": "https://mp.weixin.qq.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                    "picURL": "https://www.dingtalk.com/"
                    }
                ]
            },
        "msgtype": "feedCard"
}


headers = {"Content-Type": "application/json"}
resp = requests.post(ding_url, data=json.dumps(msg_markdown), headers=headers)
print resp.content
print resp.status_code
