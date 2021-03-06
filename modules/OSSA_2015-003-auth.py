__author__ = 'pranali.deore'

from glanceclient import Client

import datetime
import time
import uuid

total_images_created = 0
deleted_in_saving_state = 0
total_images_deleted = 0

OS_AUTH_TOKEN = "65d763d51eaa4853aebcd33b78ddab4a"
OS_IMAGE_ENDPOINT = "http://10.69.4.176:9292/v1"
file_location = "http://releases.ubuntu.com/14.10/ubuntu-14.10-server-i386.iso"

glance = Client('1', endpoint=OS_IMAGE_ENDPOINT, token=OS_AUTH_TOKEN)


def create_delete_image():
    id = str(uuid.uuid4())
    image = glance.images.create(name=id,
                                 copy_from=file_location,
                                 disk_format='ami')
    global total_images_created, deleted_in_saving_state, total_images_deleted
    total_images_created += 1
    print("Image status = = %s" % image.status)

    #Initially image goes into queued state hence added sleep here
    time.sleep(3)

    image = glance.images.get(image.id)
    if image.status == "saving":
        print("Image status = = %s" % image.status)
        glance.images.delete(image)
        print("Image %s deleted in saving state" % image.id)
        deleted_in_saving_state += 1
    else:
        # if image status is set to active after 3 sec of sleep
        # delete the image
        glance.images.delete(image)

    #number of total deleted images
    total_images_deleted += 1



if __name__ == '__main__':
    start_time = datetime.datetime.now()
    duration = 3600 #in seconds
    stop_time = time.mktime(start_time.timetuple()) + duration

    while 1:
        create_delete_image()
        t = time.time()
        if t >= stop_time:
            break

    print 'Total images created', total_images_created
    print 'Images deleted in saving state ', deleted_in_saving_state
    print 'Total images deleted ', total_images_deleted
