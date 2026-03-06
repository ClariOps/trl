def cpu_to_millicores(cpu):
    if cpu is None:
        return None

    if cpu.endswith("m"):
        return int(cpu.replace("m", ""))

    return int(float(cpu) * 1000)


def memory_to_mi(mem):
    if mem is None:
        return None

    if mem.endswith("Mi"):
        return int(mem.replace("Mi", ""))

    if mem.endswith("Gi"):
        return int(mem.replace("Gi", "")) * 1024

    return None