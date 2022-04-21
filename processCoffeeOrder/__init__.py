
from unittest import result
import azure.functions as func

import logging
import json

from azure.data.tables import TableServiceClient
from datetime import datetime

def main(msg: func.ServiceBusMessage):
    logging.info('Python ServiceBus queue trigger processed message.')

    result = json.dumps({
        'body': msg.get_body().decode('utf-8')
    }, default=str)

    logging.info(result)

    resultDict = json.loads(result)
    logging.info(resultDict)
    
    #resultDict['body'] = "u\'" + resultDict['body'] + "\'"
    logging.info(resultDict)
    PRODUCT_ID = u'00123411'
    PRODUCT_NAME = u'B'

    data = resultDict['body'].split(",")

    my_entity = {
        u'PartitionKey': PRODUCT_NAME,
        u'RowKey': PRODUCT_ID,
        u'type': data[0],
        u'amount': data[1],
    }


    table_service_client = TableServiceClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=orderstoragecoffee;AccountKey=/HlYJsI+3aFvQijcIYYfvoX3wVZD81RaXS9xW56xKJWPE/QbgHmDKy6mNwTfBrmtcmYw9Y1nxw6A2yM/yxnM3Q==;EndpointSuffix=core.windows.net")
    table_client = table_service_client.get_table_client(table_name="coffeeData")

    entity = table_client.create_entity(entity=my_entity)

