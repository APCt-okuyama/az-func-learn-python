import azure.functions as func
from func1_blueprint import bp


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
app.register_functions(bp)
