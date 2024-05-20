# RBNS Downloader

`rbns-downloader` is a Python package designed to facilitate the downloading of RNA Bind-n-Seq (RBNS) experimental data. This package provides command-line tools to download and list RBNS data efficiently.

## Features

- Download specific RBNS experiments or all available experiments.
- List available files from specific RBNS experiments or all available experiments.
- Configurable output directory and verbosity for progress display.

## Installation

You can install the `rbns-downloader` package using `pip`:

```bash
pip install git+https://github.com/Ferny730JR/rbns_downloader.git
```

## Requirements

- Python 3.6 or higher
- `requests`
- `jellyfish`
- `clint`

These dependencies are automatically installed when you install the package via `pip`.

## Usage

After installing the package, you can use the `rbns` command-line tool.

### Downloading Experiments

To download a specific experiment:

```bash
rbns download <target>
```

To download all available experiments:

```bash
rbns download all
```

### Listing Experiments

To list files from a specific experiment:

```bash
rbns list <target>
```

To list files from all available experiments:

```bash
rbns list all
```

### Additional Options

- Specify the output directory for saving RBNS data using `-o` or `--output`:
  ```bash
  rbns download <target> -o /path/to/output_directory
  ```

- Enable verbose mode to show download progress using `-v` or `--verbose`:
  ```bash
  rbns download <target> -v
  ```

## Example Commands

- Download a specific experiment with verbose output:
  ```bash
  rbns download RBFOX2 -v
  ```

- List all available experiments:
  ```bash
  rbns list all
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
