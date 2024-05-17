import redis
import configparser
from logger import Logger

class RedisUploader:
    def __init__(self, config_file='D:\\Apeksha\\APRIL\\14-05-24\\Teltonika_socket_pgm\\src\\config.ini'):
        self.logging = Logger()
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.redis_host = self.config.get('Redis', 'host')
        self.redis_port = self.config.getint('Redis', 'port')
        self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=0, decode_responses=True)

    def upload_record(self,redis_key, record):
        if not self.redis_client:
            raise RuntimeError("Redis client not connected. Call connect_to_redis() first.")
        try:
            self.redis_client.rpush(redis_key, record)
        except Exception as e:
            self.logging.log("redis_error", f"Error uploading record to Redis: {e}")  


if __name__ == "__main__":
    # Define your test records (replace this with your dynamic data source)
    test_records = "00000000000000f98e020000018f75d79dc0012e3cbf9e07bec469039100c1070000004e0014000700ef0100f00100150500450100010100ca0000cc00000900b5002900b6001f004229650018000000431019004400000009010400c9000000cb0000000300f100009dfd00c700005a15001000010fa20001004e000000000000000000000000018f75d79208012e3cc0fb07bec7dc039400af070000004e0014000700ef0100f00100150500450100010100ca0000cc00000900b5002900b6001f0042298f001800000043101a004400000009010400c9000000cb0000000300f100009dfd00c700005a15001000010fa20001004e0115a4230035008b000002000074a4"
    redis_key = "TestTeltonikaRawData"
    # Create an instance of RedisUploader, reading redis_key from the config
    redis_uploader = RedisUploader()

    for _ in range(1):
        redis_uploader.upload_record(redis_key, test_records)
    