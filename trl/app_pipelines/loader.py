import importlib.util
from types import ModuleType
from typing import List
from trl.dsl import __DSL_IRS__

def load_user_irs(app_path: str) -> List[object]:
    __DSL_IRS__.clear()
    spec = importlib.util.spec_from_file_location("user_app", app_path)
    mod = importlib.util.module_from_spec(spec)  # type: ModuleType
    spec.loader.exec_module(mod)
    return list(__DSL_IRS__)
