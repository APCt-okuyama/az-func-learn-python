# az-func-learn-python

(注意) Linuxやwindows環境で検証しているため、環境変数の指定の方法が統一されていないです。

https://docs.microsoft.com/ja-jp/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser

### オペレーティングシステムにLinuxを選択する必要があります。

現時点では Python 関数を Windows で実行することはできないため、Linxu OS の Functions しか利用できない。
Functions作成時に `--os-type linux` を指定して作成します。

https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-scale

## 準備

※可能か限り最新のものを利用する

```
az version
"azure-cli": "2.30.0"

func -v 
4.0.4544

python -V
Python 3.9.11
```

環境変数(linux)
```
export RG_NAME=az-func-example-rg
export LOCATION=japaneast
```
環境変数(win)
```
set RG_NAME=az-func-example-rg
set LOCATION=japaneast
```

## Azureリソース
```
az group create -n %RG_NAME% -l %LOCATION%

az storage account create -n funcstorage0001 -g %RG_NAME% -l %LOCATION% --sku Standard_LRS --kind StorageV2
az storage account show-connection-string -g %RG_NAME% -n funcstorage0001


( pythonを利用するので `--os-type linux` を指定します。 検証目的なので従量課金)
az functionapp create -g %RG_NAME% --consumption-plan-location %LOCATION% --runtime python --runtime-version 3.9 --functions-version 4 --name my-example-func-py --os-type linux --storage-account funcstorage0001 --app-insights my-example-app-insights 
```

※従量課金プランで作成しているので開発中は不用意にスケーリングされないようにScaleLimitを設定しておきます。
```
az resource update --resource-type Microsoft.Web/sites -g %RG_NAME% -n my-example-func-py/config/web --set properties.functionAppScaleLimit=1
```

FTPベースのデプロイは利用しない場合無効にしておく
```
az webapp config set --name my-example-func-py --resource-group %RG_NAME% --ftps-state Disabled
```

## Python 仮想環境を作成してアクティブにする
```
py -m venv .venv
.venv\scripts\activate
python -m pip install -r requirements.txt
```

## Functions Core tools
良く利用するコマンド
```
# プロジェクトの初期化
func init --python

# 関数の追加
func new

# 関数のデプロイ (windowsからはremote buildになります)
func azure functionapp publish my-example-func-py
func azure functionapp publish my-example-func-py --publish-local-settings -y

# ログの確認
func azure functionapp logstream my-example-func-py
```

# 確認
```
curl http://localhost:7071/api/orchestrators/orchestrationTrigger
```

# (注意) 不要になったら削除する
```
az group delete --name az-func-example-rg -y
```
