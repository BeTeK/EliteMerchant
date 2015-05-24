import os
certPath = None
def where():
    global certPath
    if certPath is None:
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

        if not os.path.exists(path):
            path = os.path.join("cacert.pem")

        certPath = path

    return certPath