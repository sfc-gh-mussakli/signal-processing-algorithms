"""Build script for project installation."""

import platform
import os
import shutil

from pathlib import Path


from setuptools import Extension, Distribution
from setuptools.command.build_ext import build_ext


ext_modules = [
    Extension(
        "signal_processing_algorithms.energy_statistics._e_divisive",
        sources=["./src/signal_processing_algorithms/energy_statistics/e_divisive.c"],
        extra_compile_args=["-O3"] if "Darwin" in platform.system() else ["-O3", "-std=c99", "-c"],
        extra_link_args=[] if "Darwin" in platform.system() else ["-shared"],
        optional=True,
    )
]


def build() -> None:
    """Build the extensions."""
    distribution = Distribution({"name": "package", "ext_modules": ext_modules})
    cmd = build_ext(distribution)
    cmd.ensure_finalized()
    cmd.run()

    for output in cmd.get_outputs():
        output = Path(output)
        relative_extension = Path("src") / output.relative_to(cmd.build_lib)

        shutil.copyfile(output, relative_extension)
        print(relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)


if __name__ == "__main__":
    build()
