def process_data(payload: dict):
    value = payload.get("value", 0)
    return {"original":value, "doubled":value*2}