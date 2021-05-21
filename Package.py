import datetime
import PackageHashTable
import DistanceHashTable
import csv
import Main

class Package(object):

    # This is the constructor function, it defines an object/package.
    def __init__(self, package_id, address, city, state, zip_code,
                 delivery_deadline, weight, special_notes, delivery_status, delivery_time, distance_values, load_time):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes
        self.delivery_status = delivery_status
        self.delivery_time = delivery_time
        self.distance_values = distance_values
        self.load_time = load_time

# This function is used to retrieve and store data from the csv file into a hash table. : O(n)
# It creates a package object, that is then saved in the package hash table.
# Returns package hash map.
def get_data_from_csv(table, hashmap):

    # Loops through the package csv file, assigns a value to variable
    for row in table:
        package_id = int(row[0])
        address = row[1]
        city = row[2]
        state = row[3]
        zip_code = row[4]
        delivery_deadline = row[5]
        weight = int(row[6])
        special_notes = row[7]
        delivery_status = "AT HUB"
        delivery_time = None
        distance_values = None
        load_time = None

        # Creates a temporary object
        temp_package = Package(package_id, address, city, state, zip_code, delivery_deadline,
                               weight, special_notes, delivery_status, delivery_time, distance_values, load_time)

        # Inserts an object into the hashtable, the package_id is passed in as the key
        hashmap.insert_into_hashtable(package_id, temp_package)

    return hashmap

# This function loads the packages onto 1 of 2 trucks. : O(n)^2
# The package address is used to look for the distance values for that package.
# Then the distance values are saved to the package object to be used during delivery.
def load_trucks(hashmap, truck_num, hour, minute, pickup):
    first_truck = []
    second_truck = []
    first_pickup = []
    second_pickup = []
    max_capacity = 16
    first_truck_full = False
    second_truck_full = False

    for count in range(1, 41):
        package = hashmap.get(count)
        special_notes = package.special_notes
        package_address = (f"{package.address}\n({package.zip_code})")
        distance_values = DistanceHashTable.find_address_in_hashmap(package_address)
        package.distance_values = distance_values

        if pickup==False:
            if special_notes.startswith('Must be delivered with') and len(first_truck) < max_capacity:
                first_truck.append(package)
                package.delivery_status = "ON TRUCK"
                package.load_time = Main.running_time(hour, minute)

            elif special_notes.startswith("Can only be on truck 2") and len(second_truck) < max_capacity:
                second_truck.append(package)
                package.delivery_status = "ON TRUCK"
                package.load_time = Main.running_time(hour, minute)

            elif special_notes == '':
                if len(first_truck) < max_capacity:
                    first_truck.append(package)
                    package.delivery_status = "ON TRUCK"
                    package.load_time = Main.running_time(hour, minute)
                    if len(first_truck)+1 == max_capacity:
                        first_truck_full = True

                elif first_truck_full and not second_truck_full:
                    second_truck.append(package)
                    package.delivery_status = "ON TRUCK"
                    package.load_time = Main.running_time(hour, minute)
                    if len(second_truck)+1 == max_capacity:
                        second_truck_full = True

        if pickup==True:
            if (special_notes.startswith("Delayed") or special_notes.startswith("Wrong address listed")) and (truck_num == 1):
                first_pickup.append(package)
                package.delivery_status = "ON TRUCK"
                package.load_time = Main.running_time(hour, minute)

            elif (package.delivery_status == "AT HUB") and (truck_num == 2):
                second_pickup.append(package)
                package.delivery_status = "ON TRUCK"
                package.load_time = Main.running_time(hour, minute)

    #print("---TRUCKS HAVE BEEN LOADED---\n")
    return first_truck, second_truck, first_pickup, second_pickup

# This function contains the main algorithm of the project. : O(n)^2
# It contains the code to deliver the packages.
# A nearest neighbor algorithm is executed to deliver all the packages on the truck.
# Returns the sum of the path taken by the truck to deliver all the packages, total_miles.
# Pseudocode below:

# TRUCK DELIVERY FUNCTION
# Initialize variables | boolean pickup, int column, list path, int truck speed, datetime delayed time (9:05)
# Begin while loop | loop until length of truck list is greater than 0, basically until there are no packages on the truck

    # DELIVER CLOSEST PACKAGE
    # Initialize variable | int minimum distance value
    # For loop | For count :=  1 to len(truck) DO
        # Set variables | package to the value of truck at the count index, get distance values from package object
        # If statement | If the distance value at column index is less than the minimum distance value THEN
            # Set variable | minimum row set to count
            # Set variable | minimum package set to package
            # Set variable | minimum distance value set to distance value at column index
            # Set variable | zero place set to the index of the zero(min) in the distance values list
    # Append minimum distance value to path list
    # Pop/ remove the minimum row from the truck list
    # Set variable | column to zero place

    # UPDATE PACKAGE OBJECT INFORMATION
    # Calculate | total miles set to the sum of the path
    # Running time | hour set to total miles divided by truck speed
    # Running time | minutes set to total miles divided by truck speed minus hour times 60
    # Update package object | delivery time set to running time, delivery status set to delivered

    # GO BACK TO HUB TO PICK UP REMAINING PACKAGES
    # If statement | if the delivery time of the last delivered package is after 9:05
    # and the truck has not already gone back to the hub THEN
        # Set variables | pickup set to True
        # Append the distance of the package back to the hub to the path list
        # Update total miles, hour, and minutes
        # if statement | if truck number is 1 THEN
            # Set variable | pickup 1 set to list that load_truck passes in
            # For loop | for each package in pickup 1 list DO
                # Append package to the truck list
        # elif statement | if truck number is 2 THEN
            # Set variable | pickup 2 set to list that load_truck passes in
            # For loop | for each package in pickup 2 list DO
                # Append package to the truck list
        # Update variable | column set to 0, basically starting from the hub again

    # If statement | if the there is only one package on the truck THEN
        # Append the distance of that package to the hub to the path list
# Return total miles - sum of the path
def truck_delivery(hashmap, truck, truck_num):
    pickup = False
    delayed_time = datetime.timedelta(hours=9, minutes=5)
    column = 0
    path = []
    truck_speed = 18
    while len(truck) > 0:
        min_distance_value = 100
        for count in range(0, len(truck)):
            package = truck[count]
            distance_values = package.distance_values
            if distance_values[column] < min_distance_value:
                min_row = count
                min_package = package
                min_distance_value = distance_values[column]
                zero_place = distance_values.index(min(distance_values))
        path.append(min_distance_value)
        truck.pop(min_row)
        column = zero_place

        total_miles = sum(path)
        hour = total_miles // truck_speed
        minutes = ((total_miles / truck_speed) - hour) * 60
        status = hashmap.get(min_package.package_id)
        status.delivery_time = Main.running_time(hour, minutes)
        status.delivery_status = "DELIVERED"


        if status.delivery_time > delayed_time and not pickup:
            pickup = True
            path.append(distance_values[0])
            total_miles = sum(path)
            hour = total_miles // truck_speed
            minutes = ((total_miles / truck_speed) - hour) * 60
            if truck_num == 1:
                truck1, truck2, pickup1, pickup2 = load_trucks(hashmap, 1, hour, minutes, pickup=True)
                for i in pickup1:
                    truck.append(i)
            elif truck_num == 2:
                truck1, truck2, pickup1, pickup2 = load_trucks(hashmap, 2, hour, minutes, pickup=True)
                for i in pickup2:
                    truck.append(i)
            column = 0

        if len(truck) == 1:
            path.append(distance_values[0])


    # print("---ALL PACKAGES ON TRUCK HAVE BEEN DELIVERED---")
    # print('PATH TAKEN:', path, "\n")
    # print(sum(path))

    return total_miles


# This function opens the CSV file to be read.
# It returns the get_data_from_csv function so that the hashtable is created.
def open_csv():
    with open('WGUPSPackage.csv') as package:
        read_table = csv.reader(package, delimiter=',')
        lines = list(read_table)
        length = len(lines)
        hashmap = PackageHashTable.HashMap(length)

        return get_data_from_csv(lines, hashmap)

# Main function that calls the functions open_csv(), load_trucks(), truck_delivery(), and interface().
# This function is used to call all important functions to operate the program.
def main():
    hashmap = open_csv()
    truck1, truck2, pickup1, pickup2 = load_trucks(hashmap, 0, 0, 0, pickup=False)
    first_truck_milage = truck_delivery(hashmap, truck1, 1)
    second_truck_milage = truck_delivery(hashmap, truck2, 2)
    Main.interface(hashmap)

    print(f'Total miles traveled for truck number 1 : {first_truck_milage}')
    print(f'Total miles traveled for truck number 2 : {second_truck_milage}')
    print(f'Total miles of all trucks:  {first_truck_milage + second_truck_milage}')





