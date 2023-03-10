

def object_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/product_name/<filename>
    return '{0}/{1}'.format(instance.title, filename)