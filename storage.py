try:
    import io
    from io import BytesIO
    # import pandas as pd
    from google.cloud import storage

except Exception as e:
    print("Some Modules are Missing {}".format(e))

def add_to_cloudinary(cover, name_of_file):
    storage_client = storage.Client.from_service_account_json("property-runner-aaa5f5ba471b.json")
    # Create a Bucket object
    bucket = storage_client.get_bucket('property-runner')
    filename = "%s.%s" % ('', f'{name_of_file}')
    blob = bucket.blob(filename)

    filenames = []
    for file in storage_client.list_blobs(bucket):
        filenames.append(file.name)


    if f".{name_of_file}" not in filenames:
        blob.upload_from_string(cover)
    else:
        return "Error"

    print(f"New File: {name_of_file}")
    print(f"All Files: {filenames}")

    return "Success"

    # with open('Hayden.jpg', 'rb') as f:
    #     blob.upload_from_file(f)
    # print("Upload complete")