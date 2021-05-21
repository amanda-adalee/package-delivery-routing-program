class HashMap:

    # This function is the constructor & creates an empty hashmap with # of buckets that parameter passes in : O(n)
    def __init__(self, buckets):
        self.hashmap = []
        for i in range(buckets):
            self.hashmap.append([])

    # This function creates the hash key needed for the hash table : O(1)
    # Returns hashkey
    def create_hashkey_from_id(self, key):
        hashkey = int(key) - 1
        return hashkey

    # This function inserts package values into the hash table using a key : O(1)
    def insert_into_hashtable(self, key, value):
        hash_key = self.create_hashkey_from_id(key)
        hash_pair = [hash_key, value]
        self.hashmap[hash_key] = hash_pair

    # This function deletes a value from the hash table : O(1)
    # Did not use for the project
    # Returns boolean
    def delete_from_hashtable(self, key):
        hash_key = self.create_hashkey_from_id(key)
        if self.hashmap[hash_key] == None:
            return False
        if self.hashmap[hash_key][0] == key:
            self.hashmap[hash_key].pop()
            return True

    # This function looks up buckets in the hash table // for the prompt(user) : O(n)
    # Prints package information for the user.
    def lookup_in_hashtable(self, packageid, single_package):
        hash_key = self.create_hashkey_from_id(packageid)
        found = False
        for bucket in self.hashmap:
            if bucket[0] == hash_key:
                found = True
                temp_package = bucket[1]
                if single_package:
                    package_info = (f'Package #{temp_package.package_id} is {temp_package.delivery_status}. Delivery address is {temp_package.address} '
                        f'{temp_package.city}, {temp_package.state} {temp_package.zip_code}. '
                        f'Package weight is {temp_package.weight}. Delivery deadline is {temp_package.delivery_deadline}.'
                        f' Delivered at {temp_package.delivery_time} AM.\n')
                if not single_package:
                    package_info = (
                        f'Delivery address is {temp_package.address} '
                        f'{temp_package.city}, {temp_package.state} {temp_package.zip_code}. '
                        f'Package weight is {temp_package.weight}. Delivery deadline is {temp_package.delivery_deadline}.')
        if found:
            print(package_info)
        else:
            print(f'Package #{packageid} does not exist.\n')

    # This function retrieves an object from the hash table : O(n)
    # Returns an object stored in the hash table
    def get(self, key):
        hash_key = self.create_hashkey_from_id(key)
        for pair in self.hashmap:
            if pair[0] == hash_key:
                return pair[1]
        return None
