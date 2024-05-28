# Flex Consumption Plan

仮想ネットワークの統合　が可能 ★

Python 3.10、Python 3.11

2024/05時点は Preview です。

## 前提
https://learn.microsoft.com/ja-jp/azure/azure-functions/create-first-function-cli-python?tabs=linux%2Cbash%2Cazure-cli%2Cbrowser

Azure CLI バージョン ※最新を利用
```
az version
{
  "azure-cli": "2.61.0",
  "azure-cli-core": "2.61.0",
  "azure-cli-telemetry": "1.1.0",
  "extensions": {}
}
```

Azure Functions Core Tools
```
func --version
4.0.5801
```

# 補足

```
# @app.route(route="HttpExample", auth_level=func.AuthLevel.Anonymous)
@app.route(route="HttpExample", auth_level=func.AuthLevel.ANONYMOUS)
```
定義が変わったな！？

# az cli (azure function)
az 
```
export RG_NAME=rg-okym-funcpy-2024-05
export STORAGE_NAME=st2024okym0001test
export REGION=japaneast
export FUNC_NAME=func-sample-durable-py

# rg
az group create --name $RG_NAME --location $REGION
# az group delete -n $RG_NAME

# storage (--allow-blob-public-access false)
az storage account create --name $STORAGE_NAME --location $REGION --resource-group $RG_NAME --sku Standard_LRS

# list-flexconsumption-locations ※japaneastはまだ提供されていない
az functionapp list-flexconsumption-locations --output table
Name
---------------------
eastus
northeurope
southeastasia
eastasia
eastus2
southcentralus
australiaeast
northcentralus(stage)
westus2
uksouth
eastus2euap
westus3
swedencentral

# 通常の従量課金 (--consumption-plan-location)
az functionapp create --resource-group $RG_NAME --consumption-plan-location $REGION --runtime python --runtime-version 3.11 --functions-version 4 --name $FUNC_NAME --os-type linux --storage-account $STORAGE_NAME
# ※ Flex 従量課金だと durable(python) が Azure にデプロイ後に以下のエラーになるので 通常の従量課金プランで実施

# function (--flexconsumption-location)
# az functionapp create --resource-group $RG_NAME --flexconsumption-location $REGION --runtime python --runtime-version 3.11 --functions-version 4 --name $FUNC_NAME --os-type linux --storage-account $STORAGE_NAME
```

v2 プログラミング モデルを有効
```
az functionapp config appsettings set --name $FUNC_NAME --resource-group $RG_NAME --settings AzureWebJobsFeatureFlags=EnableWorkerIndexing
```

# az function (ここからはプログラミング)

※<プロジェクト フォルダ> を作成しておく
仮想環境作成

```
python -m venv .venv
source .venv/bin/activate
```

## create project

仮想環境に Python v2 関数プロジェクトを作成

```
cd <プロジェクト フォルダ>
func init --python
```

## create func

```
func new --name HttpExample --template "HTTP trigger" --authlevel "ANONYMOUS"
```

## run on local

```
func start
```

## deploy

```
func azure functionapp publish $FUNC_NAME
```

# プログラミングモデルの v1 と v2

- v2 では トリガーとバインディングを デコレーターで指定する (function.json が不要になった)
- 関数のエントリーポイントが _init_.py から function_app.py に変更

## すべてのステータスを取得することも可能

```
# 'functionName' がすでに動いているかどうかを確認する
    instances = await client.get_status_all()
```

