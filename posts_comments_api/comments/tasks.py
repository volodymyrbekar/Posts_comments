from celery import shared_task
from .models import Comments
from users.models import User
from django.core.exceptions import ObjectDoesNotExist
from toxicity_checker import generate_ai_reply


@shared_task
def schedule_auto_reply(comment_id):
    try:
        comment = Comments.objects.get(id=comment_id)
        user = User.objects.get(id=comment.user_id)
        # Generate the auto-reply
        message = generate_ai_reply(comment.content)
        # Send the auto-reply
        Comments.objects.create(user_id=user.id, post_id=comment.post_id, content=message)
    except ObjectDoesNotExist:
        pass
