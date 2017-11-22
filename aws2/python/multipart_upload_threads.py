import logging
import math
import mimetypes
from multiprocessing import Pool
import os
import boto

from boto.s3.connection import S3Connection
from filechunkio import FileChunkIO


def _upload_part(bucketname, aws_key, aws_secret, multipart_id, part_num,
    source_path, offset, bytes, amount_of_retries=10):
    """
    Uploads a part with retries.
    """
    def _upload(retries_left=amount_of_retries):
        try:
            logging.info('Start uploading part #%d ...' % part_num)
            conn = boto.connect_s3(
                aws_key,
                aws_secret,
                host='10.254.9.36',
                is_secure=False,
                port=7480,
                calling_format=boto.s3.connection.OrdinaryCallingFormat(),
            )
            bucket = conn.get_bucket(bucketname)
            for mp in bucket.get_all_multipart_uploads():
                if mp.id == multipart_id:
                    with FileChunkIO(source_path, 'r', offset=offset,
                        bytes=bytes) as fp:
                        mp.upload_part_from_file(fp=fp, part_num=part_num)
                    break
        except Exception, exc:
            if retries_left:
                _upload(retries_left=retries_left - 1)
            else:
                logging.info('... Failed uploading part #%d' % part_num)
                raise exc
        else:
            logging.info('... Uploaded part #%d' % part_num)

    _upload()


def upload(bucketname, aws_key, aws_secret, source_path, keyname,
    acl='private', headers={}, guess_mimetype=True, parallel_processes=8):
    """
    Parallel multipart upload.
    """
    conn = boto.connect_s3(
        aws_key,
        aws_secret,
        host='10.254.9.36',
        is_secure=False,
        port=7480,
        calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )
    bucket = conn.get_bucket(bucketname)

    if guess_mimetype:
        mtype = mimetypes.guess_type(keyname)[0] or 'application/octet-stream'
        headers.update({'Content-Type': mtype})

    mp = bucket.initiate_multipart_upload(keyname, headers=headers)

    source_size = os.stat(source_path).st_size
    bytes_per_chunk = max(int(math.sqrt(5242880) * math.sqrt(source_size)),
        5242880)
    chunk_amount = int(math.ceil(source_size / float(bytes_per_chunk)))

    pool = Pool(processes=parallel_processes)
    for i in range(chunk_amount):
        offset = i * bytes_per_chunk
        remaining_bytes = source_size - offset
        bytes = min([bytes_per_chunk, remaining_bytes])
        part_num = i + 1
        pool.apply_async(_upload_part, [bucketname, aws_key, aws_secret, mp.id,
            part_num, source_path, offset, bytes])
    pool.close()
    pool.join()

    if len(mp.get_all_parts()) == chunk_amount:
        mp.complete_upload()
        key = bucket.get_key(keyname)
        key.set_acl(acl)
    else:
        mp.cancel_upload()

if __name__ == '__main__':
    #fallocate -l 500M test.img
    upload('test','cosbench','cosbench','/root/test.img','test.img')
