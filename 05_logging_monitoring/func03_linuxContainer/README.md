# カスタム コンテナーを使用して Linux で関数を作成する

https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-create-function-linux-custom-image?tabs=in-process%2Cbash%2Cazure-cli&pivots=programming-language-python

Premium プラン or 専用プラン が必要です。※従量課金プランではコンテナは利用できない。

## Functionsを--docker指定で作成
```
func init --worker-runtime python --docker
```

```
func new --name HttpExample --template "HTTP trigger" --authlevel anonymous
```

## Docker 

docker image作成
```
docker build --tag tokym/my-func-py-image:v1.0.0 .
```

ローカル実行
```
docker run --rm -p 8080:80 -it tokym/my-func-py-image:v1.0.0
```

Image Push
```
docker push tokym/my-func-py-image:v1.0.0
```

## Azure Functions(Premium プラン)

Premium プラン作成
```
az functionapp plan create --resource-group $RG_NAME --name my-func-PremiumPlan --location $LOCATION --number-of-workers 1 --sku EP1 --is-linux
```

Function作成(--app-insightsなどを指定)
```
az functionapp create --name my-example-func-py-container --storage-account funcstorage0001 --resource-group $RG_NAME --plan my-func-PremiumPlan --functions-version 4 --deployment-container-image-name tokym/my-func-py-image:v1.0.0 --app-insights my-example-app-insights
```

## curlで確認
```
curl https://my-example-func-py-container.azurewebsites.net/api/HttpExample
```

## イメージの更新

イメージを更新して再度、`az functionapp create`を実行する

再起動？