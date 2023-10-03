# Functions

def path_to_upload_img(instance, filename):
    return f"{instance.user.id}/images/{instance.id}/{filename}"
