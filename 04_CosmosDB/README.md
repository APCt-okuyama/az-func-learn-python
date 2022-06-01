# Cosmos DB

Cosmos DBのアカウントを準備する。　※従量課金のサーバレスモードで作成(--capabilities EnableServerless)
```
# Create a Cosmos account for SQL API
az cosmosdb create --name "my-training1-account" --resource-group az-func-example-rg --default-consistency-level Eventual --locations regionName="japaneast" failoverPriority=0 isZoneRedundant=False --capabilities EnableServerless
az cosmosdb list-connection-strings --name my-training1-account --resource-group az-func-example-rg
```

以下のコマンドでデータベースとコンテナーを作成する  
※activity(`functions.json`)で `"createIfNotExists": true` を指定している場合は自動で作成されるため、手動で作成する必要なし。

