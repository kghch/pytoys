#!/usr/bin/python
#-*- coding: utf-8 -*-

import time
import collections

class LRUCache(collections.MutableMapping):

	def __init__(self, timeout=60):
		self._timeout = timeout
		self._time2keys = collections.defaultdict(list)
		self._key2time = {}
		self._last_visited_time = collections.deque()
		self._store = {}


	def __getitem__(self, key):
		t = time.time()
		self._last_visited_time.append(t)
		self._key2time[key] = t
		self._time2keys[t].append(key)

		return self._store[key]


	def __setitem__(self, key, value):
		t = time.time()
		self._last_visited_time.append(t)
		self._key2time[key] = t
		self._time2keys[t].append(key)
		self._store[key] = value


	def __delitem__(self, key):
		del self._store[key]
		del self._key2time[key]


	def __iter__(self):
		pass

	def __len__(self):
		pass

	def sweep(self):
		now = time.time()

		while len(self._last_visited_time) > 0:
			ltime = self._last_visited_time[0]

			if now - ltime < self._timeout:
				break

			for key in self._time2keys[ltime]:
				self._last_visited_time.popleft()

				if key in self._store:
					if now - self._key2time[key] > self._timeout:

						del self._store[key]
						del self._key2time[key]

			del self._time2keys[ltime]

def test():
	cache = LRUCache(timeout=0.3)

	cache['key1'] = 'v1'
	cache['key2'] = 'v2'

	time.sleep(0.2)
	cache.sweep()
	assert 'key1' in cache

	time.sleep(0.2)
	cache.sweep()
	assert 'key2' not in cache


test()