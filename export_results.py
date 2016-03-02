import pymysql.cursors

def delete_results():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='agriculture_experiments',
                             charset='utf8')

    try:
        with connection.cursor() as cursor:
            sql = "TRUNCATE results"
            cursor.execute(sql)
            connection.commit()

    finally:
        connection.close()   
    

def write_result(extraction, model, false_negatives, false_positives):
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='agriculture_experiments',
                             charset='utf8')

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO results VALUES(%s, %s, %s,%s,%s)"
            cursor.execute(sql, (model.split(' ')[0], extraction, model.split(' ')[1], 
                    float(false_negatives * 100), float(false_positives * 100)))
            connection.commit()

    finally:
        connection.close()