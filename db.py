import psycopg2


db_config = {'user' : 'postgres',
            'password' : 'onlilo123',
            'host' :'database-1.cmqsecpalehs.ap-south-1.rds.amazonaws.com',
            'port' : '5432'
            }

def push2dB(body):
    try:   
        conn = psycopg2.connect(user = db_config['user'],
                                password = db_config['password'],
                                host = db_config['host'],
                                port = db_config['port'],
                                connect_timeout=20)
        
        cursor = conn.cursor()
        insert_query="""INSERT INTO public.readings("Ax","Ay","Az","Gx","Gy","Gz","BPM","value") VALUES 
                        (%(Ax)s,%(Ay)s,%(Az)s,%(Gx)s,%(Gy)s,%(Gz)s,%(BPM)s,%(value)s) 
                        RETURNING id;"""
        records_to_insert= {"Ax":float(body["ax"]),"Ay":float(body["ay"]),"Az":float(body["az"]),"Gx":float(body["gx"]),
                "Gy":float(body["gy"]),"Gz":float(body["gz"]),"BPM":int(body["BPM"]),"value":int(body["value"])}
        cursor.execute(insert_query,records_to_insert)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status":200,"message": "Data successfully inserted"}
    except Exception as e:
        return {"status":500,"message": str(e)}
