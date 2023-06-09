### 插件描述
本插件用于将画图请求转发给stable diffusion webui。

### 环境要求
使用前先安装stable diffusion webui，并在它的启动参数中添加 "--api"。
具体信息，请参考[文章](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API)。

请**安装**本插件的依赖包```webuiapi```
```
    ```pip install webuiapi```
```
### 使用说明
请将`config.json.template`复制为`config.json`，并修改其中的参数和规则。

#### 画图请求格式
用户的画图请求格式为:
```
    <画图触发词><关键词1> <关键词2> ... <关键词n>:<prompt> 
```
- 本插件会对画图触发词后的关键词进行逐个匹配，如果触发了规则中的关键词，则会在画图请求中重载对应的参数。
- 规则的匹配顺序参考`config.json`中的顺序，每个关键词最多被匹配到1次，如果多个关键词触发了重复的参数，重复参数以最后一个关键词为准：
- 关键词中包含`help`或`帮助`，会打印出帮助文档。
第一个"**:**"号之后的内容会作为附加的**prompt**，接在最终的prompt后

例如: 画横版 高清 二次元:cat
会触发三个关键词 "横版", "高清", "二次元"，prompt为"cat"
若默认参数是:
```
    "width": 512,
    "height": 512,
    "enable_hr": false,
    "prompt": "8k"
    "negative_prompt": "nsfw",
    "sd_model_checkpoint": "perfectWorld_v2Baked"
```

"横版"触发的规则参数为:
```
    "width": 640,
    "height": 384,
```
"高清"触发的规则参数为:
```
    "enable_hr": true,
    "hr_scale": 1.6,
```
"二次元"触发的规则参数为:
```
    "negative_prompt": "(low quality, worst quality:1.4),(bad_prompt:0.8), (monochrome:1.1), (greyscale)",
    "steps": 20,
    "prompt": "masterpiece, best quality",

    "sd_model_checkpoint": "meinamix_meinaV8"
```
最后将第一个":"后的内容cat连接在prompt后，得到最终参数为:
```
    "width": 640,
    "height": 384,
    "enable_hr": true,
    "hr_scale": 1.6,
    "negative_prompt": "(low quality, worst quality:1.4),(bad_prompt:0.8), (monochrome:1.1), (greyscale)",
    "steps": 20,
    "prompt": "masterpiece, best quality, cat",
    
    "sd_model_checkpoint": "meinamix_meinaV8"
```
PS: 参数分为两部分:
- 一部分是params，为画画的参数;参数名**必须**与webuiapi包中[txt2img api](https://github.com/mix1009/sdwebuiapi/blob/fb2054e149c0a4e25125c0cd7e7dca06bda839d4/webuiapi/webuiapi.py#L163)的参数名一致
- 另一部分是options，指sdwebui的设置，使用的模型和vae需要写在里面。它和http://127.0.0.1:7860/sdapi/v1/options所返回的键一致。