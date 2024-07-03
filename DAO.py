from database.DB_connect import DBConnect
from model.artObject import ArtObject
from model.connessioni import Connessione
from model.artista import Artista

class DAO():

    @staticmethod
    def getRoles():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = "SELECT distinct role FROM authorship order by role"
        cursor.execute(query, )

        for row in cursor:
            result.append(row[0])
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtists(role):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""SELECT a.* 
                 FROM artists a, authorship at
                 where a.artist_id = at.artist_id and at.role = %s""")
        cursor.execute(query, (role,))

        for row in cursor:
            result.append(Artista(**row))
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(artista1, artista2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
                select a1.artist_id as art1, a2.artist_id as art2
                from authorship a1, authorship a2, exhibition_objects e1, exhibition_objects e2
                where a1.artist_id = %s and a2.artist_id = %s and
                e1.exhibition_id = e2.exhibition_id and a1.object_id = e1.object_id
                and e2.object_id = a2.object_id
                
                """)
        cursor.execute(query, (artista1, artista2))

        for row in cursor:
            result.append((row["art1"], row["art2"]))
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(artista1, artista2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
                    select count(distinct e1.exhibition_id) as peso, a1.artist_id as art1, a2.artist_id as art2
                    from authorship a1, authorship a2, exhibition_objects e1, exhibition_objects e2
                    where a1.artist_id = %s and a2.artist_id = %s and
                    e1.exhibition_id = e2.exhibition_id and a1.object_id = e1.object_id
                    and e2.object_id = a2.object_id
                    group by art1, art2
                    """)
        cursor.execute(query, (artista1, artista2))

        for row in cursor:
            result.append(row["peso"])
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result


