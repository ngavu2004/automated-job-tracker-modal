# my_job_queue.py
import modal




app = modal.App("my-job-queue")

image_with_module = (modal.Image.debian_slim()
                     .pip_install("openai", "jsonschema")
                     .add_local_python_source("parsers"))


@app.function(secrets=[modal.Secret.from_name("openai-secret")], image=image_with_module)
def extract_email_data(data: dict):
    from parsers import OpenAIExtractor
    openai_extractor = OpenAIExtractor()

    subject = data.get("subject", "")
    body = data.get("body", "")
    response = openai_extractor.get_response(subject, body)
    job_title = response.get("job_title", None)
    company_name = response.get("company_name", None)
    application_status = response.get("status", None)
    is_job_application_email = response.get("is_job_application_email", False)

    print(f"Extracted Data: {job_title}, {company_name}, {application_status}, {is_job_application_email}")
    return is_job_application_email, job_title, company_name, application_status