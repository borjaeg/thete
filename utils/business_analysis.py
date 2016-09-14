import pymysql.cursors
import pandas as pd

def get_plague_crops():

    results = []
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='fitosanitarios',
                             charset='utf8')

    try:
        sql = \
            """
            SELECT COUNT(*) num_productos -- , C.CultivosEnFitosanitarios, EfectosEnPlagas,
            FROM usoautorizado U
            LEFT JOIN cultivosenfitosanitarios C ON (U.CultivosEnFitosanitariosId = C.CultivosEnFitosanitariosId)
            LEFT JOIN efectosenplagas E ON (U.EfectosEnPlagasId = E.EfectosEnPlagasId)
            GROUP BY C.CultivosEnFitosanitariosId, E.EfectosEnPlagasId
            ORDER BY num_productos DESC;    
            """
        results = pd.read_sql(sql, connection)

    except Exception as e:
        print(e)
    finally:
        connection.close()

    return results 


def get_crops():

    results = []
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='fitosanitarios',
                             charset='utf8')

    try:
        sql = \
            """
            SELECT CultivosEnFitosanitarios, SUM(num_productos) AS num_productos
            FROM (
                SELECT C.CultivosEnFitosanitarios, EfectosEnPlagas, COUNT(*) num_productos
                FROM usoautorizado U
                LEFT JOIN cultivosenfitosanitarios C ON (U.CultivosEnFitosanitariosId = C.CultivosEnFitosanitariosId)
                LEFT JOIN efectosenplagas E ON (U.EfectosEnPlagasId = E.EfectosEnPlagasId)
                GROUP BY C.CultivosEnFitosanitariosId, E.EfectosEnPlagasId
                ORDER BY num_productos DESC
            ) T
            GROUP BY CultivosEnFitosanitarios
            ORDER BY num_productos DESC;  
            """
        results = pd.read_sql(sql, connection)

    except Exception as e:
        print(e)
    finally:
        connection.close()

    return results


def get_plagues():

    results = []
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='fitosanitarios',
                             charset='utf8')

    try:
        sql = \
            """
            SELECT EfectosEnPlagas, SUM(num_productos) AS num_productos
            FROM (
                SELECT C.CultivosEnFitosanitarios, EfectosEnPlagas, COUNT(*) num_productos
                FROM usoautorizado U
                LEFT JOIN cultivosenfitosanitarios C ON (U.CultivosEnFitosanitariosId = C.CultivosEnFitosanitariosId)
                LEFT JOIN efectosenplagas E ON (U.EfectosEnPlagasId = E.EfectosEnPlagasId)
                GROUP BY C.CultivosEnFitosanitariosId, E.EfectosEnPlagasId
                ORDER BY num_productos DESC
            ) T
            GROUP BY EfectosEnPlagas
            ORDER BY num_productos DESC;   
            """
        results = pd.read_sql(sql, connection)

    except Exception as e:
        print(e)
    finally:
        connection.close()

    return results

def get_tuples():

    results = []
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='fitosanitarios',
                             charset='utf8')

    try:
        sql = \
            """
            SELECT CONCAT(C.CultivosEnFitosanitarios, '-' , EfectosEnPlagas) AS tuple
            FROM usoautorizado U
            LEFT JOIN cultivosenfitosanitarios C ON (U.CultivosEnFitosanitariosId = C.CultivosEnFitosanitariosId)
            LEFT JOIN efectosenplagas E ON (U.EfectosEnPlagasId = E.EfectosEnPlagasId)
            GROUP BY C.CultivosEnFitosanitariosId, E.EfectosEnPlagasId, UsoAutorizadoRegistro
            ORDER BY C.CultivosEnFitosanitarios ASC, EfectosEnPlagas ASC; 
            """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

    except Exception as e:
        print(e)
    finally:
        connection.close()

    return results  


def get_grouped_tuples():

    results = []
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='fitosanitarios',
                             charset='utf8')

    try:
        sql = \
            """
            SELECT C.CultivosEnFitosanitarios, EfectosEnPlagas
            FROM usoautorizado U
            LEFT JOIN cultivosenfitosanitarios C ON (U.CultivosEnFitosanitariosId = C.CultivosEnFitosanitariosId)
            LEFT JOIN efectosenplagas E ON (U.EfectosEnPlagasId = E.EfectosEnPlagasId)
            GROUP BY C.CultivosEnFitosanitariosId, E.EfectosEnPlagasId
            ORDER BY C.CultivosEnFitosanitarios ASC, EfectosEnPlagas ASC;    
            """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

    except Exception as e:
        print(e)
    finally:
        connection.close()

    return results 



