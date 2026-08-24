# OC2 Bot Examples

## Schedule a Typed Task

```python
from outflank_stage1.bot import BaseBot
from outflank_stage1.implant import Implant
from outflank_stage1.services.task_service import TaskService
from outflank_stage1.task.tasks import SleepTask


class AutoSleep(BaseBot):
    def on_new_implant(self, implant: Implant):
        TaskService().schedule_task(
            implant_uid=implant.get_uid(),
            task=SleepTask(interval=60, jitter=30),
        )
```

## Resolve an Implant for a Task Event

```python
import logging

from outflank_stage1.bot import BaseBot
from outflank_stage1.services.implant_service import ImplantService
from outflank_stage1.task import BaseTask


class TaskAuditBot(BaseBot):
    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self._implants = ImplantService()

    def on_task_response(self, task: BaseTask):
        implant_uid = task.get_implant_uid()
        if not implant_uid:
            return

        implant = self._implants.get_by_uid(implant_uid)
        if implant is not None:
            self._logger.info("Task response from %s", implant.get_uid())
```

Use `GenericTask("command")` in the first pattern when no typed task class exists. Keep counters or caches on `self` only when process-local state is sufficient.
