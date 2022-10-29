import psycopg2
import nums_from_string
import datetime
from .config import db_config

def push2dB(body):
    try:   
        conn = psycopg2.connect(user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'],
                                port = db_config['port'],
                                connect_timeout=20)
        
        cursor = conn.cursor()
        date = body["Time"].split(" ")[1]
        dt = datetime.datetime.strptime(date, '%d/%m/%Y')
        dt =  ('{0}-{1}-{2:02}'.format(dt.year, dt.month, dt.day ))
        insert_query="""INSERT INTO public.readings("device_id","Acc","Gyro","Temp","BPM","Date","Time") VALUES 
                        (%(device_id)s,%(Acc)s,%(Gyro)s,%(Temp)s,%(BPM)s,%(Date)s,%(Time)s) 
                        RETURNING id;"""
        records_to_insert= {"Acc":body["Acc"],"Gyro":body["Gcc"],
                            "Temp":float(body["Temp"]),"BPM":float(body["BPM"]),"device_id":3,
                            "Date":dt,"Time":body["Time"].split(" ")[0]}
        cursor.execute(insert_query,records_to_insert)
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Data successfully inserted"}
    except Exception as e:
        return {"message": str(e)}

