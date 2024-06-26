import logging
import time
import uuid
import azure.functions as func
import azure.durable_functions as df

bp = df.Blueprint()


# An HTTP-Triggered Function with a Durable Functions Client binding
@bp.route(route="orchestrators/{functionName}")
@bp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client):
    function_name = req.route_params.get('functionName')
    instance_id = "o1-" + str(uuid.uuid4())
    await client.start_new(function_name, instance_id)
    response = client.create_check_status_response(req, instance_id)
    return response


# Orchestrator
@bp.orchestration_trigger(context_name="context")
def hello_orchestrator(context):
    result1 = yield context.call_activity("hello", "Seattle")
    result2 = yield context.call_activity("hello", "Tokyo")
    result3 = yield context.call_activity("hello", "London")

    return [result1, result2, result3]


# Activity
@bp.activity_trigger(input_name="city")
def hello(city: str):
    logging.info(f"Saying hello to {city} start")
    time.sleep(60)
    logging.info(f"Saying hello to {city} end")
    return f"Hello {city}"
