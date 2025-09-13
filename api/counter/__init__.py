# Written by saperez24
# Azure Function for Azure Resume Challenge

import logging
import os
import azure.functions as func
from azure.data.tables import TableServiceClient, TableEntity

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Visitor counter triggered.')

    # Get storage account connection string
    connection_string = os.getenv("AzureWebJobsStorage")
    table_name = "VisitorCounter"

    # Connect to Table Storage
    service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = service.get_table_client(table_name=table_name)

    # PartitionKey = "Counter", RowKey = "Resume"
    try:
        entity = table_client.get_entity(partition_key="Counter", row_key="Resume")
        entity["Count"] = entity["Count"] + 1
        table_client.update_entity(entity, mode="Merge")
    except:
        # If not exists, create it
        entity = TableEntity(PartitionKey="Counter", RowKey="Resume", Count=1)
        table_client.create_entity(entity)

    # Return the count
    return func.HttpResponse(
        str(entity["Count"]),
        status_code=200,
        headers={"Content-Type": "application/json"}
    )
