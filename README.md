# 使用方法
第一次试着做项目，还不是很熟练
This is my first time building a project, so I'm still learning and getting used to the development workflow.

如果你有python就不用看下面的了，直接把apikey复制到agent里就行
If you had already downloaded the python then you can jump the following step
## 1.Python环境

### Mac系统
在terminal（Mac系统）里输入以下命令，下载homebrew
Install the homebrew by the following command

>/bin/bash -c "\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
>echo >> ~/.zprofile
>echo 'eval "\$(/opt/homebrew/bin/brew shellenv zsh)"' >> ~/.zprofile
>eval "\$(/opt/homebrew/bin/brew shellenv zsh)"
>brew --version

之后：
then :

>brew install python@3.12
>/opt/homebrew/bin/python3.12 --version
下载python3.12的版本。
download the python3.12

在此项目的文件夹中打开terminal，输入以下命令，创建虚拟环境
open the terminal in this directory and create the virtual environment by following command

>/opt/homebrew/bin/python3.12 -m venv venv
>source venv/bin/activate

terminal里，输入
Download the required packages.

>pip install -r requirements.txt
下载所需的包。至此环境配置完成
finished

### Win系统
在Win + R输入cmd打开终端，输入以下命令
Open the cmd and enter the following command

>winget install Python.Python.3.12

在此项目的文件夹里打开cmd，创建虚拟环境：
create the virtual environment by following comman

>python -m venv venv
>venv\Scripts\activate

最后输入以下命令下载所需包：
Download the required packages.

>pip install -r requirements.txt


## 2.注册Openrouter，获取API
- 去网站 **www.openrouter.ai** 注册账号，申请一个 API key，这一步可能需要挂梯子
  Go to the www.openrouter.ai, create an account and get an API key.
  
- 把你的 api key 保存好，你可以复制黏贴到一个word文档里，注意<span style="color:red">不要让别人知道</span>你的 api key，除非你钱多
  Save the API key in a proper place, you can paste it in a docx.
  Don't let others know your API key unless you are rich

- 注册好拿到 API 之后在文件 **agent.py** 中的第13行中的 **OPENROUTER_API_KEY** 中复制粘贴你的 API key
then paste the API key to the file **agent.py**, line 13, **OPENROUTER_API_KEY**
