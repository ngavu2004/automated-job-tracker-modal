# my_job_queue_endpoint.py
import fastapi
import modal

image = modal.Image.debian_slim().pip_install("fastapi[standard]")
app = modal.App("fastapi-modal", image=image)
web_app = fastapi.FastAPI()


@app.function()
@modal.asgi_app()
def fastapi_app():
    return web_app


@web_app.post("/submit")
async def submit_job_endpoint(data: dict):
    process_job = modal.Function.from_name("my-job-queue", "extract_email_data")

    call = process_job.spawn(data)
    return {"call_id": call.object_id}


@web_app.get("/result/{call_id}")
async def get_job_result_endpoint(call_id: str):
    function_call = modal.FunctionCall.from_id(call_id)
    try:
        result = function_call.get(timeout=0)
    except modal.exception.OutputExpiredError:
        return fastapi.responses.JSONResponse(content="", status_code=404)
    except TimeoutError:
        return fastapi.responses.JSONResponse(content="", status_code=202)

    return result