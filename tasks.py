import csv


class TaskManager():

    def loadTasks(self):
        with open("tasks.csv") as tasks:
            tasks_csv = csv.DictReader(tasks)
            for task in tasks_csv:
                with open("profiles.csv") as profiles:
                    profiles_csv = csv.DictReader(profiles)
                    for profile in profiles_csv:
                        try:
                            if task['PROFILE'] == profile['PROFILE_NAME']:
                                self.profile = profile
                                self.task = task
                                print(task)
                                continue
                            else:
                                break
                        except Exception as e:
                            print(e)
                            continue
                    print(self.profile['FIRSTNAME'])


TaskManager().loadTasks()
