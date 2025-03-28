import json
import logging
import os

import azure.functions as func
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from azure.storage.queue import QueueClient, QueueServiceClient

app = func.FunctionApp()

# Replace with your actual connection string
connection_string = os.getenv("AzureWebJobsStorage")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Getting 'name' from the query or body
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        # Example: Upload a file to Blob Storage
        try:
            # Choose the container and blob name
            container_name = "container1"
            blob_name = f"hello_{name}.txt"
            container_client = blob_service_client.get_container_client(container_name)
            
            # Uploading a file to blob
            blob_client = container_client.get_blob_client(blob_name)
            data = f"Hello, {name}. This file was created using Azure Functions."
            blob_client.upload_blob(data, overwrite=True)  # Uploading the data to the blob
            
            logging.info(f"Uploaded blob {blob_name} to container {container_name}.")
            return func.HttpResponse(f"Blob for {name} uploaded successfully.", status_code=200)

        except Exception as e:
            logging.error(f"Error uploading blob: {str(e)}")
            return func.HttpResponse(f"Error uploading blob: {str(e)}", status_code=500)
        
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
