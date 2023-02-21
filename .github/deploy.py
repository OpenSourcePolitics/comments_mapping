import os
import json
import time


def container_id():
    container_name = os.environ['CONTAINER_NAME']
    container_json = os.popen('scw container container list -o json').read()
    container_json = json.loads(container_json)
    return [container['id'] for container in container_json if container['name'] == container_name][0]


def container_status(id):
    status = os.popen(f'scw container container get {id} -o json').read()
    status_json = json.loads(status)
    return status_json['status']


container_id = container_id()

print('Deploying container ...')
os.popen(f'scw container container deploy {container_id}')
print('Deployed container, waiting for it to be ready ...')
time.sleep(5)

retry_count = 12

while retry_count >= 0:
    if container_status(container_id) == 'ready':
        print('Deployed successfully')
        exit(0)
    else:
        print(f'Container is not ready, current status is {container_status(container_id)}')
        print(f'Retrying in 10 seconds, {retry_count} retries left')
        time.sleep(10)
        retry_count -= 1

print('Container is not ready after 2 minutes, exiting')
exit(1)
