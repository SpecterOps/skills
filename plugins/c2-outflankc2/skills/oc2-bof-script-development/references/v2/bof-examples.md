# OC2 V2 BOF Wrapper Examples

## Minimal Wrapper

File: `env_bof.s1.py`

```python
from outflank_stage1.task.base_bof_task import BaseBOFTask


class EnvBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("env")
        self.parser.description = "List environment variables."
```

With default naming, this loads `env.<arch>.o` from the same directory.

## Constrained Typed Argument

File: `untrustprocess_bof.s1.py`

```python
from typing import List, Tuple

from outflank_stage1.implant.enums import ImplantArch, ImplantPrivilege
from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding


class UntrustProcessBOF(BaseBOFTask):
    def __init__(self):
        super().__init__(
            "untrustprocess",
            min_privilege=ImplantPrivilege.HIGH,
            supported_architectures=[ImplantArch.INTEL_X64],
        )
        self.parser.add_argument("process", help="PID or process name.")
        self.parser.description = "Lower a process token integrity level."
        self.parser.epilog = (
            "Example usage:\n"
            "  - untrustprocess 1337\n"
            "  - untrustprocess firefox.exe\n"
        )

    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        return [(BOFArgumentEncoding.WSTR, arguments[0])]
```

For optional or variant arguments, parse once and build the tuple list conditionally. Constrain any value used by `_get_base_binary_name()` with `choices=`.
