# The unified Parity CI image (Debian 12 / bookworm)

[![Docker Pulls](https://img.shields.io/docker/pulls/paritytech/ci-unified-bookworm)](https://hub.docker.com/r/paritytech/ci-unified-bookworm/tags)

This is the Debian 12 (`bookworm`) revision of [`ci-unified`](../ci-unified/README.md), added because
Debian 11 (`bullseye`) reached end of life on 2026-08-31 and its `bullseye-security` apt suite is no
longer refreshed.

Both images are built and published in parallel for the time being:

| Image | Base | Status |
| --- | --- | --- |
| `paritytech/ci-unified` | Debian 11 `bullseye` | maintained for now, EOL base |
| `paritytech/ci-unified-bookworm` | Debian 12 `bookworm` | migrate here |

### Specification

Same contents as `ci-unified`, on a newer base:

* Rust stable 1.93.0
* Rust nightly 2026-01-27
* LLVM 15 (unchanged, from `apt.llvm.org/bookworm`)
* Python 3.11.2 (was 3.9.2)
* Ruby 3.1 (was 2.7.4)
* Plenty of different utilities required in the CI pipelines

### Migration notes

Beyond the newer package versions, these differences can affect existing jobs:

* **`pip install` into the system interpreter no longer works.** Debian 12 marks the system Python as
  externally managed (PEP 668), so `pip install <pkg>` fails with
  `error: externally-managed-environment`. Jobs that install Python packages need a virtualenv.
* **`yq` now comes from apt instead of pip**, so it is 3.1.0 rather than PyPI's 4.x. Same upstream
  ([kislyuk/yq](https://github.com/kislyuk/yq)) and `yq`/`tomlq` work as before, but the XML wrapper is
  installed as **`xq-python`**, not `xq`.
* **glibc 2.36** (was 2.31) and **OpenSSL 3.x** (was 1.1.1). Binaries built in this image will not run
  on hosts with an older glibc.
* **Ruby 3.1** is a major bump from 2.7 and can break Gemfiles that were pinned for 2.7.

### Tags

Same pattern as `ci-unified`:

```
<DISTRO_CODENAME>[ -<RUST_STABLE_VERSION> | -<RUST_STABLE_VERSION-RUST_NIGHTLY_VERSION> ][ -v<DATESTAMP> ]
```

For example:

* `paritytech/ci-unified-bookworm:bookworm-1.93.0`
* `paritytech/ci-unified-bookworm:bookworm-1.93.0-v202601271200`
* `paritytech/ci-unified-bookworm:bookworm-1.93.0-2026-01-27`
* `paritytech/ci-unified-bookworm:bookworm-1.93.0-2026-01-27-v202601271200`

Available tags: https://hub.docker.com/r/paritytech/ci-unified-bookworm/tags

#### The `latest` tag

As with `ci-unified`, `latest` is an alias for the newest available tag combination, so using it means
following the upstream in rolling-release style and accepting possible breaking changes.
