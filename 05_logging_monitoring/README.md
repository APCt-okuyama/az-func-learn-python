# Logging & Monitoring

Functions(Python)でのLogging, Monitoring について簡単に。

基本的にApplication Insights(ワークスペース ベース)を利用する。

# 1. Application Insightsの設定

Application Insightsを利用します。
デフォルトではfunctionsと同じ名前で自動的にapp-insightsが作成される ※これはclassicタイプかな

```
az extension add -n application-insights
```

```
workspaceの作成
az monitor log-analytics workspace create --resource-group %RG_NAME% --workspace-name my-example-workspace

az monitor app-insights component create --app my-example-app-insights --location %LOCATION% --kind web -g %RG_NAME% --workspace "/subscriptions/d79e0410-8e3c-4207-8d0a-1f7885d35859/resourcegroups/%RG_NAME%/providers/microsoft.operationalinsights/workspaces/my-example-workspace"
```

```
az functionapp create 
```
※無効にしたい場合は `--disable-app-insights`
※既存のapp-insightsを利用する場合は `--app-insights` `--app-insights-key`

# 2. Logging

## アプリケーションのログ

Applicationのログはlogging ハンドラーを介して出力する。
下記のようにログレベルを設定可能

```
import logging

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.critical('This is logging.critical.')
    logging.error('This is logging.error.')
    logging.warning('This is logging.warning.')  
    logging.info('This is logging.info.')
    logging.debug('This is logging.debug.')
```

exception(例外)もApplication Insightsで監視できるのでエラー処理に適切に利用する
```
raise ValueError("error!")
```

### ログの確認(CLI)
Core Toolのコマンドで確認
従量課金プランの Linux 上で実行されているアプリでは、この方法を使用できない。
```
func azure functionapp logstream my-example-func-py
```

### ログの確認

![image](./img/001.PNG)
| -| 確認方法 |
| --- | --- |
| ログ |　tracesテーブル を KQLで検索 |
| ログ ストリーム | ポータルのストリーム画面<br>反応がわるいときがある。 |

### ログレベル(ログの量)の設定
host.json で調整可能
```
{
  "version": "2.0",
  "logging": {
    "logLevel": {
      "default":"Information"
    },
```

## カスタム テレメトリをログに記録する
opencensus-python-extensions-azure(python用)の利用について


## Monitoring

### Portal画面から確認できる内容

### 必要な情報をまとめてダッシュボードで監視する

### KQL
基本的な利用方法だけ覚えて利用する
