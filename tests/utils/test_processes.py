from typing import List

import pytest

from step_exec_lib.utils.processes import run_and_handle_error


@pytest.mark.parametrize(
    "args,expected_error,exit_code",
    [
        (["echo", "ok"], "", 0),
        (["echo", "ok"], "blaaaaah", 0),
        (["bash", "-c", "echo 'wrooong' && false"], "blaaaaah", 1),
        (["bash", "-c", "echo 'wrooong' 1>&2 && false"], "ooo", 0),
    ],
)
def test_run_and_handle_error(
    args: List[str], expected_error: str, exit_code: int
) -> None:
    res = run_and_handle_error(args, expected_error)
    assert res.returncode == exit_code
