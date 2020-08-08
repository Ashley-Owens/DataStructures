# Course: CS261 - Data Structures
# Assignment 5
# Student: Ashley Owens
# Description: Uses a DA to implement a hash table data structure. 
# Performs collsion resolution using chaining via a singly linked list.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the contents of the hash map by replacing it with a new one.
        """
        new = HashMap(self.capacity, self.hash_function)
        self.buckets = new.buckets
        self.size = new.size

    def get(self, key: str) -> object:
        """
        Args:
            key (str): given key
        Returns:
            object: the value associated with the given key or None
        """
        # Obtains the LL object and node associated with the given key.
        linkedlst, node = self.get_node(key)
        
        if not node:
            return None

        return node.value

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If a given key already exists, 
        its value is replaced with the new value. Otherwise, a key/value pair is added.
        Args:
            key (str): key
            value (object): value
        """
        # Obtains the LL object and node associated with the given key.
        linkedlst, node = self.get_node(key)

        if not node:
            linkedlst.insert(key, value)
            self.size += 1

        # If key is already present in the hash map, updates its value.
        else:
            node.value = value

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If key is not present, no operations is performed.
        Args:
            key (str): given key
        """
        # Obtains the LL object and node associated with the given key.
        linkedlst, node = self.get_node(key)
        
        if not node:
            return 
        
        # Removes the key: value pair from the linked list.
        linkedlst.remove(key)
        self.size -= 1
    
    def get_node(self, key: str) -> object:
        """
        Gets the Linked List and node associated with the given key.
        Args:
            key (str): node.key
        Returns:
            tuple: Linked List and node objects
        """
        # Determines the associated DA index for the given key.
        hash_index = self.hash_function(key) % self.capacity

        # Obtains the current object at the DA hash_index.
        linkedlst = self.buckets.get_at_index(hash_index)

        # Determines if the key exists in the Linked List object.
        node = linkedlst.contains(key)

        return linkedlst, node

    def contains_key(self, key: str) -> bool:
        """
        Args:
            key (str): given key being searched for
        Returns:
            bool: True if present, else False
        """
        # Obtains the LL object and node associated with the given key.
        linkedlst, node = self.get_node(key)
        
        if not node:
            return False

        return node.key == key

    def empty_buckets(self) -> int:
        """
        Returns:
            int: the number of empty buckets in the hash table. 
        """
        count = 0

        # Accesses each Linked List object in the array.
        for i in range(self.capacity):
            linkedlst = self.buckets.get_at_index(i)

            # If the list is empty, increments bucket counter.
            if linkedlst.length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        Returns:
            float: average number of elements in each bucket.
        """
        return (self.size / self.capacity)

    def resize_table(self, new_capacity: int) -> None:
        """
        Creates a new hash map congruous to the new capacity size. All existing
        key: value pairs are rehashed and placed accordingly in the new hash table.
        Args:
            new_capacity (int): desired capacity of the new hash map
        """
        # Performs no operations for capacity input error.
        if new_capacity < 1:
            return 

        # Creates a new hash map according to new capacity.
        self.new = HashMap(new_capacity, self.hash_function)
        
        # Obtains all the keys located in the current hash map.
        keys = self.get_keys()
        
        # Iterates through the keys, rehashing and placing them in the new hashmap.
        for i in range(keys.length()):
            key = keys.get_at_index(i)
            prev_lst, node = self.get_node(key)
            hash_index = self.new.hash_function(key) % self.new.capacity
            linkedlst = self.new.buckets.get_at_index(hash_index)
            linkedlst.insert(node.key, node.value)
            self.new.size += 1
        
        # Updates the old hash map to the new one.
        self.buckets = self.new.buckets
        self.capacity = self.new.capacity
        self.size = self.new.size

    def get_keys(self) -> DynamicArray:
        """
        Obtains every key stored in the current hash map.
        Returns:
            DynamicArray: contains all current keys
        """
        # Initializes a DA object
        keys = DynamicArray()

        # Iterates through the hash map, adding each key to the DA.
        for i in range(self.buckets.length()):
            linkedlst = self.buckets.get_at_index(i)
            for node in linkedlst:
                keys.append(node.key)

        return keys




# BASIC TESTING
if __name__ == "__main__":
    pass

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.size, m.capacity)


    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)


    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())


    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(m.table_load(), m.size, m.capacity)

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(100, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)


    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.size, m.capacity)
    # m.resize_table(100)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)


    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    # # m.put('str' + str(0), 1)

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(40, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(10, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))


    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)


    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(30, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))


    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.size, m.capacity)
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(50, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # print(m.remove('key4'))


    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(20, hash_function_1)
    # m.put('key1', 10)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    # # print(m)
    # m.resize_table(30)
    # print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    # print(m)


    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)

    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')

    #     for key in keys:
    #         result &= m.contains_key(str(key))
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    # print("\nPDF - get_keys example 1")
    # print("------------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(100, 200, 10):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys())
    # print(m)

    # m.resize_table(1)
    # print(m.get_keys())
    # print(m)

    # m.put('200', '2000')
    # m.remove('100')
    # m.resize_table(2)
    # print(m.get_keys())
    # print(m)


    
   

