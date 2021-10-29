load("@rules_python//python:defs.bzl", "py_binary")
load("@py_deps//:requirements.bzl", "requirement")

py_binary(
    name = "exercise_models",
    srcs = ["exercise_models.py"],
    deps = [
        "//db/model:models",
        "//db/model:handler"
    ],
)