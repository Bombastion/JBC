load("@rules_pkg//:pkg.bzl", "pkg_tar")
load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@py_deps//:requirements.bzl", "requirement")
load("@io_bazel_rules_docker//container:image.bzl", "container_image")
load("@io_bazel_rules_docker//docker/util:run.bzl", "container_run_and_commit")
load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")

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

# Dockerizing the service

# Package requirements.txt into a tar so we can load it into the container
# image.
pkg_tar(
    name = "py_requirements",
    package_dir = "/etc",
    srcs = ["//:requirements.txt"],
    mode = "0644",
    visibility = ["//visibility:private"],
)

# Establish a base image with required symlinks
container_image(
    name = "python3.9.9_base_image",
    base = "@python3.9.9_slim_buster//image",
    tars = [":py_requirements"],
    # slim-buster image places python3 under /usr/local/bin, but the host
    # toolchain used by py3_image might use /usr/bin instead.
    symlinks = {
        "/usr/bin/python": "/usr/local/bin/python",
        "/usr/bin/python3": "/usr/local/bin/python3",
    },
)

# Use pip to install the dependencies inside the container.
container_run_and_commit(
    name = "python3.9.9_base_image_with_deps",
    image = "python3.9.9_base_image.tar",
    commands = [
        "pip3 install --default-timeout=180 -r /etc/requirements.txt",
    ],
)

py3_image(
    name = "jbc_image",
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
