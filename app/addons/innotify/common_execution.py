from app.addons.innotify.task_registrator import TaskRegistrator
from app.models.queue.task_executor import TaskExecutor

def threaded_task_scheduler(**data):
    pool_name = data["pool_name"]
    # print(" @@@@ threaded_task_scheduler-%s" % pool_name)
    notifier = TaskRegistrator(pool_name)
    while notifier.run(pool_name):
        print(" ### %s ## TaskAllocator().allocate_task(pool_name) ..." % pool_name)
        # print(" ### %s ## TaskAllocator().allocate_task(pool_name) ..." % notifier.get_pool_name())
        if notifier.get_data() is not None:
            TaskExecutor().execute_task(notifier.get_data())

    print(" Thread-%s -- Selesai ." % pool_name)

