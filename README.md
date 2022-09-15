# az-func-learn-python

(注意) Linuxやwindows環境で検証しているため、環境変数の指定の方法が統一されていないです。

https://docs.microsoft.com/ja-jp/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser

## オペレーティングシステムにLinuxを選択する必要があります。

現時点では Python 関数を Windows で実行することはできないため、Linxu OS の Functions しか利用できない。
Functions作成時に `--os-type linux` を指定して作成します。

https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-scale

## pythonのバージョン

https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-versions?tabs=azure-cli%2Cin-process%2Cv4&pivots=programming-language-python

Functions ランタイムのバージョン 4.x を利用するので、Python 3.9、3.8、3.7　のどれかを利用する。
今回は Python 3.9 を利用します。

## 準備

※可能な限り最新のものを利用する
※pyenv をインストールしておくと便利 (option)

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
export SUBSCRIPTION=xxxx
```
環境変数(win)
```
set RG_NAME=az-func-example-rg1
set LOCATION=japaneast
set SUBSCRIPTION=xxxx
```

## Azureリソースの準備

リソースグループ
```
az group create -n $RG_NAME -l $LOCATION

(注意) 不要になったら削除する
az group delete --name $RG_NAME -y
```

app-insights
```
# workspaceの作成
az monitor log-analytics workspace create --resource-group $RG_NAME --workspace-name my-example-workspace

# app-insightsの作成
az monitor app-insights component create --app my-example-app-insights --location $LOCATION --kind web -g $RG_NAME --workspace "/subscriptions/$SUBSCRIPTION/resourcegroups/$RG_NAME/providers/microsoft.operationalinsights/workspaces/my-example-workspace"
```

storage
```
az storage account create -n funcstorage0001 -g $RG_NAME -l $LOCATION --sku Standard_LRS --kind StorageV2
az storage account show-connection-string -g $RG_NAME -n funcstorage0001 -o tsv
```

### 従量課金プラン
```
( pythonを利用するので `--os-type linux` を指定します。 検証目的なので従量課金)
az functionapp create -g $RG_NAME --consumption-plan-location $LOCATION --runtime python --runtime-version 3.9 --functions-version 4 --name my-example-func-py --os-type linux --storage-account funcstorage0001 --app-insights my-example-app-insights 
```

※従量課金プランで作成しているので開発中は不用意にスケーリングされないようにScaleLimitを設定しておきます。
```
az resource update --resource-type Microsoft.Web/sites -g $RG_NAME -n my-example-func-py/config/web --set properties.functionAppScaleLimit=1
```

FTPベースのデプロイは利用しない場合無効にしておく
```
az webapp config set --name my-example-func-py --resource-group $RG_NAME --ftps-state Disabled
```

### プレミアムプラン (EP1)

プランを作成
```
az functionapp plan create --resource-group $RG_NAME --name my-func-PremiumPlan --location $LOCATION --number-of-workers 1 --sku EP1 --is-linux

# Function作成(--app-insightsなどを指定)
az functionapp create --name my-example-func-py --storage-account funcstorage0001 --resource-group $RG_NAME --plan my-func-PremiumPlan --runtime python --runtime-version 3.9 --functions-version 4 --app-insights my-example-app-insights

# Function作成(--app-insightsなどを指定)　コンテナ
az functionapp create --name my-example-func-py-container --storage-account funcstorage0001 --resource-group $RG_NAME --plan my-func-PremiumPlan --functions-version 4 --deployment-container-image-name tokym/my-func-py-image:v1.0.0 --app-insights my-example-app-insights
```

## Python 仮想環境を作成してアクティブにする

windows
```
py -m venv .venv
.venv\scripts\activate
```
linux
```
python -m venv .venv
source .venv/bin/activate
```

## ライブラリーのインストール
```
python -m pip install -r requirements.txt
```

## Functions Core tools
良く利用するコマンド
```
# プロジェクトの初期化
func init --python

# 関数の追加
func new

# local実行
func start

# 関数のデプロイ (defaultはremote build)
func azure functionapp publish my-example-func-py
func azure functionapp publish my-example-func-py --publish-local-settings -y

# -b local
# ローカルビルド オプション (こちらのがすこし早い？。linuxで開発しているときに利用, windows開発環境では推奨されない。とりあえずは標準のリモートビルドで問題なしかな。)
func azure functionapp publish my-example-func-py1 -b local

# Azure上のアプリケーション設定をlocal.setting.json取り込む
func azure functionapp fetch-app-settings my-example-func-py

# logをfilesystemへ書き出すように設定 (Linux従量課金プランではできない)
az webapp log config --name my-example-func-py --resource-group $RG_NAME --web-server-logging filesystem

# ログの確認
func azure functionapp logstream my-example-func-py
```

# 確認
```
curl https://my-example-func-py1.azurewebsites.net/api/httptrigger
```

# pyenv

必要最低限のコマンド

```
# インストール可能な一覧
pyenv install --list

# インストール アンインストール
pyenv install 3.9.11
pyenv uninstall 3.9.11

# インストール済み一覧
pyenv versions

# バージョンの切り替え (global or local)
pyenv global 3.9.11
pyenv local 3.9.11
  python --version で確認する
```
