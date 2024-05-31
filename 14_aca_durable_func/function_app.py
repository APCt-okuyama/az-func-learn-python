import azure.functions as func
from func01.func1_blueprint import bp as bulk_create_data_bp
from func02.func2_blueprint import bp as bulk_create_data2_bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
app.register_functions(bulk_create_data_bp)
app.register_functions(bulk_create_data2_bp)
