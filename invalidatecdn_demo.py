import boto3
import time
import sys


""" Invalidate CDN at s3://static/demo/src """
DISTRIBUTION_ID = 'A1AA1AA11A11AA'

client = boto3.client('cloudfront')


def create_invalidation():
    res = client.create_invalidation(
        DistributionId=DISTRIBUTION_ID,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': [
                    '/demo/src/*'
                ]
            },
            'CallerReference': str(time.time()).replace(".", "")
        }
    )
    invalidation_id = res['Invalidation']['Id']
    return invalidation_id


def get_invalidation_status(inval_id):
    res = client.get_invalidation(
        DistributionId=DISTRIBUTION_ID,
        Id=inval_id
    )
    return res['Invalidation']['Status']


def run():
    the_id = create_invalidation()
    count = 0
    while True:
        status = get_invalidation_status(the_id)
        if status == 'Completed':
            print("Completed, id: {}".format(the_id))
            break
        elif count < 10:
            count += 1
            time.sleep(30)
        else:
            print("Timeout, please check CDN")
            sys.exit(1)


if __name__ == '__main__':
    run()
