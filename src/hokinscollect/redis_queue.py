import redis
import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(
    os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
)
from constantstore import constant


class RedisQueue(object):
    def __init__(self, name):
        self.key = name
        self.max_size: int = 100000
        self.rq: redis.Redis = redis.Redis(
            host=constant.REDIS_IP, port=constant.REDIS_PORT, db=0, decode_responses=True
        )

    def __len__(self) -> int:
        return self.rq.llen(self.key)

    def __iter__(self):
        while self.size() > 0:
            yield self.rq.get()

    def size(self) -> int:  # 큐 크기 확인
        return self.rq.llen(self.key)

    def is_empty(self) -> bool:  # 비어있는 큐인지 확인
        return self.size() == 0

    def put(self, element) -> int:  # 데이터 넣기
        return self.rq.lpush(self.key, element)  # left push

    def put_and_trim(self, element) -> int:  # 데이터 넣기
        queue_count: int = self.rq.lpush(self.key, element)  # left push
        self.rq.ltrim(self.key, 0, self.max_size - 1)  # 최대크기를 초과한 경우 자르기
        return queue_count

    def get(self, is_blocking=False, timeout=None) -> str:  # 데이터 꺼내기
        if is_blocking:
            element: tuple = self.rq.brpop(self.key, timeout=timeout)  # blocking right pop
            element: str = element[1]  # key[0], value[1]
        else:
            element: str = self.rq.rpop(self.key)  # right pop
        return element

    def get_without_pop(self) -> str:  # 꺼낼 데이터 조회
        if self.is_empty():
            return None
        element: str = self.rq.lindex(self.key, -1)
        return element

    def get_without_all(self) -> list:
        if self.is_empty():
            return None
        return [self.rq.lindex(self.key, i) for i in range(self.size())]


StartQueue: RedisQueue = RedisQueue(constant.REDISTARTQUEUENAME)
WaitingQueue: RedisQueue = RedisQueue(constant.REDISJOBQUEUENAME)
ProceedingQueue: RedisQueue = RedisQueue(constant.REDISPROCEEDINGQUEUENAME)
