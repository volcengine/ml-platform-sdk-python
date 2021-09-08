from socket import gethostbyname

DOMAIN = "tos-s3-cn-beijing.ivolces.com"


def _is_volce_intranet():
    for i in range(3):
        try:
            ips = gethostbyname(DOMAIN)
            if ips and len(ips) > 0:
                return True
            else:
                return False
        except Exception:
            pass
        return False


IS_VOLCE_INTRANET = _is_volce_intranet()


def get_tos_endpoint(region):
    if IS_VOLCE_INTRANET:
        return f"http://tos-s3-{region}.ivolces.com"
    else:
        return f"http://tos-s3-{region}.volces.com"
