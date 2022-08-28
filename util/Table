
class Table(object):
    def __init__(self, name, columns):
        self.name = ""
        self.columns = columns.keys()
    
    def select(self, columns, where, order_by):
        query = "SELECT "
        model_columns = tuple(self.columns)

        if columns: 
            query += str(tuple(columns))

        else:
            query += str(model_columns)

        query += f"FROM {self.name} "
        
        if where:
            columns = where.keys()
            
            query =+ "WHERE"
            for column in columns:
                query += f"{column} = {columns[column]}"
            
        if order_by:
            query += f"ORDER BY {order_by}"
            if order_by[:-1] == "-":
                query += " DESC"
                
        
