"""
Project 1: The Speed Cache -- LRUCache starter.

See the assignment for full phase-by-phase requirements.
Thread-safety (Phase 3) belongs here too -- wrap get/put bodies in a
single threading.Lock. Don't over-engineer with finer-grained locking.
"""

import threading
from typing import Any, Optional

from doubly_linked_list import DoublyLinkedList, Node

_MISSING = object()  # sentinel distinguishing "not found" from a legitimately-stored None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.map = {}
        self.list = DoublyLinkedList()
        # TODO (Phase 3): add a threading.Lock and wrap get/put bodies in it.
        self._lock = threading.Lock()

    def get(self, key: Any) -> Any:
        """
        Return the value for `key` and move it to the most-recently-used
        end, or return the _MISSING sentinel if absent. Both in O(1).
        """
        # TODO
        with self._lock:
            node = self.map.get(key)

            if node is None: 
                return _MISSING

            self.list.move_to_front(node)
            return node.value 
        

    def put(self, key: Any, value: Any) -> None:
        """
        Insert or update `key`, moving it to the most-recently-used end.
        If at capacity, evict the least-recently-used entry BEFORE
        inserting the new one. O(1).
        """
        # TODO
        with self._lock:
            if key in self.map:
                node = self.map[key]
                node.value = value
                self.list.move_to_front(node)
                return 

            if self.capacity <= 0:
                return

            if len(self.map) >= self.capacity:
                lru_node = self.list.least_recently_used()

                if lru_node is not None:
                    self.list.remove(lru_node)
                    del self.map[lru_node.key]

            new_node = Node(key, value)
            self.list.add_to_front(new_node)
            self.map[key] = new_node
