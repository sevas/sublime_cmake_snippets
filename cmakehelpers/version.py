VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 3
VERSION_EXTRA = '-dev'

__version__ = "{}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
__loose_version__ = "{}.{}".format(VERSION_MAJOR, VERSION_MINOR)

if VERSION_EXTRA:
    __version__ = "{}{}".format(__version__, VERSION_EXTRA)
    __version_info__ = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH, float('inf'))
else:
    __version_info__ = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)


__all__ = ['__version__', '__version_info__', '__loose_version__']