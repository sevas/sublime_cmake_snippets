VERSION_MAJOR = 0
VERSION_MINOR = 2
VERSION_PATCH = 0
VERSION_EXTRA = '-dev'

__version__ = "{0}.{1}.{2}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
__loose_version__ = "{0}.{1}".format(VERSION_MAJOR, VERSION_MINOR)

if VERSION_EXTRA:
    __version__ = "{0}{1}".format(__version__, VERSION_EXTRA)
    __version_info__ = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH, float('inf'))
else:
    __version_info__ = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)


__all__ = ['__version__', '__version_info__', '__loose_version__']
