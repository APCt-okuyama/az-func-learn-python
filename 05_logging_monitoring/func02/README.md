
同じconsumption-planへfunctionappを作成
```
az functionapp create -g $RG_NAME --consumption-plan-location $LOCATION --runtime python --runtime-version 3.9 --functions-version 4 --name my-example-func-py2 --os-type linux --storage-account funcstorage0001 --app-insights my-example-app-insights
```

