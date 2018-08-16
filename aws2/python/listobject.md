
paginator = s3_client.get_paginator('list_objects')
operation_parameters = {'Bucket': config.src_bucket,
                        'Prefix': config.prefix,
                        'Marker': pre_init.marker
                        }

page_iterator = paginator.paginate(**operation_parameters)
for page in page_iterator:
   print page['Contents']
