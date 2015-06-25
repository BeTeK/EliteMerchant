#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Created by: python.exe -m py2exe main.py -W setup.py

import datetime
from distutils.core import setup
import py2exe
import site
import os
import os.path
class Target(object):
    '''Target is the baseclass for all executables that are created.
    It defines properties that are shared by all of them.
    '''
    def __init__(self, **kw):
        self.__dict__.update(kw)

        # the VersionInfo resource, uncomment and fill in those items
        # that make sense:
        
        # The 'version' attribute MUST be defined, otherwise no versioninfo will be built:
        # self.version = "1.0"
        
        # self.company_name = "Company Name"
        # self.copyright = "Copyright Company Name © 2013"
        # self.legal_copyright = "Copyright Company Name © 2013"
        # self.legal_trademark = ""
        # self.product_version = "1.0.0.0"
        # self.product_name = "Product Name"

        # self.private_build = "foo"
        # self.special_build = "bar"

    def copy(self):
        return Target(**self.__dict__)

    def __setitem__(self, name, value):
        self.__dict__[name] = value

RT_BITMAP = 2
RT_MANIFEST = 24

# A manifest which specifies the executionlevel
# and windows common-controls library version 6

manifest_template = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="*"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="%(level)s"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="*"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
  </dependency>
</assembly>
'''



main = Target(
    # We can extend or override the VersionInfo of the base class:
    # version = "1.0",
    # file_description = "File Description",
    # comments = "Some Comments",
    # internal_name = "spam",

    script="main.py", # path of the main script

    # Allows to specify the basename of the executable, if different from 'main'
    # dest_base = "main",

    # Icon resources:[(resource_id, path to .ico file), ...]
    icon_resources=[(1, r"img/main.ico")],

    other_resources = [(RT_MANIFEST, 1, (manifest_template % dict(prog="main", level="asInvoker")).encode("utf-8")),
    # for bitmap resources, the first 14 bytes must be skipped when reading the file:
    #                    (RT_BITMAP, 1, open("bitmap.bmp", "rb").read()[14:]),
                      ]
    )


# ``zipfile`` and ``bundle_files`` options explained:
# ===================================================
#
# zipfile is the Python runtime library for your exe/dll-files; it
# contains in a ziparchive the modules needed as compiled bytecode.
#
# If 'zipfile=None' is used, the runtime library is appended to the
# exe/dll-files (which will then grow quite large), otherwise the
# zipfile option should be set to a pathname relative to the exe/dll
# files, and a library-file shared by all executables will be created.
#
# The py2exe runtime *can* use extension module by directly importing
# the from a zip-archive - without the need to unpack them to the file
# system.  The bundle_files option specifies where the extension modules,
# the python dll itself, and other needed dlls are put.
#
# bundle_files == 3:
#     Extension modules, the Python dll and other needed dlls are
#     copied into the directory where the zipfile or the exe/dll files
#     are created, and loaded in the normal way.
#
# bundle_files == 2:
#     Extension modules are put into the library ziparchive and loaded
#     from it directly.
#     The Python dll and any other needed dlls are copied into the
#     directory where the zipfile or the exe/dll files are created,
#     and loaded in the normal way.
#
# bundle_files == 1:
#     Extension modules and the Python dll are put into the zipfile or
#     the exe/dll files, and everything is loaded without unpacking to
#     the file system.  This does not work for some dlls, so use with
#     caution.
#
# bundle_files == 0:
#     Extension modules, the Python dll, and other needed dlls are put
#     into the zipfile or the exe/dll files, and everything is loaded
#     without unpacking to the file system.  This does not work for
#     some dlls, so use with caution.

def findSitePackagesPath(requestedPath):
    for i in site.getsitepackages():
        path = os.path.join(i, requestedPath)
        if os.path.exists(path):
            return path

    raise Exception("cannot find file {0}".format(requestedPath))

print(findSitePackagesPath(os.path.join("requests", "cacert.pem")))

excludes = ["pygame", # disabled soundsystems
            "pyglet"]
includes = ["sip",
            "PyQt5",
            "PyQt5.QtCore",
            "PyQt5.QtGui",
            "PyQt5.QtMultimedia",
            "PyQt5.QtNetwork", # for QtMultimedia
            #"pygame.mixer",
            "requests",
            "requests.adapters",
            "certifi"]
datafiles = [
              ("platforms", [ findSitePackagesPath(os.path.join("PyQt5", "plugins", "platforms", "qwindows.dll")) ]),
              ("imageformats", [ findSitePackagesPath(os.path.join("PyQt5", "plugins", "imageformats", "qico.dll")) ]),
              ("mediaservice", [ # for QtMultimedia
                #findSitePackagesPath(os.path.join("PyQt5", "plugins", "mediaservice", "dsengine.dll")),
                #findSitePackagesPath(os.path.join("PyQt5", "plugins", "mediaservice", "qtmedia_audioengine.dll")),
                findSitePackagesPath(os.path.join("PyQt5", "plugins", "mediaservice", "wmfengine.dll")) # only this required
              ]),
              ("img",[
                r"img\\main.ico",
                r"img\\illegal.png",
                r"img\\power_1.png",
                r"img\\power_2.png",
                r"img\\power_3.png",
                r"img\\power_4.png",
                r"img\\power_5.png",
                r"img\\power_6.png",
                r"img\\power_7.png",
                r"img\\power_8.png",
                r"img\\power_9.png",
                r"img\\power_10.png",
                r"img\\EDAssetsLicense"
              ]),
              ("sounds",[
                r"sounds\\soundcredits.txt",
                r"sounds\\startup.wav",
                r"sounds\\error.wav",
                r"sounds\\error1.wav",
                r"sounds\\error2.wav",
                r"sounds\\search.wav",
                r"sounds\\search1.wav",
                r"sounds\\search2.wav",
                r"sounds\\search3.wav"
              ]),
              ("", [
                findSitePackagesPath(os.path.join("PyQt5", "ssleay32.dll")), # for QtMultimedia
                findSitePackagesPath(os.path.join("PyQt5", "libeay32.dll")), # for QtMultimedia
                r"..\\extraInstallFiles\\MSVCP100.dll",
                r"..\\extraInstallFiles\\MSVCR100.dll",
                r"version.txt"
              ]),
              ("requests", [ findSitePackagesPath(os.path.join("requests", "cacert.pem")) ])
            ]

###############################
# WRITING VERSION STRING
majorversion=0
minorversion=12
builddate=datetime.datetime.now().strftime("%y%m%d")
versionstring=str(majorversion)+'.'+str(minorversion)+'.'+builddate
with open("version.txt", "w") as f:
  f.write(versionstring)


py2exe_options = dict(
    packages = [],
    excludes = excludes,
##    excludes = "tof_specials Tkinter".split(),
##    ignores = "dotblas gnosis.xml.pickle.parsers._cexpat mx.DateTime".split(),
##    dll_excludes = "MSVCP90.dll mswsock.dll powrprof.dll".split(),
    optimize=0,
    compressed=True, # uncompressed may or may not have a faster startup
    bundle_files=3,#1,
    dist_dir='dist',
    includes=includes
    )


# Some options can be overridden by command line options...
setup(name="name",
      # console based executables
      #console=[main],

      # windows subsystem executables (no console)
      windows=[main],
      data_files=datafiles,
      # py2exe options
      zipfile=None,
      options={"py2exe": py2exe_options},
      )

