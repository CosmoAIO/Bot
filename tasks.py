import csv
import json


class TaskManager():
    def __init__(self, file):
        self.file = file

    # either in 'loadTasks' or 'returnTasks' add a list which stores two distionary "task-info" & "profile-info". append each task-info and profile-info for each task created eg:
    # task: {task1, task-info:, profile-info}, {task2. task-info:, profile-info:} etc....

    def loadTasks(self):
        print("Loading tasks.")

        self.tasks = []
        with open(self.file) as tasks:
            tasks_csv = csv.DictReader(tasks)
            for task in tasks_csv:
                with open("profiles.json") as profiles:
                    profiles_json = json.load(profiles)
                    for profile in profiles_json['profiles']:
                        try:
                            if task['PROFILE'] == profile['profileName']:
                                self.profile = profile
                                self.task = task
                                self.tasks.append(task)
                                print(task)
                            else:
                                continue
                        except Exception as e:
                            print(e)

        i = len(self.tasks)
        print(f"Loaded {i} tasks.")

    def returnTasks(self):
        pass


task = TaskManager("tasks.csv")  # can use ("{foldername}/tasks.csv") to get a directory location
task.loadTasks()
