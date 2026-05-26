from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("sancheck")

except PackageNotFoundError:
    __version__ = "unknown"