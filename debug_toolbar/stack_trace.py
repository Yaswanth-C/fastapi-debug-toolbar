import inspect
import linecache
from typing import List, Dict, Any

def get_stack_trace() -> List[Dict[str, Any]]:
    stack_trace = []
    # skip the first 2 frames to remove this function and its caller.
    for frame in inspect.stack()[2:]:
        data = {
            "func": frame.function,
            "file": frame.filename,
            "lineno": frame.lineno,
            "code": linecache.getline(frame.filename, frame.lineno).strip(),
        }
        stack_trace.append(data)
    return stack_trace
