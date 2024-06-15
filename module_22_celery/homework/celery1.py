import uuid

from celery import Celery, group
from werkzeug.utils import secure_filename

from image import blur_image
from mail import send_email

celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@celery.task()
def process_image(src_file_name, subscribers):
    receivers = ', '.join(subscribers)

    order_id = uuid.uuid4()
    blur_file_name = f"blur_{src_file_name}"
    blur_image(src_file_name, blur_file_name)

    if subscribers:
        send_email(order_id, receivers, blur_file_name)


def process_images(images, subscribers):
    names = []

    for i_image in images:
        file = images[i_image]
        filename = secure_filename(file.filename)
        file.save(filename)
        names.append(filename)

    task_group = group(
        process_image.s(i_image, subscribers)
        for i_image in names
    )
    result = task_group.apply_async()
    result.save()

    return result.id


def restore(task_id):
    return celery.GroupResult.restore(task_id)
