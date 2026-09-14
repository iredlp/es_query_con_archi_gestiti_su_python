from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    def getAllNodes(city):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM customers WHERE city = %s"
        cursor.execute(query, (city,))
        results = [Cliente(**row) for row in cursor]
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getSpesaClienti(city, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT c.customer_id, 
                   SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS spesa_totale
            FROM customers c, orders o, order_items oi
            WHERE c.customer_id = o.customer_id
              AND o.order_id = oi.order_id
              AND c.city = %s
              AND YEAR(o.order_date) = %s
            GROUP BY c.customer_id
        """
        cursor.execute(query, (city, anno))
        # Salviamo come mappa {id: spesa} o lista di tuple
        results = {row["customer_id"]: float(row["spesa_totale"]) for row in cursor}
        cursor.close()
        conn.close()
        return results



    class DAO:
        @staticmethod
        def getAllNodes2(city):
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM customers WHERE city = %s"
            cursor.execute(query, (city,))
            results = [Cliente(**row) for row in cursor]
            cursor.close()
            conn.close()
            return results

        @staticmethod
        def getSpesaClienti2(city, anno):
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT c.customer_id, 
                       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS spesa_totale
                FROM customers c, orders o, order_items oi
                WHERE c.customer_id = o.customer_id
                  AND o.order_id = oi.order_id
                  AND c.city = %s
                  AND YEAR(o.order_date) = %s
                GROUP BY c.customer_id
            """
            cursor.execute(query, (city, anno))
            # Salviamo come dizionario comodo: {customer_id: spesa}
            results = {row["customer_id"]: float(row["spesa_totale"]) for row in cursor}
            cursor.close()
            conn.close()
            return results