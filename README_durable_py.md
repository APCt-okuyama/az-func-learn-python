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

# Azure CLI (azure function)
az 
```
export RG_NAME=rg-okym-funcpy-202406
export STORAGE_NAME=st202406okym0001test
export REGION=japaneast
export FUNC_NAME=func-sample-durable-py

# rg
az group create --name $RG_NAME --location $REGION
# az group delete -n $RG_NAME


# タグを適用
tags="owner=<t_okuyama>"
az group update --name $RG_NAME --tags $tags


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
az functionapp create --resource-group $RG_NAME --consumption-plan-location $REGION --runtime python --runtime-version 3.10 --functions-version 4 --name $FUNC_NAME --os-type linux --storage-account $STORAGE_NAME
# ※ Flex 従量課金だと durable(python) が Azure にデプロイ後に以下のエラーになるので 通常の従量課金プランで実施

# [注意] 予期せぬ課金を防ぐための functionAppScaleLimit の設定
az resource update --resource-type Microsoft.Web/sites -g $RG_NAME -n $FUNC_NAME/config/web --set properties.functionAppScaleLimit=2


# function (--flexconsumption-location)
# az functionapp create --resource-group $RG_NAME --flexconsumption-location $REGION --runtime python --runtime-version 3.10 --functions-version 4 --name $FUNC_NAME --os-type linux --storage-account $STORAGE_NAME
```

v2 プログラミング モデルを有効
```
az functionapp config appsettings set --name $FUNC_NAME --resource-group $RG_NAME --settings AzureWebJobsFeatureFlags=EnableWorkerIndexing
```




## Functionsのデプロイ
```
func azure functionapp publish $FUNC_NAME
func azure functionapp publish $FUNC_NAME --publish-local-settings -y
```

```
func azure functionapp logstream $FUNC_NAME
```





これより下はACAを利用する場合
# Azure CLI (azure function & Container Apps)

- vnet統合 と 0スケーリング(費用削減) の為、Durable Functions を Container Apps へデプロイする
- 利用する Docker Image は[こちら](https://mcr.microsoft.com/catalog?search=functions)


## ACR
```
export ACR_NAME=acr202406funcapp
export IMAGE_NAME=durable-function-test
```

ACR セットアップ
```
az extension add --name containerapp --upgrade
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
```

ACR 作成
```
az acr create --resource-group $RG_NAME --name $ACR_NAME --sku Basic
```


```
az acr login --name $ACR_NAME

# build
docker build --tag $ACR_NAME.azurecr.io/$IMAGE_NAME:v1.0.0 .

# push
docker push ${ACR_NAME}.azurecr.io/$IMAGE_NAME:latest
```
## Container Apps



環境作成
```
export CONTAINERAPPS_ENVIRONMENT=aca-okym-2024-01
az containerapp env create \
  --name $CONTAINERAPPS_ENVIRONMENT \
  --resource-group $RG_NAME \
  --location "$REGION"
```
※ --plan default は 「ワークロード プロファイル」
※ --plan については 「従量課金のみ」と「ワークロード プロファイル」どちらも 0スケーリング可能



アプリの作成
※ システム割り当てマネージド ID を利用します。

image mcr.microsoft.com/k8se/quickstart:latest でアプリを作成
```
export CONTAITER_APP_NAME=my-1st-container-app
az containerapp create --name $CONTAITER_APP_NAME --resource-group $RG_NAME --environment $CONTAINERAPPS_ENVIRONMENT --image mcr.microsoft.com/k8se/quickstart:latest --target-port 80 --ingress 'external' --query properties.configuration.ingress.fqdn
```

システム割り当てマネージド ID の設定
```
az containerapp registry set \
  --name $CONTAITER_APP_NAME \
  --resource-group $RG_NAME \
  --identity system \
  --server "${ACR_NAME}.azurecr.io"
```

コンテナ アプリを更新
※コンテナイメージを作りなおしてデプロイする
```
az containerapp update --name $CONTAITER_APP_NAME --resource-group $RG_NAME --image $ACR_NAME.azurecr.io/$IMAGE_NAME:latest
```

https://my-1st-container-app.purpleisland-1252aa69.japaneast.azurecontainerapps.io/api/orchestrators/hello_orchestrator2


環境変数の設定
```
az containerapp update -n $CONTAITER_APP_NAME -g $RG_NAME \
  --set-env-vars WEBSITE_HOSTNAME=localhost:80 \
  --set-env-vars AzureWebJobsStorage=<ここはシークレットを利用する>
```

WEBSITE_HOSTNAME=localhost:80

# az function (ここからはプログラミング)

※<プロジェクト フォルダ> を作成しておく
仮想環境作成

```
cd <プロジェクト フォルダ>
python -m venv .venv
source .venv/bin/activate
# deactivate
```

## create project

仮想環境に Python v2 関数プロジェクトを作成

```
cd <プロジェクト フォルダ>
func init --python -model V2
```

## create func

```
func new --name HttpExample --template "HTTP trigger" --authlevel "ANONYMOUS"
```

## run on local

```
func start
# logをファイルに出力する場合
func start > outfile.log 2>&1
```

dockerコンテナの場合
```
docker run -p 8080:80 \
  -e AzureWebJobsFeatureFlags=EnableWorkerIndexing \
  -e AzureWebJobsStorage=$AzureWebJobsStorage \
  -e WEBSITE_HOSTNAME=localhost:8080 \
  -it acr202405funcapp.azurecr.io/durable-function-test:v1
```
※ ACA へデプロイする場合は WEBSITE_HOSTNAME=localhost:80

https://blog.shibayan.jp/entry/20220503/1651510570

## deploy

```
func azure functionapp publish $FUNC_NAME
```

# プログラミングモデルの v1 と v2

- v2 では トリガーとバインディングを デコレーターで指定する (function.json が不要になった)
- 関数のエントリーポイントが _init_.py から function_app.py に変更

## すべてのステータスを取得することも可能

```
# 'functionName' がすでに動いているかどうかを確認可能
    instances = await client.get_status_all()
```

