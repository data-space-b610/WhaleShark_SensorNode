import pika
import json
from influxdb import InfluxDBClient


develop_host = '192.168.2.44'
develop_port = '8086'
develop_user = ''
develop_password = ''
develop_dbname = 'ankus4iot_mp6050'
develop_protocol = 'json'
develop_client = InfluxDBClient(develop_host, develop_port, develop_user, develop_password, develop_dbname)
# json_data = '{"mtime":"2019-05-10 09:08:53.155", "b": 2, "c": 3, "d": 4, "e": 5}'
# parsed_json = json.loads(json_data)
# dict_record = [
#         {
#             "measurement": "ankus4iot_mp6050",
#             "time": parsed_json['mtime'],
#             "fields": json.loads(json_data)
#         }
#     ]
# print(dict_record)
# develop_client.write_points(dict_record)

credentials = pika.PlainCredentials('rabbitmq', 'zx82qm73')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.2.44',5672, '/',  credentials))
channel = connection.channel()
channel.queue_declare(queue='mp6050')
import datetime
from datetime import timedelta
def callback(ch, method, properties, body):
    json_data = body
    json_data=str(json_data, 'utf-8')
    json_data ='{' + json_data  +'}'
    try:
        parsed_json = json.loads(json_data)
        date_time_obj = datetime.datetime.strptime(parsed_json['mtime'], '%Y-%m-%dT%H:%M:%SZ')
        date_time_obj = date_time_obj + timedelta(hours=9)
        dict_record = [
                {
                    "measurement": "ankus4iot_mp6050",
                    #"time": date_time_obj,
                    "fields": json.loads(json_data)
                }
            ]
        develop_client.write_points(dict_record)
        print(date_time_obj, parsed_json['acc_x'],parsed_json['acc_y'],parsed_json['acc_z'])
    except Exception as e:
        print(str(e))
        
channel.basic_consume('mp6050',callback,auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
