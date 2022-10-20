import psycopg2
from .config import db_config

def push2dB(body):
    try:   
        conn = psycopg2.connect(user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'],
                                port = db_config['port'],
                                connect_timeout=20)
        
        cursor = conn.cursor()
        insert_query="""INSERT INTO public.readings("device_id","Ax","Ay","Az","Gx","Gy","Gz","BPM") VALUES 
                        (%(device_id)s,%(Ax)s,%(Ay)s,%(Az)s,%(Gx)s,%(Gy)s,%(Gz)s,%(BPM)s) 
                        RETURNING id;"""
        records_to_insert= {"Ax":float(body["ax"]),"Ay":float(body["ay"]),"Az":float(body["az"]),"Gx":float(body["gx"]),
                "Gy":float(body["gy"]),"Gz":float(body["gz"]),"BPM":int(body["BPM"]),"device_id":int(body["device_id"])}
        cursor.execute(insert_query,records_to_insert)
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Data successfully inserted"}
    except Exception as e:
        return {"message": str(e)}
