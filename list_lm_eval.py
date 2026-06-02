from lm_eval.tasks import TaskManager

tm = TaskManager()

mmlu_tasks = [t for t in tm.all_tasks if "gpqa" in t.lower()]
print(mmlu_tasks, "\n")