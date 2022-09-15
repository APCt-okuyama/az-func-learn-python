# Using Flask Framework with Azure Functions

https://docs.microsoft.com/en-us/samples/azure-samples/flask-app-on-azure-functions/azure-functions-python-create-flask-app/


## 構成
```
$ tree -L 1
.
├── FlaskApp ※ Flaskアプリの実態。これを作成する。
├── HttpTrigger ※ http trigger から WsgiMiddleware で FlaskApp へ繋ぐ
├── README.md
├── getting_started.md
├── host.json
├── local.settings.json
└── requirements.txt
```

## FlaskApp
FlaskAppはFlaskで作られた簡単なアプリ
```
from flask import Flask

# Always use relative import for custom module
from .package.module import MODULE_VALUE

app = Flask(__name__)

@app.route("/")
def index():
    return (
        "Try /hello/Chris for parameterized Flask route.\n"
        "Try /module for module import guidance"
    )

@app.route("/hello/<name>", methods=['GET'])
def hello(name: str):
    return f"hello {name}"

@app.route("/module")
def module():
    return f"loaded from FlaskApp.package.module = {MODULE_VALUE}"

if __name__ == "__main__":
    app.run()
```