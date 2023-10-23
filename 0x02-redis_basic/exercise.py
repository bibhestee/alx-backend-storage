#!/usr/bin/env python3
""" Cache using redis basics and python """
import redis
from typing import Union, Any, Callable
import uuid
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
        call_history - store the history of actions on the method
        Arguments:
                method (fn): method to be stored
        Return:
            History (fn)
    """
    @wraps(method)
    def wrapper_call(self, *args, **kwargs):
        """
            wrapper_call - wrapper function
            Arguments:
                    args - tuple of arguments passed to the method
                    kwargs - key-value pair arguments
           Return:
                 Wrapper
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper_call


def count_calls(method: Callable) -> Callable:
    """
        count_calls - count the no of times a method is called
        Arguments:
                method (fn): method to be counted
        Return:
            Counts (fn)
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper_count(self, *args, **kwargs):
        """
            wrapper_count - wrapper function
            Arguments:
                    args - tuple of arguments passed to the method
                    kwargs - key-value pair arguments
           Return:
                 Wrapper
        """
        self._redis.incr(key, amount=1)
        return method(self, *args, **kwargs)
    return wrapper_count


class Cache:
    """
        Cache - cache class
        Methods:
            store: store the data into redis db
        Attributes:
            _redis: redis instance
    """
    def __init__(self):
        """instance initialization"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            Store - generates a rndom key and then uses this key to
                    store the data argument into redis database
            Arguments:
                    data (any): data to be stored
            Return:
                key to the stored data (str - uuid)
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Any:
        """
            get - take a key string argument and an optional Callable
        argument named fn. This callable will be used to convert the data
        back to the desired format.
            Arguments:
                    key (str): key to retrieve data from redis db
                    fn (fn): callable to convert data
            Return:
                The retrieved data (any)
        """
        return fn(self._redis.get(key)) if fn else self._redis.get(key)

    def get_str(self, key: str) -> str:
        """return str"""
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """retrun int"""
        value = self._redis.get(key)
        return int.from_bytes(value)


def replay(fn: Callable):
    """
        replay - display the history of calls of a particular function.
        Arguments:
                fn (fn): the function whom history is to be displayed
        Return:
                replay
    """
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""
        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""
        print("{}(*{}) -> {}".format(func_name, input, output))
