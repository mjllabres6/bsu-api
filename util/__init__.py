
def validate_data(body, model):
    data = {}
    columns = model.columns
    for col in columns:
        if col in body and type(body[col]) == columns[col]:
            data.update({col: body.get(col)})
        elif col in model.optional and col not in body:
            pass
        elif col not in body and col not in model.optional:
            return f"MISSING REQUIRED COLUMN {col}"
        else:
            return f"INVALID TYPE ON COLUMN {col}"
    return data
