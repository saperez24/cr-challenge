import os
import azure.functions as func
from azure.data.tables import TableServiceClient, UpdateMode
from azure.core.exceptions import ResourceNotFoundError

# Environment variable for Table Storage connection string
TABLE_CONN_STR = os.environ["TABLE_STORAGE_CONNECTION_STRING"]
TABLE_NAME = "VisitorCounter"
PARTITION_KEY = "visitors"
ROW_KEY = "count"

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Connect to the Table Storage
        service = TableServiceClient.from_connection_string(conn_str=TABLE_CONN_STR)
        table_client = service.get_table_client(table_name=TABLE_NAME)

        # Get the current counter
        try:
            entity = table_client.get_entity(partition_key=PARTITION_KEY, row_key=ROW_KEY)
            count = entity.get("count", 0)
        except ResourceNotFoundError:
            # Entity doesn't exist yet
            count = 0
            table_client.create_entity({
                "PartitionKey": PARTITION_KEY,
                "RowKey": ROW_KEY,
                "count": count
            })

        # Increment and update
        count += 1
        table_client.update_entity({
            "PartitionKey": PARTITION_KEY,
            "RowKey": ROW_KEY,
            "count": count
        }, mode=UpdateMode.REPLACE)

        return func.HttpResponse(f"Visitor count: {count}", status_code=200)

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
