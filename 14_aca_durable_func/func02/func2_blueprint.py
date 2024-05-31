import logging
import socket
import time
import uuid
import azure.functions as func
import azure.durable_functions as df
import numpy as np

bp = df.Blueprint()

hostname = socket.gethostname()  # Get the hostname
formatter = logging.Formatter(f'%(levelname)s - Host: {hostname} - %(process)d - %(thread)d - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()  # Get the root logger
logger.addHandler(handler)  # Add the handler to the logger

# An HTTP-Triggered Function with a Durable Functions Client binding
@bp.route(route="orchestrators2/{functionName}")
@bp.durable_client_input(client_name="client")
async def http_start2(req: func.HttpRequest, client):
    function_name = req.route_params.get('functionName')
    instance_id = "o2-" + str(uuid.uuid4())
    await client.start_new(function_name, instance_id)
    response = client.create_check_status_response(req, instance_id)
    return response


# Orchestrator
@bp.orchestration_trigger(context_name="context")
def hello_orchestrator2(context):

    # F1
    all_work_batch = yield context.call_activity("F1")
    # logging.info(f"all_work_batch: {all_work_batch}")

    # F2
    parallel_tasks = []
    # 100個に分割してActivityを呼び出す
    split_work_batches = np.array_split(all_work_batch, len(all_work_batch) // 100)
    for works in split_work_batches:
        parallel_tasks.append(context.call_activity("F2", works.tolist()))
    # logging.info(f"parallel_tasks: {parallel_tasks}")
    outputs = yield context.task_all(parallel_tasks)

    # F3
    result = yield context.call_activity("F3", outputs)
    return result


# Activity
@bp.activity_trigger(input_name="dummy")
def F1(dummy=None):
    logging.info("F1 start")
    # 数値の配列作成する
    return [i for i in range(1000)]


# Activity
@bp.activity_trigger(input_name="input")
def F2(input):
    logging.info("F2 start")

    for i in input:
        time.sleep(3)
        logging.info(f"F2 input: {i}")
    logging.info("F2 end")
    return input


# Activity
@bp.activity_trigger(input_name="input")
def F3(input):
    logging.info("F3 start ... endz")
    return input
