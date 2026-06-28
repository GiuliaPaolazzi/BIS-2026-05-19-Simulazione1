from database.DB_connect import DBConnect
from model.arco import Arco
from model.artista import Artist
from model.genere import Genere


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGeneri():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct g.GenreId, g.Name 
                    from genre g 
                    order by g.Name """

        cursor.execute(query)

        for row in cursor:
            results.append(Genere(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArtisti(g):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId , a.Name 
from artist a, track t , album a2 
where a.ArtistId =a2.ArtistId and t.AlbumId = a2.AlbumId 
and t.GenreId = %s"""

        cursor.execute(query,(g.GenreId,))

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArchi(g, idMapA):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t1.AID as AID1, t2.AID as AID2
from (select i.CustomerId as CID, a.ArtistId as AID
from  track t , album a, invoice i , invoiceline il 
where  t.AlbumId = a.AlbumId and i.InvoiceId = il.InvoiceId and il.TrackId =t.TrackId 
and t.GenreId = %s )t1, (select i.CustomerId as CID, a.ArtistId as AID
from  track t , album a, invoice i , invoiceline il 
where  t.AlbumId = a.AlbumId and i.InvoiceId = il.InvoiceId and il.TrackId =t.TrackId 
and t.GenreId = %s )t2
where t1.CID = t2.CID and t1.AID < t2.AID"""

        cursor.execute(query, (g.GenreId,g.GenreId))

        for row in cursor:
            results.append(Arco(idMapA[row["AID1"]],idMapA[row["AID2"]]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllPopolarita(g):
        conn = DBConnect.get_connection()

        results = {}

        cursor = conn.cursor(dictionary=True)
        query = """select a.ArtistId as AID, sum(il.Quantity) as pop
from invoiceline il, track t , album a 
where t.AlbumId = a.AlbumId and il.TrackId =t.TrackId and t.GenreId = %s
group by a.ArtistId """

        cursor.execute(query,(g.GenreId,))

        for row in cursor:
            results[row["AID"]] = row["pop"]

        cursor.close()
        conn.close()
        return results

