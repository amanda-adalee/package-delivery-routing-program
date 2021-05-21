import csv

# This function loops through all the rows in csv file & and converts miles to floats : O(N^2)
# Then adds info to a hash table, key = address & values = miles
# Returns the distance hash table.
def hashtable(table):
    hashmap = []
    bucket = 0
    for row in table:
        col = 0
        hashmap.append([])
        address = row[1].strip()
        # Sets a list of all the miles in a row
        miles_in_row = list(row[2:])

        # Loops through the list created and sets those values to a float instead of string
        for mile in miles_in_row: # O(N)
            miles_in_row[col] = float(mile)
            col += 1
        # Adds info into a hash table bucket
        hash_key = address
        hash_pair = [hash_key, miles_in_row]
        hashmap[bucket] = hash_pair
        bucket += 1

    return hashmap

# This function takes the key parameter and searches through the hashmap to find the values. : O(n)
def find_address_in_hashmap(key):
    hashmap = open_csv()
    found = False
    for col in hashmap:
        if col[0] in key:
            found = True
            miles = col[1]
    if found:
        return miles
    else:
        print("not found")

# This function opens the csv file for reading.
# It returns the hashtable function.
def open_csv():
    with open('WGUPSDistanceTable.csv') as distance:
        read_table = csv.reader(distance, delimiter=',')
        return hashtable(read_table)

# Main function
def main():
    open_csv()

main()
