from cricket_datastore_client import CricketDatastoreClient

def get_datastore_client(app_id: int = 0):
    """
    Returns DatastoreClient to interact with the datastore SC
    """
    if(app_id == 0):
        return CricketDatastoreClient()
    
    return CricketDatastoreClient(app_id)