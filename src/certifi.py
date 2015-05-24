import os

def where():
    path = os.path.join("requests", "cacert.pem")

    try:
        import site
        def findSitePackagesPath(requestedPath):
            for i in site.getsitepackages():
                path = os.path.join(i, requestedPath)
                if os.path.exists(path):
                    return path

            return None

        pathTmp = findSitePackagesPath(os.path.join("requests", "cacert.pem"))
        if pathTmp is not None:
            path = pathTmp

    except ImportError:
        pass

    return path