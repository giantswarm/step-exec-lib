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


def run_and_handle_error(args: List[str], expected_error_text: str, **kwargs: Any) -> int:
    logger.info("Running command:")
    logger.info(" ".join(args))
    if "text" not in kwargs:
        kwargs["text"] = True

    try:
        run_res = subprocess.run(args, **kwargs, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # nosec

        logger.info(run_res.stdout)
        logger.info(f"Command executed, exit code: {run_res.returncode}.")

        return run_res.returncode

    except subprocess.CalledProcessError as e:
        if expected_error_text in e.stdout:
            logger.info(f"Found expected error text '{expected_error_text}', exit code: 0")
            return 0
        else:
            logger.info(e.stdout)
            logger.info(f"CalledProcessError: {e}, exit code: {e.returncode}")
            return e.returncode
