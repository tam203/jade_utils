import os
import subprocess
import base64

terra_work_path = os.path.join('jade-personal-dask', 'terraform','env-dev')
terraform_cmd = '../bin/terraform'

def create_a_cluster(env, num_workers, aws_access_key, aws_secret_key):

    encoded_env = encode_env(env_export(env))

    if not os.path.exists('jade-personal-dask'):
        print("downloading terraform and tools, this may take a minute or two...")
        result = subprocess.run(["git", "clone", "https://github.com/met-office-lab/jade-personal-dask.git"], stdout=subprocess.PIPE)
    if not os.path.exists('jade-personal-dask'):
        raise IOError('Failed to create/clone jade-personal-dask and it doesn\'t exist: %s' % result.stderr)
    subprocess.run([terraform_cmd, 'get'], cwd=terra_work_path)

    return std_out_or_error(
        run_terraform(['apply'], aws_access_key, aws_secret_key, encoded_env, num_workers))


def run_terraform(command_and_args, aws_access_key, aws_secret_key, env, num_workers):
    return subprocess.run(
        [terraform_cmd] + command_and_args + [
            '-var-file=dev.tfvars',
            '-var', 'aws_access_key=%s' % aws_access_key,
            '-var', 'aws_secret_key=%s' % aws_secret_key,
            '-var', 'num_workers=%s' % num_workers,
            '-var', 'conda_env=%s' % env
        ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=terra_work_path
    )

def std_out_or_error(result):
    if result.stderr:
        print(result.stderr.decode())
        raise Exception({'msg':'Failed to successfully complete. State is no unknown',
               'stderr':result.stderr.decode(),
               'stdout':result.stdout.decode(),
               'subprocess_result':result})

    print(result.stdout.decode())
    return result

def destroy_the_cluster(aws_access_key, aws_secret_key):
    return std_out_or_error(
        run_terraform(['destroy', '-force'], aws_access_key, aws_secret_key, 'NONE', 1))



def avaliable_conda_envs():
    envs = subprocess.check_output(['conda', 'env', 'list']).decode().splitlines()
    return [env.split(' ')[0] for env in envs[2:-1]]

def env_export(env):
    avaliable_envs = avaliable_conda_envs()
    if env not in avaliable_envs:
        raise Exception("enviroment '%s' is not in avaliable enviroments: %s" %(env, ', '.join(avaliable_envs)))
    return subprocess.check_output(["conda", "env", "export", "-n", env])

def encode_env(env_yaml):
    return base64.b64encode(env_yaml).decode()
