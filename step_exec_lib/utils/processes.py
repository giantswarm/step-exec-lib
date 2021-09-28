import logging
import subprocess  # nosec: we need it to invoke binaries from system
from typing import List, Any

logger = logging.getLogger(__name__)

_TOKEN_ARG = "--github-token"

def run_and_log(args: List[str], **kwargs: Any) -> subprocess.CompletedProcess:
    sanitized_args = sanitize_args(args)

    logger.info("Running command:")
    logger.info(" ".join(sanitized_args))
    if "text" not in kwargs:
        kwargs["text"] = True
    run_res = subprocess.run(args, **kwargs)  # nosec
    logger.info(f"Command executed, exit code: {run_res.returncode}.")
    return run_res

def sanitize_args(args: List[str]) -> List[str]:
    """
    Sanitizes credentials that should not be logged.
    :param args: List of string args.
    :return: Sanitized list of string args.
    """

    res = []

    for arg in args:
        if arg.startswith(_TOKEN_ARG):
            res.append(f"{_TOKEN_ARG}=*****")
        else:
            res.append(arg)

    return res
