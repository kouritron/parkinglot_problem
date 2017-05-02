
from parkinglot import *


#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------  stupid UI to test the public API
class ParkingLotCMDUI(object):

    def __init__(self):
        """ Initialize a new parking lot controller. """
        super(ParkingLotCMDUI, self).__init__()

    def print_main_menu(self):
        """ """

        msg = ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> menu: \n"
        msg += "10. park new car \n"
        msg += "20. get car back with ticket number \n"
        msg += "30. get incurred cost on ticket number so far. \n"
        msg += "40. print the parking lot state \n"
        msg += "50. compactify parking lot. \n"
        msg += "60. advance time by 1 min \n"
        msg += "61. advance time by 10 min \n"
        msg += "62. advance time by 60 min \n"
        msg += "63. advance time by 300 min \n"
        msg += "64. advance time by 900 min \n"
        msg += "70. get time now \n"
        msg += "90. Exit"
        print msg


    def read_car(self):
        """ Return a new car object created with plate, model, and size values read from stdin. """

        plate = raw_input("Enter plate number: ")
        model = raw_input("Enter car model: ")
        size = None
        size_choice = None

        while True:
            size_line = raw_input("Choose car size, 1.Small  -- 2.Medium -- 3.Large: ")
            try:
                size_choice = int(size_line.strip())
            except:
                continue

            if size_choice in {1, 2, 3}:
                break

        if 1 == size_choice:
            size = LotSize.SMALL
        elif 2 == size_choice:
            size = LotSize.MEDIUM
        elif 3 == size_choice:
            size = LotSize.LARGE

        return Car(plate=plate, model=model, size=size)



    def mainloop(self):
        pc = ParkingLotController(small_count=3, small_rate=1, medium_count=4, medium_rate=2, large_count=10,
                                  large_rate=87000)

        print "populating lot with some sample cars. "
        cars = []
        cars.append(Car(plate='AAA 4001', model='horse', size=LotSize.MEDIUM))
        cars.append(Car(plate='AAA 4002', model='donkey', size=LotSize.MEDIUM))
        cars.append(Car(plate='AAA 8001', model='space ship', size=LotSize.LARGE))
        cars.append(Car(plate='AAA 2002', model='space ship', size=LotSize.LARGE))
        cars.append(Car(plate='AAA 2002', model='bike', size=LotSize.SMALL))
        cars.append(Car(plate='AAA 2003', model='bike', size=LotSize.SMALL))
        cars.append(Car(plate='AAA 2004', model='bike', size=LotSize.SMALL))
        cars.append(Car(plate='XXXtraaaa111', model='bike', size=LotSize.SMALL))
        cars.append(Car(plate='XXXtraaaa222', model='bike', size=LotSize.SMALL))
        cars.append(Car(plate='XXXdummass', model='bike', size=LotSize.SMALL))

        for car in cars:
            ticket_no = pc.park_car_and_return_ticket_number(car)
            print "Car successfully parked. here is your ticket no: " + str(ticket_no)



        print "--------------------------------------------------------------------------------------------------------"



        while True:
            self.print_main_menu()
            choice_line = raw_input("choose an option: ")
            try:
                choice_num = int(choice_line.strip())
            except:
                continue

            if 90 == choice_num:
                return

            elif 10 == choice_num:
                car = self.read_car()
                ticket_no = pc.park_car_and_return_ticket_number(car)
                print "Car successfully parked. here is your ticket no: " + str(ticket_no)

            elif 20 == choice_num:
                ticket_no = None
                try:
                    ticket_no = int(raw_input("Enter ticket number: ").strip())
                except:
                    continue

                car, cost = pc.return_car_and_get_cost_for_ticket_number(ticket_no=ticket_no)
                if not car:
                    print "invalid ticket number"
                    continue

                print "Here is your car: " + str(car)
                print "Here is your total cost: " + str(cost)


            elif 30 == choice_num:
                ticket_no = None
                try:
                    ticket_no = int(raw_input("Enter ticket number: ").strip())
                except:
                    continue

                cost = pc.get_cost_for_ticket_number(ticket_no=ticket_no)

                if not cost:
                    print "Invalid ticket no supplied. "
                    continue
                else:
                    print "Ticket number " + str(ticket_no) + " has incurred " + str(cost) + " dollars so far"

            elif 40 == choice_num:
                print str(pc)

            elif 50 == choice_num:
                pc.compactify_parking_lot()

            elif 60 == choice_num:
                TimeHelper.advance_time(seconds_to_advance_by=60)

            elif 61 == choice_num:
                TimeHelper.advance_time(seconds_to_advance_by=600)

            elif 62 == choice_num:
                TimeHelper.advance_time(seconds_to_advance_by=3600)

            elif 63 == choice_num:
                TimeHelper.advance_time(seconds_to_advance_by=300*60)

            elif 64 == choice_num:
                TimeHelper.advance_time(seconds_to_advance_by=900*60)

            elif 70 == choice_num:
                now = TimeHelper.get_time()
                print ">> Time is: " + str(now) + " seconds passed Jan 1 1970  or in YY-MM-DD HH:MM:SS "
                print ">> Time: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
            else:
                print "Invalid choice."






if '__main__' == __name__:

    #print 'hi'
    #c1 = Car(plate='ZXw21', model='horse', size=LotSize.LARGE)
    #print str(c1)

    cmd_ui = ParkingLotCMDUI()
    try:
        cmd_ui.mainloop()
    except EOFError:
        pass

    print "Exiting"

