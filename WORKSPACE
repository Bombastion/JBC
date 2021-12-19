workspace(name = "JBC")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

_configure_python_based_on_os = """
if [[ "$OSTYPE" == "darwin"* ]]; then
    ./configure --prefix=$(pwd)/bazel_install --with-openssl=$(brew --prefix openssl)
else
    ./configure --prefix=$(pwd)/bazel_install
fi
"""

# Fetch Python and build it from scratch
http_archive(
    name = "python_interpreter",
    build_file_content = """
exports_files(["python_bin"])
filegroup(
    name = "files",
    srcs = glob(["bazel_install/**"], exclude = ["**/* *"]),
    visibility = ["//visibility:public"],
)
""",
    patch_cmds = [
        "mkdir $(pwd)/bazel_install",
        _configure_python_based_on_os,
        "make",
        "make install",
        "ln -s bazel_install/bin/python3 python_bin",
    ],
    sha256 = "06828c04a573c073a4e51c4292a27c1be4ae26621c3edc7cf9318418ce3b6d27",
    strip_prefix = "Python-3.9.9",
    urls = ["https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tar.xz"],
)

# Fetch official Python rules for Bazel
http_archive(
    name = "rules_python",
    sha256 = "b6d46438523a3ec0f3cead544190ee13223a52f6a6765a29eae7b7cc24cc83a0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.1.0/rules_python-0.1.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

# Fetch pip and install our requirements.txt
load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
    name = "py_deps",
    python_interpreter_target = "@python_interpreter//:python_bin",
    requirements = "//:requirements.txt",
)

# Bazel Docker rules
http_archive(
    name = "io_bazel_rules_docker",
    sha256 = "59536e6ae64359b716ba9c46c39183403b01eabfbd57578e84398b4829ca499a",
    strip_prefix = "rules_docker-0.22.0",
    urls = ["https://github.com/bazelbuild/rules_docker/releases/download/v0.22.0/rules_docker-v0.22.0.tar.gz"],
)

load(
    "@io_bazel_rules_docker//repositories:repositories.bzl",
    container_repositories = "repositories",
)

container_repositories()

load("@io_bazel_rules_docker//repositories:deps.bzl", container_deps = "deps")

container_deps()

# Pull a container matching the version of Python we've built above (3.9.9)
load(
    "@io_bazel_rules_docker//container:container.bzl",
    "container_pull",
)

container_pull(
    name = "python3.9.9_slim_buster",
    registry = "docker.io",
    repository = "library/python",
    digest = "sha256:1894f5a820074eef46c09cb88df65279f2b21f4df822032bbec90a83a2dd24b8",  # 3.9.9-slim-buster
)

load(
    "@io_bazel_rules_docker//python3:image.bzl",
    _py_image_repos = "repositories",
)

_py_image_repos()

# These lines must be last
register_toolchains("//:py_3_toolchain")
register_execution_platforms(
    "@local_config_platform//:host",
    "@io_bazel_rules_docker//platforms:local_container_platform",
)
