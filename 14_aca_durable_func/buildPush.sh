export TAG_NAME=$(date +%Y%m%d%H%M%S)
echo "###########################################"
echo RG_NAME       : $RG_NAME
echo ACR IMAGE     : ${ACR_NAME}.azurecr.io/$IMAGE_NAME:latest
echo CONTAINER APP : $CONTAITER_APP_NAME
echo TAG_NAME      : $TAG_NAME
echo "###########################################"

docker build --tag $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG_NAME .
docker push ${ACR_NAME}.azurecr.io/$IMAGE_NAME:$TAG_NAME

# コンテナアプリを更新
az containerapp update --name $CONTAITER_APP_NAME --resource-group $RG_NAME --image $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG_NAME

# https: