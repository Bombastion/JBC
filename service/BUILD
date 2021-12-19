load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")
load("@py_deps//:requirements.bzl", "requirement")

filegroup(
    name = "templates",
    srcs = glob(["templates/*"]),
)

filegroup(
    name = "javascript",
    srcs = glob(["static/scripts/*"]),
)

filegroup(
    name = "styles",
    srcs = glob(["static/styles/*"]),
)

py3_image(
    name = "jbc_service",
    srcs = ["flask_service.py"],
    main = "flask_service.py",
    data = [
        ":javascript",
        ":styles",
        ":templates",
    ],
    deps = [
        "//db/model:models",
        "//db/model:handler",
        requirement("Flask"),
        requirement("Flask-Login"),
    ],
)

py_binary(
    name = "flask_service",
    srcs = ["flask_service.py"],
    main = "flask_service.py",
    data = [
        ":javascript",
        ":styles",
        ":templates",
    ],
    deps = [
        "//db/model:models",
        "//db/model:handler",
        requirement("Flask"),
        requirement("Flask-Login"),
    ],
)
