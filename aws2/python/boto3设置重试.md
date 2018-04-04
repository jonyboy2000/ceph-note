config = Config(connect_timeout=5, retries={'max_attempts': 0})
client = session.client('s3', endpoint_url=url, config=config)
