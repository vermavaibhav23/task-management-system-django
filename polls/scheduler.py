from polls.models import Task
import heapq


class TaskScheduler:
    PRIORITY_MAP = {'high': 1, 'medium': 2, 'low': 3}

    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_next_tasks(self):
        pending_tasks = Task.objects.filter(user=self.user_id, status='pending')
        self.heap = []
        for task in pending_tasks:
            # custom order can be implemented later
            heapq.heappush(self.heap, (self.PRIORITY_MAP[task.priority], task.timestamp, task))

        sorted_tasks = []
        while self.heap:
            _, _, task = heapq.heappop(self.heap)
            sorted_tasks.append(task)

        return sorted_tasks

    def run_pending_tasks(self):
        sorted_tasks = self.get_next_tasks()

        for task in sorted_tasks:
            # execute task here
            task.status = 'completed'
            task.save()

        return sorted_tasks
