"""Tools for working with dask."""


def update_worker_memory(cluster, new_limit):
    cluster.pod_template.spec.containers[0].resources.limits["memory"] = new_limit
    cluster.pod_template.spec.containers[0].resources.requests["memory"] = new_limit
    if '--memory-limit' in cluster.pod_template.spec.containers[0].args:
        index = cluster.pod_template.spec.containers[0].args.index('--memory-limit')
        cluster.pod_template.spec.containers[0].args[index + 1] = new_limit
    return cluster


def update_worker_cpu(cluster, new_limit):
    cluster.pod_template.spec.containers[0].resources.limits["cpu"] = new_limit
    cluster.pod_template.spec.containers[0].resources.requests["cpu"] = new_limit
    if '--nthreads' in cluster.pod_template.spec.containers[0].args:
        index = cluster.pod_template.spec.containers[0].args.index('--nthreads')
        cluster.pod_template.spec.containers[0].args[index + 1] = new_limit
    return cluster
