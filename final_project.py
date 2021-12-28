#!usr/bin/env python
import argparse
import uuid
import datetime 
from manager import Tasks

__author__ = 'Zach Huang'

class Task:
  """Representation of a task
  
  Attributes:
    - name - string
    - priority - int value of 1, 2, or 3; 1 is default
    - created - date
    - unique id - number
    - completed - date
    - due date - date, this is optional
    """

  def __init__(self, name):
      self.name = name
      self.priority = 1
      self.created = datetime.datetime.utcnow()
      self.unique_id = uuid.uuid1()
      self.completed = None
      self.due_date = '-'

def main():
    parser = argparse.ArgumentParser(description='Update your to-do list.')
    parser.add_argument('--add', type=str, required=False, help='a task string to add to your list.')
    parser.add_argument('--priority', type=int, required=False, default=1, help='priority of task; default value is 1.')
    parser.add_argument('--due', type=str, required=False, help='due date in YYYY/MM/DD format.')
    parser.add_argument('--query', type=str, required=False, nargs='+', help='query task with keyword.')
    parser.add_argument('--list', action='store_true', required=False, help='list all tasks that have not been completed.')
    parser.add_argument('--delete', type=str, required=False, help='delete specific task.')
    parser.add_argument('--done', type=str, required=False, help='flag the task is done.')
    parser.add_argument('--report', action='store_true', required=False, help='list all completed/incompleted tasks.')

    # parse the argument
    args = parser.parse_args()

    # initiate Tasks() class
    task_list = Tasks()

    # initiate Task() class into Tasks list
    new_task = Task(args.add)
    new_task.priority = args.priority
    new_task.due_date = args.due

    if args.add:
        task_list.add(new_task)
    elif args.list:
        task_list.list()
    elif args.delete:
        task_list.delete(args.delete.strip())
    elif args.done:
        task_list.done(args.done.strip())
    elif args.query:
        task_list.query(args.query)
    elif args.report:
        task_list.report()

    
    task_list.pickle_tasks()
    exit()

if __name__ == '__main__':
    main()
        