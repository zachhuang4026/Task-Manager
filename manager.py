#!usr/bin/env python
from os import path
import pickle
import datetime

__author__ = 'Zach Huang'

class Tasks:
    def __init__(self):
        """Read picked tasks file into a list"""
        if path.exists('.todo.pickle'):
            with open('.todo.pickle', 'rb') as f:
                self.tasks = pickle.load(f)
                # convert date into string and sorted by due date
                self.tasks.sort(key=lambda x: str(x.due_date))
        else:
            self.tasks = []
        
    def pickle_tasks(self):
        """Pickle task list into a file (last step before the program ends)"""
        with open('.todo.pickle', 'wb') as f:
            pickle.dump(self.tasks, f)


    def add(self, task):
        """add task into task list"""
        # if the task name is not a string, ask user to input again
        try:
            type(float(task.name)) == float
            print('There was an error in creating your task. Run "todo -h" for usage instructions.')
        
        except:
            self.tasks.append(task)
            print('Created task %s' % task.unique_id)


    def date_diff(self, created_date):
        """Method to calculate the day difference between given date and today"""
        today = datetime.date.today()

        # created date is default as datetime, need to convert to date
        created_day = created_date.date()
        diff = today - created_day
        age = diff.days + 1

        return age

    def print_header(self, tasks):
        """Method for list(), which can format the printout style"""
        space = ' '
        dash = '-'
        id_len = len((str(tasks[-1].unique_id)))

        # the items need to be printed
        print('ID', space*(id_len), \
                'Age', space*2,\
                'Due Date', space*4, \
                'Priority', space*4, \
                'Task')
        # formatting
        print(dash*id_len, space*2, \
            dash*3, space*2, \
            dash*10, space*2, \
            dash*10, space*2, 
            dash*10)

    def list(self):
        """list all incompleted tasks"""
        try:
            self.print_header(self.tasks)
            space = ' '

            for t in self.tasks:
                if t.completed is None:
                    age = self.date_diff(t.created)
                    age_len = len(str(age))
                    due_len = len(str(t.due_date))
                    prior_len = len(str(t.priority))

                    # formatting the varibales
                    print(t.unique_id, space*2, \
                        str(age) + 'd', space*(3-age_len+1),\
                        t.due_date, space*(10-due_len+2),\
                        t.priority, space*(8-prior_len+4), \
                        t.name)
        except:
            print('Empty.')


    def done(self, id):
        """if the task is done, update the flag 'completed' with the current datetime"""
        for t in self.tasks:
            # find by given id
            if str(t.unique_id) == id:
                # update with datetime
                t.completed = datetime.datetime.utcnow()
        print('Completed task', id)

    def query(self, keywords):
        """query tasks with a list of keywords"""
        try:
            space = ' '
            self.print_header(self.tasks)

            # create a set in case multiple keywords all appears in one task
            seen = set()
            for keyword in keywords:
                for t in self.tasks:
                    if keyword.lower() in t.name.lower() and t.completed is None:
                        seen.add(t)

            # sort the set by the due date
            seen_list = sorted(seen, key=lambda x: str(x.due_date))

            for t in seen_list:
                age = self.date_diff(t.created)
                age_len = len(str(age))
                due_len = len(str(t.due_date))
                prior_len = len(str(t.priority))

                print(t.unique_id, space*2, \
                    str(age) + 'd', space*(3-age_len+1),\
                    t.due_date, space*(10-due_len+2),\
                    t.priority, space*(8-prior_len+4), \
                    t.name)
        except:
            print('Inavlid keyword.')

    def delete(self, id):
        """delete task by unique id"""
        for t in self.tasks:
            # if the unique id equals to given id, delete it
            if str(t.unique_id) == id:
                self.tasks.remove(t)
        print('Deleted task', t.unique_id)


    def report_header(self, tasks):
        """customized printing format for report()"""
        space = ' '
        dash = '-'
        id_len = len((str(tasks[-1].unique_id)))
        print('ID', space*(id_len), \
                'Age', space*2,\
                'Due Date', space*4, \
                'Priority', space*4, \
                'Task', space*18, \
                'Created', space*23, \
                'Completed')
        print(dash*id_len, space*2, \
            dash*3, space*2, \
            dash*10, space*2, \
            dash*10, space*2, \
            dash*20, space*2, \
            dash*28, space*2, \
            dash*28)

    def report(self):
        """report incompleted/completed tasks"""
        try:
            self.report_header(self.tasks)
            space = ' '
            for t in self.tasks:
                age = self.date_diff(t.created)
                age_len = len(str(age))
                due_len = len(str(t.due_date))
                prior_len = len(str(t.priority))
                name_len = len(str(t.name))
                created_len = len(str(t.created))

                print(t.unique_id, space*2, \
                    str(age) + 'd', space*(3-age_len+1),\
                    t.due_date, space*(10-due_len+2),\
                    t.priority, space*(8-prior_len+4), \
                    t.name, space*(20-name_len+2), \
                    self.precise_time(t.created), space*2, \
                    self.precise_time(t.completed))
        except:
            print('Empty.')

    def precise_time(self, date_time):
        """convert datetime to weekday/month/day/time/time zone/year"""
        if date_time is not None:
            weekday_dict = {0:'Mon', 1:'Tue', 2:'Wed',
                            3:'Thr', 4:'Fri', 5:'Sat', 6:'Sun'}
            month_dict = {1:'Jan', 2:'Feb', 3:'Mar',
                        4:'Apr', 5:'May', 6:'Jun',
                        7:'Jul', 8:'Aug', 9:'Sep',
                        10:'Oct', 11:'Nov', 12:'Dec'}                
            weekday = weekday_dict[date_time.weekday()]
            month = month_dict[date_time.month]
            day = date_time.day
            time = date_time.time().strftime("%H:%M:%S")

            # extract time zone: https://www.codegrepper.com/code-examples/python/python+get+timezone+from+datetime
            local_now = date_time.astimezone()
            local_tz = local_now.tzinfo
            tzname = local_tz.tzname(local_now)
            year = date_time.year

            return '%s %s %i %s %s %i' % (weekday, month, day, time, tzname, year)
        
        else:
            return '-'

