from typing import Any, Dict, List, Tuple, cast

import configargparse
import pytest

from step_exec_lib.errors import ValidationError, Error
from step_exec_lib.steps import Runner, BuildStep
from step_exec_lib.types import STEP_ALL, StepType
from tests.dummy_build_step import (
    DummyBuildStep,
    DummyTwoStepBuildFilteringPipeline,
    STEP_DUMMY1,
    STEP_DUMMY2,
    STEP_DUMMY3,
    get_test_config_parser,
)


class TestBuildStep:
    def test_is_abstract(self) -> None:
        with pytest.raises(TypeError):
            BuildStep()  # type: ignore

    def test_name(self) -> None:
        bs = DummyBuildStep("bs1")
        assert bs.name == "DummyBuildStep"

    def test_raises_own_exception_when_binary_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        fake_bin = "fake.bin"

        def check_bin(name: str) -> None:
            assert name == fake_bin
            return None

        monkeypatch.setattr("shutil.which", check_bin)
        bs = DummyBuildStep("s1")
        with pytest.raises(ValidationError):
            bs._assert_binary_present_in_path(fake_bin)

    def test_validates_version_ok(self) -> None:
        bs = DummyBuildStep("bs1")
        bs._assert_version_in_range("test", "v0.2.0", "0.2.0", "0.3.0")
        bs._assert_version_in_range("test", "0.2.0", "0.2.0", "0.3.0")
        bs._assert_version_in_range("test", "v0.2.100", "0.2.0", "0.3.0")
        with pytest.raises(ValidationError):
            bs._assert_version_in_range("test", "v0.3.0", "0.2.0", "0.3.0")
        with pytest.raises(ValidationError):
            bs._assert_version_in_range("test", "v0.1.0", "0.2.0", "0.3.0")


class TestBuildPipeline:
    def test_combines_step_types_ok(self) -> None:
        bsp = DummyTwoStepBuildFilteringPipeline()
        assert bsp.steps_provided == {STEP_DUMMY1, STEP_DUMMY2, STEP_DUMMY3}

    @pytest.mark.parametrize(
        "set_of_requested_tags, set_of_requested_skips, expected_run_counters",
        [
            # STEP_ALL should run all build steps
            ([STEP_ALL], [], ([1, 1, 1, 1], [1, 1, 1, 1])),
            # STEP_DUMMY1 should run only 1st BuildStep, but 'configure' needs to run for both still
            ([STEP_DUMMY1], [], ([1, 1, 1, 1], [1, 0, 0, 0])),
            # STEPS_DUMMY3 should run only 2nd BuildStep, but 'configure' needs to run for both still
            ([STEP_DUMMY3], [], ([1, 0, 0, 0], [1, 1, 1, 1])),
            # this should run all except the ones including STEP_DUMMY1 (1st one)
            ([STEP_ALL], [STEP_DUMMY1], ([1, 0, 0, 0], [1, 1, 1, 1])),
            # this should run all except the ones including STEP_DUMMY3 (2nd one)
            ([STEP_ALL], [STEP_DUMMY3], ([1, 1, 1, 1], [1, 0, 0, 0])),
        ],
    )
    def test_runs_steps_ok(
        self,
        set_of_requested_tags: List[StepType],
        set_of_requested_skips: List[StepType],
        expected_run_counters: Tuple[List[int], List[int]],
    ) -> None:
        bsp = DummyTwoStepBuildFilteringPipeline()
        config_parser = get_test_config_parser()
        bsp.initialize_config(config_parser)
        config = config_parser.parse_known_args()[0]
        config.steps = list(set_of_requested_tags)
        config.skip_steps = list(set_of_requested_skips)
        context: Dict[str, Any] = {}
        bsp.pre_run(config)
        bsp.run(config, context)
        bsp.cleanup(config, context, False)

        bsp.step1.assert_run_counters(*expected_run_counters[0])
        bsp.step2.assert_run_counters(*expected_run_counters[1])

    def test_runs_with_exception(self) -> None:
        bsp = DummyTwoStepBuildFilteringPipeline(fail_in_pre=True)
        config_parser = get_test_config_parser()
        bsp.initialize_config(config_parser)
        config = config_parser.parse_known_args()[0]
        with pytest.raises(Error):
            bsp.pre_run(config)

        # this fails in pre_run
        bsp.step1.assert_run_counters(1, 1, 0, 0)
        # since step above fails, this won't have even pre_run ran
        bsp.step2.assert_run_counters(1, 0, 0, 0)


class TestRunner:
    def test_single_step(self) -> None:
        test_step = DummyBuildStep("t1")
        runner = Runner(cast(configargparse.Namespace, None), [test_step])
        runner.run()

        test_step.assert_run_counters(0, 1, 1, 1)
        assert runner.context["test"] == 1

    def test_exits_on_failed_pre_run(self) -> None:
        test_step = DummyBuildStep("t1", fail_in_pre=True)
        runner = Runner(cast(configargparse.Namespace, None), [test_step])
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            runner.run()
        assert pytest_wrapped_e.typename == "SystemExit"
        assert pytest_wrapped_e.value.code == 1
        test_step.assert_run_counters(0, 1, 0, 0)

    def test_breaks_build_on_failed_run(self) -> None:
        test_step1 = DummyBuildStep("t1", fail_in_run=True, fail_in_cleanup=True)
        test_step2 = DummyBuildStep("t2")
        runner = Runner(cast(configargparse.Namespace, None), [test_step1, test_step2])

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            runner.run()

        # if the first build step failed, second one should be not executed
        # but cleanup should still run for both steps, even if cleanup in the 1st one fails
        test_step1.assert_run_counters(0, 1, 1, 1)
        test_step2.assert_run_counters(0, 1, 0, 1)
        assert test_step1.cleanup_informed_about_failure
        assert test_step2.cleanup_informed_about_failure
        assert pytest_wrapped_e.typename == "SystemExit"
        assert pytest_wrapped_e.value.code == 1
