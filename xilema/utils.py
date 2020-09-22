
def listify(inst):
    if isinstance(inst, list):
        return inst
    else:
        return [inst]
