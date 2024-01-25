from adminpage.models import Task, UserTask, Notification

def task():
    tasks = Task.objects.all()
    for task in tasks:
        if task.task_time == "Her Gün":
            task.is_completed = False
            user_task = UserTask.objects.filter(task=task)
            for user in user_task:
                Notification.objects.create(user=user.user, noti_type="9", task_id=task.id, title="Yeni görev ataması yapıldı.")