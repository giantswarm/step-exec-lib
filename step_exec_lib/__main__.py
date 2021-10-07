import os
import logging

from utils.processes import run_and_handle_error

logger = logging.getLogger(__name__)

def main():
    log_format = "%(asctime)s %(name)s %(levelname)s: %(message)s"
    logging.basicConfig(format=log_format)
    logging.getLogger().setLevel(logging.INFO)

    env_vars = os.environ.copy()
    env_vars["ATS_KUBE_CONFIG_PATH"] = "/tmp/kind-kubeconfig"

    # args = ["go", "test", "-v", "-tags=smoke", "/Users/rossf7/src/giantswarm/step-exec-lib/integration/test/metrics"]
    args = ["go", "test", "-v", "-tags=smoke", "examples/apps/hello-world-go/tests/ats/*"]
    ret_res = run_and_handle_error(args, "build constraints exclude all Go files", env=env_vars)

    logger.info(f"Got return code {ret_res}")

if __name__ == "__main__":
    main()
