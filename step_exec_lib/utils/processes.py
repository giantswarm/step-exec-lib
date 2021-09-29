import logging
import subprocess  # nosec: we need it to invoke binaries from system
from typing import List, Any

logger = logging.getLogger(__name__)

_GITHUB_TOKEN_ARG = "--github-token"  # nosec


def run_and_log(args: List[str], **kwargs: Any) -> subprocess.CompletedProcess:
    logger.info("ARGS:")
    logger.info(" ".join(args))

    sanitized_args = sanitize_args(args)

    logger.info("SANITIZED:")
    logger.info(" ".join(sanitized_args))

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
        if arg.startswith(_GITHUB_TOKEN_ARG):
            res.append(f"{_GITHUB_TOKEN_ARG}=*****")
        else:
            res.append(arg)

    return res
