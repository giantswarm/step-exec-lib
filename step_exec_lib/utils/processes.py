import logging
import subprocess  # nosec: we need it to invoke binaries from system
from typing import List, Any

logger = logging.getLogger(__name__)


def run_and_log(args: List[str], **kwargs: Any) -> subprocess.CompletedProcess:
    logger.info("Running command:")
    logger.info(" ".join(args))
    if "text" not in kwargs:
        kwargs["text"] = True

    run_res = subprocess.run(args, **kwargs)  # nosec
    logger.info(f"Command executed, exit code: {run_res.returncode}.")
    return run_res


def run_and_handle_error(args: List[str], error_text: str, **kwargs: Any) -> int:
    logger.info("Running command:")
    logger.info(" ".join(args))
    if "text" not in kwargs:
        kwargs["text"] = True

    try:
        run_res = subprocess.run(args, **kwargs, check=True, stderr=subprocess.PIPE)  # nosec
        logger.info(f"Command executed, exit code: {run_res.returncode}.")
        return run_res.returncode

    except subprocess.CalledProcessError as e:
        logger.info(f"CalledProcessError: {e}.")

        if error_text in e.stderr:
            logger.info(f"Found expected error text '{error_text}', exit code: 0")
            return 0
        else:
            logger.info(f"Did not find error text '{error_text}', exit code: 1")
            return 1
