![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/cezkc6dw967dsqlizgfe.jpg)

- This post describe how to remove files from CloudFront edge caches before it expires using python boto3

- To invalidate files, specify either the path for individual files or a path that ends with the * wildcard, which might apply to one file or to many, as shown in the following examples:
 - `/images/image1.jpg`
 - `/images/image*`
 - `/images/*`
 
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/9p29dpj6f30o0k646a9d.png)
- Using python boto3 [invalidatecdn_demo.py](https://github.com/vumdao/invalidate-cdn/blob/master/invalidatecdn_demo.py)
```
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

```

- Run
```
~()⚡ $ python invalidatecdn_demo.py 
Completed, id: I1CLODB5ZXEQUK
```

- Result
 - In progress
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/b0f6fgc459dkvc1741hh.png)

 - Complete
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/f62t39vkyjr1opqhnoxt.png)

- Ref: https://dev.to/vumdao/invalidation-aws-cdn-using-boto3-2k9g
