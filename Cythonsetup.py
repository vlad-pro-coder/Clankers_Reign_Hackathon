from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy
import os

build_dir = "build"
os.makedirs(build_dir, exist_ok=True)

ext_modules = [
    Extension(
        name="RaspGSCamera",
        sources=["./Drivers/RaspGSCamera.pyx"],
        include_dirs=[numpy.get_include()]  # <-- THIS is critical
    ),
    Extension(
        name="SmoothBno085",
        sources=["./Drivers/SmoothBno085.pyx"],
        include_dirs=[numpy.get_include()]  # <-- THIS is critical
    ),
    Extension(
        name="ClientPhotoSender",
        sources=["./Drivers/ClientPhotoSender.pyx"],
        include_dirs=[numpy.get_include()]  # <-- THIS is critical
    )

]

setup(
    name="RaspGSCamera",
    ext_modules=cythonize(
        ext_modules,
        compiler_directives={'language_level': "3"}
    ),
    script_args=["build_ext", "--build-lib", build_dir, "--build-temp", build_dir]
)
