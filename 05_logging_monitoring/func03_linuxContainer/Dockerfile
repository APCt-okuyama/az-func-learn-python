# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.9-appservice
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.9

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /
RUN pip install -r /requirements.txt

##　ローカルで実行する場合、環境変数として設定
ENV PYTHON_ENABLE_WORKER_EXTENSIONS=1
ENV APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=1ebe2792-8d4e-4cca-a22f-ef2d416f2320;IngestionEndpoint=https://japaneast-1.in.applicationinsights.azure.com/;LiveEndpoint=https://japaneast.livediagnostics.monitor.azure.com/"
ENV APPINSIGHTS_INSTRUMENTATIONKEY="1ebe2792-8d4e-4cca-a22f-ef2d416f2320"
ENV FUNC01_URL_STRING="https://my-example-func-py.azurewebsites.net/api/httptrigger"
ENV FUNC02_URL_STRING="https://my-example-func-py2.azurewebsites.net/api/httptrigger"
##

COPY . /home/site/wwwroot