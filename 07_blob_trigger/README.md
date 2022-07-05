# Blob Trigger と アクセス制限

## trigger 対象の blob を準備

Storageアカウントを作成
```
az storage account create -n funcstorage0002 -g $RG_NAME -l $LOCATION --sku Standard_LRS --kind StorageV2
az storage account show-connection-string -g $RG_NAME -n funcstorage0001
```

コンテナを作成
```
az storage container create --account-name funcstorage0002 -n samples-workitems
```
# Trigger設定

![image](./img/blob-trigger-access.png)


## option 1 (アクセス キー)接続文字列　※SASではない

アプリ設定または設定コレクションの名前

## option 2 (ID ベースの接続)
シークレットを含む接続文字列の代わりとして利用できる



## option 3

Functionsの送信IPアドレスを固定する (NATゲートウェイ)
ネットワークの制限を入れる

## SASの利用について
まず、３種類ある

| SAS | 説明 | 備考 |
| --- | --- | --- |
| ユーザー委任のSAS | Azure ADの資格情報で保護<br>blob ストレージにのみ適用される | セキュリティーが一番高い<br>Microsoft推奨 |
| サービスSAS |ストレージアカウントキーで保護<br>blob,queue,table,filesのどれか一つだけのアクセスを委任する||
| アカウントSAS | ストレージアカウントキーで保護<br>blob,queue,table,filesの複数のアクセスを委任する<br>ストレージアカウントのShared Access Signatureから設定 | |


### ユーザー委任のSASを作成してアクセスしてみる (Azure CLI)

ストレージ BLOB データ共同作成者ロールを割り当てる
```
az role assignment create \
    --role "Storage Blob Data Contributor" \
    --assignee t_okuyama@ap-com.co.jp \
    --scope "/subscriptions/$SUBSCRIPTION/resourceGroups/$RG_NAME/providers/Microsoft.Storage/storageAccounts/funcstorage0002"
```

コンテナー用のSASを作成
```
az storage container generate-sas --account-name funcstorage0002 --name samples-workitems --permissions acdlrw --expiry 2022-07-06T00:00:00Z \
    --auth-mode login \
    --as-user \
    --ip 123.48.1.91
```

BLOB用のSASを作成
```
az storage blob generate-sas \
    --account-name funcstorage0002 \
    --container-name samples-workitems \
    --name README.md \
    --permissions acdrw \
    --expiry 2022-07-06T00:00:00Z \
    --auth-mode login \
    --as-user \
    --full-uri
```

fileのupload
```
az storage blob upload --container-name samples-workitems \
                        --file test.data \
                        --name test.data2 \
                        --account-name funcstorage0002 \
                        --overwrite \
                        --sas-token "se=2022-07-06T00%3A00%3A00Z&sp=racwdl&sip=123.48.1.91&sv=2021-06-08&sr=c&skoid=d79c183b-899e-4700-9e31-daed46ee561b&sktid=4029eb38-8689-465c-92e1-9464066c814c&skt=2022-07-05T07%3A46%3A13Z&ske=2022-07-06T00%3A00%3A00Z&sks=b&skv=2021-06-08&sig=xoqCYR7ina7lc0VM6KdSCim3JY4Xf/e641UXbs9m1S8%3D"

```

az storage blob download -c samples-workitems -n README.md --account-name funcstorage0002 --account-
        key myaccountkey


取り消す
```
az storage account revoke-delegation-keys \
    --name funcstorage0002 \
    --resource-group $RG_NAME
```

Azure Blob Storageでは、ストレージに保管したデータのことを「BLOB」といい、BLOBを保管する場所を「コンテナー」と呼びます。

BLOB SAS URL
```
https://funcstorage0002.blob.core.windows.net/samples-workitems?"sp=rac&st=2022-07-05T06:46:46Z&se=2022-07-05T14:46:46Z&skoid=d79c183b-899e-4700-9e31-daed46ee561b&sktid=4029eb38-8689-465c-92e1-9464066c814c&skt=2022-07-05T06:46:46Z&ske=2022-07-05T14:46:46Z&sks=b&skv=2021-06-08&spr=https&sv=2021-06-08&sr=c&sig=YVAqugCUiT4mXjQ%2BX%2B94m8A6t0TqTChcgkyykgzCevM%3D"
```
## Event Grid の利用の検討
BlobTriggerはポーリングなので遅い

ストレージ拡張機能 5.x 以降





# 調べたいこと1 (SASの利用例)
```
NWレベルで全てのパブリックアクセスを許可した上で、オンプレ側からのアクセスについてはSASでグローバルIP制限をかけるようにする
```

![image](./img/use-sas-sample.png)

# 調べたいこと2
```
NWレベルでESSのグローバルIPしか許可しない設定にしつつ、、、
```
ネットワーク ルールは、Azure Storage のすべてのネットワーク プロトコル (REST と SMB を含む) に適用されます。

Functionsがアクセスできなくなる。。。



