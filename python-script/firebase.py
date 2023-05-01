import datetime
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://iot-project-2b9fb-default-rtdb.europe-west1.firebasedatabase.app/"})

def update_firebase_data(data, reference_name = "default", DEBUG = False):  
  try:
    time_stamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    keys_to_add_timestamp = [key for key in data.keys()]
    for key in keys_to_add_timestamp:
      data[str(key)+"_timestamp"] = time_stamp

    ref = db.reference(reference_name)
    ref.update(data)

    if DEBUG:
      print("Data updated successfully", data)
  except Exception as e:
    print("Error while updating firebase data: ", e)
    return False
