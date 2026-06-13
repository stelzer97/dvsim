# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

"""EDA tool plugin providing ModelSim/Questa support to DVSim."""

import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from dvsim.job.data import JobSpec
from dvsim.sim.data import CoverageMetrics

if TYPE_CHECKING:
    from dvsim.job.deploy import Deploy

__all__ = ("Modelsim",)


class Modelsim:
    """Implement ModelSim/Questa tool support."""

    @staticmethod
    def get_cov_summary_table(cov_report_path: Path) -> tuple[Sequence[Sequence[str]], str]:
        """Get a coverage summary."""
        msg = f"Coverage data not found in {cov_report_path}!"
        raise RuntimeError(msg)

    @staticmethod
    def get_job_runtime(_job: JobSpec, log_text: Sequence[str]) -> tuple[float, str]:
        """Return the job runtime (wall clock time) along with its units."""
        # ModelSim prints: "# End time: 12:08:10 on Jun 13,2026, Elapsed time: 0:00:04"
        pattern = r"#\s*End time:.*Elapsed time:\s*(\d+):(\d+):(\d+)"
        for line in reversed(log_text):
            if m := re.search(pattern, line):
                t = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
                return float(t), "s"

        msg = "Job runtime not found in the log."
        raise RuntimeError(msg)

    @staticmethod
    def get_simulated_time(_job: JobSpec, log_text: Sequence[str]) -> tuple[float, str]:
        """Return the simulated time along with its units."""
        # ModelSim prints: "#    Time: 130430 ns  Iteration: 1  Instance: ..."
        pattern = r"#\s+Time:\s*(\d+\.?\d*)\s*(\w+)\s+Iteration:"
        for line in reversed(log_text):
            if m := re.search(pattern, line):
                return float(m.group(1)), m.group(2).lower()

        # Fallback: "# ** Note: $finish    : 1000 ns"
        pattern = r"\$finish\s*:\s*(\d+\.?\d*)\s*(\w+)"
        for line in reversed(log_text):
            if m := re.search(pattern, line):
                return float(m.group(1)), m.group(2).lower()

        msg = "Simulated time not found in the log."
        raise RuntimeError(msg)

    @staticmethod
    def get_coverage_metrics(raw_metrics: Mapping[str, float | None] | None) -> CoverageMetrics:
        """Get a CoverageMetrics model from raw coverage data."""
        return CoverageMetrics(code=None, assertion=None, functional=None)

    @staticmethod
    def set_additional_attrs(deploy: "Deploy") -> None:
        """Define any additional tool-specific attrs on the deploy object."""