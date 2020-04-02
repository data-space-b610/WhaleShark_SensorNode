import pika
import mpu6050
from datetime import datetime
credentials = pika.PlainCredentials('rabbitmq', 'zx82qm73')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.2.44',5672, '/',  credentials))
channel = connection.channel()


channel.queue_declare(queue='mp6050')
import time
while True:
    now = datetime.now()
    dt_string=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    try:
        gyro_xout, gyro_yout ,gyro_zout, accel_xout_scaled, accel_yout_scaled,accel_zout_scaled= mpu6050.read_mp6050()
        message='"mtime":"{m_time}","gyro_x":{gy_x},"gyro_y":{gy_y},"gyro_z":{gy_z},"acc_x":{acc_x},"acc_y":{acc_y},"acc_z":{acc_z}'.format(
                                                                                                        m_time=dt_string,
                                                                                                        gy_x=gyro_xout,
                                                                                                         gy_y=gyro_yout,
                                                                                                         gy_z=gyro_zout,
                                                                                                         acc_x=accel_xout_scaled,
                                                                                                         acc_y=accel_yout_scaled,
                                                                                                         acc_z=accel_zout_scaled)

        channel.basic_publish(exchange='',
                          routing_key='mp6050',
                          body=message)
    except Exception as e:
        print(e)
    time.sleep(0.5)
connection.close()
