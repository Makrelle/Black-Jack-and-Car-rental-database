# Project 4 - Car rental database
import os


print("Welcome to the Car rental app!")


path_to_files = os.getcwd() + "/files"
car_attributes = ["ID", "brand", "model", "model year", "power",
                 "consumption", "fuel", "transmission", "category", "price"]


def create_list_of_list(path_to_files):
    all_cars = []
    for id, car in enumerate(os.listdir(path_to_files)[:-2]):
        lst = get_info_from_file(path_to_files + "/" + car)
        lst.insert(0, id + 1)
        all_cars.append(lst)
    return all_cars


def get_info_from_file(filepath):
    lst = []
    with open(filepath, "r") as f:
        content = f.readlines()
        for line in content:
            line = line.strip("\n").split("=")
            if line[0] == "technical":
                continue
            lst.append(line[1])
    return lst


def check_available_cars(all_cars):
    available_cars = []
    with open(path_to_files + "/not_rented.txt", "r") as nr_file:
        content = nr_file.readlines()
        for line in content:
            for car in all_cars:
                if str(car[0]) == line.rstrip():
                    available_cars.append(car)
    return available_cars


def rent_a_car(all_cars):
    available_cars = check_available_cars(all_cars)
    print("Cars for rent: ")
    show_all_cars(available_cars)
    while True:
        car_to_rent = input("Enter ID of the car you want to rent: ")
        if not car_to_rent.isnumeric():
            print("Invalid input. Try again..")
            continue
        ids = []
        for car in available_cars:
            ids.append(car[0])
        if int(car_to_rent) not in ids:
            print("This car is not available.")
        else:
            i = ids.index(int(car_to_rent))
            print("Congratulations, you've rented", available_cars[i][1],
                  available_cars[i][2])
            move_car(car_to_rent)
            break


def move_car(car_to_move):
    with open(path_to_files + "/not_rented.txt", "r+") as nr_file:
        nr_file.seek(0)
        lines = nr_file.readlines()
        nr_file.seek(0)
        with open(path_to_files + "/rented.txt", "a", encoding="utf-8")\
                as r_file:
            for line in lines:
                if line.strip("\n") != car_to_move:
                    nr_file.write(line)
            r_file.write(car_to_move + "\n")


def main_menu(all_cars):
    while True:
        print("""MAIN MENU:
    ___________________________________________________________
    |  show all cars  |  search cars  |  rent a car  |  exit  |
    |       A         |       S       |       R      |    E   |
    -----------------------------------------------------------
    """)
        option = input("Please choose one option by pressing "
                       "A, S, R or E. ").lower()
        if option == "e":
            exit()
        elif option == "a":
            show_all_cars(all_cars)
        elif option == "s":
            search_cars(all_cars)
        elif option == "r":
            rent_a_car(all_cars)
        else:
            print("Invalid input. Try again")


def show_all_cars(all_cars):
    template = "|{:17}|{:^12}|"
    for car in all_cars:
        print("-" * 32)
        for i, value in enumerate(car):
            print(template.format(car_attributes[i], value))
        print("-" * 32)


def attributes_menu(selections, at):
    index = car_attributes.index(at)
    attributes = set(att[index] for att in selections)
    try:
        attributes = sorted(set(attributes), key=int)
    except ValueError:
        attributes = sorted(set(attributes))
    offer = ' | '.join(attributes)
    inp = input(f"| {at}: | {offer} | ENTER-all | R-reset | ").lower()
    if inp == "":
        return selections
    elif inp == "r":
        return []
    elif inp not in attributes:
        print("Wrong input. ")
        return selections
    else:
        new = [car for car in selections if inp in car]
        return new


def search_cars(all_cars):
    selections = all_cars
    while True:
        ats = " | ".join(at for at in car_attributes[1:])
        at = input(f"| {ats} | D-done | R-reset | E-exit to menu | ").lower()
        if at == "d":
            return show_all_cars(selections)
        elif at == "r":
            selections = all_cars
            continue
        elif at == "e":
            main_menu(all_cars)
        elif at in car_attributes:
            new = attributes_menu(selections, at)
            if new:
                selections = new
            else:
                selections = all_cars
        else:
            print("Wrong input. ")
            continue


def main():
    all_cars = create_list_of_list(path_to_files)
    main_menu(all_cars)
    print("Thank you for your visit. Good Bye! ")


main()
