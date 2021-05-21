# Amanda Arreola - #001067645

import Package
import datetime

# This function contains all the console interface that a user interacts with.
# It provides a option menu for the user.
# A user can use this interface to find information on a package, or multiple packages. : O(n)^2
def interface(hashmap):
    print("WELCOME TO WGUPS")
    print("------------------")
    print('OPTION MENU')
    print('1. FIND A PACKAGE')
    print('2. STATUS OF ALL PACKAGES IN A TIME FRAME')
    print('3. EXIT')
    choice = int(input("Enter an option from the menu (1/2/3): "))

    while choice != 3:

        if choice == 1:
            look_for_package = "yes"
            while look_for_package == "yes":
                if look_for_package == "yes":
                    user_input = int(input("What package are you looking for?"))
                    hashmap.lookup_in_hashtable(user_input, single_package=True)
                    look_for_package = input("Would you like to look for another package? (yes/no)").lower()
            if look_for_package == "no":
                choice = int(input("Enter an option from the menu (1/2/3):\n "))


        if choice == 2:
            time_frame = "yes"
            while time_frame == "yes":
                if time_frame == "yes":
                    start_time_hour, start_time_minutes = input("Enter a start time for timeframe (HH:MM): ").split(":")
                    end_time_hour, end_time_minute = input("Enter an end time for timeframe (HH:MM): ").split(":")
                    start_time = datetime.timedelta(hours=int(start_time_hour), minutes=int(start_time_minutes))
                    end_time = datetime.timedelta(hours=int(end_time_hour), minutes=int(end_time_minute))
                    status_check(hashmap, start_time, end_time)
                    time_frame = input("Would you like to look in another timeframe? (yes/no)\n").lower()

            if time_frame == "no":
                choice = int(input("Enter an option from the menu (1/2/3): "))

    if choice == 3:
        print("Thank you for visiting WGUPS. Goodbye!\n")

# This function is called to provide that status of all packages during a specific time frame. : O(n)
def status_check(hashmap, starttime, endtime):
    for count in range(1, 41):
        package = hashmap.get(count)
        load_time = package.load_time
        delivery_time = package.delivery_time

        if (starttime < delivery_time < endtime) or starttime >= delivery_time:
            package_info = (f'Package #{package.package_id} has been delivered.')
            print(package_info, end=' ')
        elif (starttime >= load_time) and (starttime < delivery_time > endtime):
            package_info = (f'Package #{package.package_id} is on route.')
            print(package_info, end=' ')
        elif (starttime > load_time) and (delivery_time > endtime):
            package_info = (f'Package #{package.package_id} is on route.')
            print(package_info, end=' ')
        elif (load_time > starttime) and (endtime < load_time):
            package_info = (f'Package #{package.package_id} is at the hub.')
            print(package_info, end=' ')
        elif (load_time > starttime) and (endtime > load_time):
            package_info = (f'Package #{package.package_id} is at the hub.')
            print(package_info, end=' ')

        hashmap.lookup_in_hashtable(count, single_package=False)

# This function provides the running time for the program.
# It can be called to provide a start, load, or delivery timestamp.
def running_time(hours, minutes):
    start_time = datetime.timedelta(hours=8, minutes=00)
    package_status_time = start_time + datetime.timedelta(hours=hours, minutes=minutes)
    return package_status_time

def main():
    Package.main()
main()
