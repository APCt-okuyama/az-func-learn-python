# Github Copilot Lab

# はじめに

こんにちは。ACS 事業部の奥山です。

Azure Functions の Durable Functions (Python) についての調査・検証を行ったので、備忘録を兼ねてブログにしておきます。

プロジェクトで時間のかかる一括処理を行う必要があり、調べた内容です。
様々な方法があるとは思いますが、Azure なら Durable Functions お勧めです！

## Durable Functions (Azure Functions) とは

以前にブログを書いたブログを紹介
https://techblog.ap-com.co.jp/entry/2022/06/02/170053

# Pythonでの実装について

Azure Functions のプログラミングには プログラミング モデル v1 と v2 があります。
v1 と v2 の最も大きな違いは functions.json を利用するかどうかですかね。 v2 では functions.json がなくなりデコレーターでバインディング等の設定を指定することになり、コード中心になります。今回は v2 で実装を進めます。

## pythonでの実装 (最低限のはじめかた)

Azure Functions の Python 開発者向けガイド
https://learn.microsoft.com/ja-jp/azure/azure-functions/functions-reference-python?tabs=asgi%2Capplication-level&pivots=python-mode-decorators

※ cliベースで作業しています。
※ pythonの仮想環境

```
python -m venv .venv
source .venv/bin/activate
# deactivate
```

## まずはプロジェクトの作成

```
mkdir <プロジェクト フォルダ>
cd <プロジェクト フォルダ>
func init --python
ls 
function_app.py  host.json  local.settings.json  requirements.txt
```

## Durable Functionの作成

function_app.py を以下の様に変更します。

```
import azure.functions as func
import azure.durable_functions as df

myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# An HTTP-Triggered Function with a Durable Functions Client binding
@myApp.route(route="orchestrators/{functionName}")
@myApp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    function_name = req.route_params.get('functionName')
    instance_id = await client.start_new(function_name)
    response = client.create_check_status_response(req, instance_id)
    return response

# Orchestrator
@myApp.orchestration_trigger(context_name="context")
def hello_orchestrator(context):
    result1 = yield context.call_activity("hello", "Seattle")
    result2 = yield context.call_activity("hello", "Tokyo")
    result3 = yield context.call_activity("hello", "London")

    return [result1, result2, result3]

# Activity
@myApp.activity_trigger(input_name="city")
def hello(city: str):
    return f"Hello {city}"
```
## ローカルで確認

```
func start
```

curlで確認
```
curl http://localhost:7071/api/orchestrators/hello_orchestrator
```
# フォルダ構成を変更
いくつかの処理を実装していきたのですが、すべて function_app.py に実装していくと管理が大変になってしまうので、ファイルを機能単位に分けます。



# 最後に

私達 ACS 事業部は Azure・AKS を活用した内製化のご支援をしております。ご相談等ありましたらぜひご連絡ください。

[https://www.ap-com.co.jp/cloudnative/?utm_source=blog&utm_medium=article_bottom&utm_campaign=cloudnative:embed:cite]

また、一緒に働いていただける仲間も募集中です！  
切磋琢磨しながらスキルを向上できる、エンジニアには良い環境だと思います。ご興味を持っていただけたら嬉しく思います。

[https://www.ap-com.co.jp/recruit/info/requirements.html?utm_source=blog&utm_medium=article_bottom&utm_campaign=recruit:embed:cite]

<fieldset style="border:4px solid #95ccff; padding:10px">
本記事の投稿者: [奥山 拓弥](https://techblog.ap-com.co.jp/archive/author/mountain1415)  
</fieldset>