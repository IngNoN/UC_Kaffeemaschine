import azure.functions as func
import logging
import json

from azure.data.tables import TableServiceClient

# send to congratiulation message queue

from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Endpoint=sb://testbus-sk11.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=m0DutAhjDyytP+yxsmTfvevz4jtakRCfIbGsDq3fcQE="
QUEUE_NAME = "congratiulaiton_message_queue"


def main(msg: func.ServiceBusMessage):

    logging.info('Python ServiceBus queue trigger processed message.')

    result = msg.get_body().decode('utf-8')
    

    logging.info(result)

    resultDict = json.loads(result)
    logging.info(resultDict)
    
    #resultDict['body'] = "u\'" + resultDict['body'] + "\'"
    cmid = resultDict["cm_id"]
    
    logging.info(type(resultDict))

    PRODUCT_ID = u'00123411'
    PRODUCT_NAME = u'C'
    my_entity = {
        u'PartitionKey': "CM_"+cmid,
        u'RowKey': "CNT_"+resultDict["cmc"],
        u'type': resultDict["type"],
        u'amount': resultDict["amount"],
    }

    table_service_client = TableServiceClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=orderstoragecoffee;AccountKey=/HlYJsI+3aFvQijcIYYfvoX3wVZD81RaXS9xW56xKJWPE/QbgHmDKy6mNwTfBrmtcmYw9Y1nxw6A2yM/yxnM3Q==;EndpointSuffix=core.windows.net")
    table_client = table_service_client.get_table_client(table_name="coffeeData")

    srv_entity = table_client.create_entity(entity=my_entity)
    
    logging.info("before check every 50 coffee")
    check_every_50_coffee(cmid, resultDict["cmc"])
    logging.info("message queue succesfully executed")


def check_every_50_coffee(coffee_id, coffee_count):
    logging.info(int(coffee_count) % 50 == 0)
    if int(coffee_count) % 50 == 0:
        servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
        sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
        message = ServiceBusMessage(str(coffee_id))
        sender.send_messages(message)
        logging.info("Sent a single message")
    return