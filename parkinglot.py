

import time


# utility time reading functions
class TimeHelper(object):

    # this helps us do things like advance time by an hour, instead of singleton just use class vars and methods.
    _simulated_elapsed_time = 0

    @classmethod
    def get_time(cls):
        """ Return the number of seconds that have passed since Jan 1 1970 as an int. """

        seconds_since_jan1_1970 = int(time.time())
        return seconds_since_jan1_1970 + cls._simulated_elapsed_time

    @classmethod
    def advance_time(cls, seconds_to_advance_by):
        """ Advance time by as many seconds as the supplied argument. so that a future call to get_time()
        returns time values advanced by this much.
        """
        assert isinstance(seconds_to_advance_by, int)

        cls._simulated_elapsed_time += seconds_to_advance_by



class LotSize(object):
    """ Enumerate different lot sizes. Python 2.7 does not have built in enums, 
    so this is the closest thing I could find. """

    # maintain increasing order for easy comparison (i.e. assert small < medium)
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

    Sizes = {SMALL, MEDIUM, LARGE}


class Car(object):

    def __init__(self, plate, model, size):
        """ Initialize a new car with the given, plate, model, and size information """

        super(Car, self).__init__()

        assert isinstance(plate, str)
        assert isinstance(model, str)
        assert size in LotSize.Sizes

        self._plate = plate
        self._model = model
        self._size = size

    def get_size(self):
        return self._size

    def __str__(self):
        result = "Car with plate: " + str(self._plate) + " model: " + str(self._model)

        if LotSize.SMALL == self._size:
            return "Small " + result
        elif LotSize.MEDIUM == self._size:
            return "Medium " + result
        elif LotSize.LARGE == self._size:
            return "Large " + result
        else:
            return "Unknown sized " + result




class LotGroup(object):
    """ Track a group of lots of the same size. handle allocating/free lots from this group. """

    def __init__(self, lots_count, size, hourly_rate):
        """ Initialize a new lot group with the given number of lots of the given size with the hourly price. """

        super(LotGroup, self).__init__()

        assert isinstance(lots_count, int)
        assert isinstance(hourly_rate, int)

        assert (size in LotSize.Sizes)

        # we can allow empty lot group even though it probably has no use.
        assert lots_count >= 0

        self._lot_count = lots_count
        self._size = size
        self._hourly_rate = hourly_rate

        # lot allocation table: sparse hash table of (lot_id, car object)
        # lot_id is just an int in xrange(0, lot_count)
        # if a lot_id does not exist as a key in this table, then that lot_id is free.
        # when a car leaves a lot that row should be deleted from this table. so that len(self.lots) returns
        # the number of cars in this lot group.
        self._lots = {}

    def __str__(self):
        """ Return a string representation of this lot group. """

        size_class_str = None
        if self._size == LotSize.SMALL:
            size_class_str = "Small"
        elif self._size == LotSize.MEDIUM:
            size_class_str = "Medium"
        elif self._size == LotSize.LARGE:
            size_class_str = "Large"
        else:
            size_class_str = "Unknown size"

        lg_state = "********** lot group with size class: " + size_class_str + "\n"
        lg_state += "with number of spots: " + str(self._lot_count) + "\n"
        lg_state += "with rate of: " + str(self._hourly_rate) + " dollar(s) per hour. \n"

        if len(self._lots):
            lg_state += "cars parked in this lot group are: \n"

            for car in self._lots.itervalues():
                lg_state += "++" +str(car) + "\n"
        else:
            lg_state += 'no cars parked in this lot group. \n'

        return lg_state


    def get_spot_count(self):
        return self._lot_count

    def get_size_class(self):
        return self._size

    def has_space(self):
        """ Return True if this lot group has space for at least one more car that can fit in this group. 
        Otherwise return False. """

        if len(self._lots) < self._lot_count:
            return True
        else:
            return False

    def can_fit(self, car):
        """ Return True if the given car can potentially fit in  lots owned by this lot group.
         Else return False. """

        if car.get_size() <= self._size:
            return True
        else:
            return False

    def find_spot_and_park(self, car):
        """ Find an empty lot, save the car there, and Return its lot_id if possible. 
         Return None if no spot is available. """

        assert self.can_fit(car)

        # we could also save the last index and start the search from where we left of last time.
        for lot_id in xrange(0, self._lot_count):

            if not self._lots.has_key(lot_id):
                # found first non-existent lot_id
                self._lots[lot_id] = car
                return lot_id

        return None

    def get_car(self, lot_id):
        """ Return a reference to the car object at lot_id in this lot group. Does not remove the car object. """

        assert lot_id >= 0
        assert lot_id < self._lot_count

        if self._lots.has_key(lot_id):
            return self._lots[lot_id]

        # if there is no car at lot_id
        return None

    def remove_car(self, lot_id):
        """ Remove and return a the car object at lot_id in this lot group. """

        assert lot_id >= 0
        assert lot_id < self._lot_count

        if self._lots.has_key(lot_id):
            car = self._lots[lot_id]
            del self._lots[lot_id]
            return car

        # if there is no car at lot_id
        return None

    def get_hourly_rate(self):
        """ Return the the hourly price of parking a car in this lot group. """

        return self._hourly_rate


class Ticket(object):

    def __init__(self, lot_group, lot_id):
        """ Create a new Ticket for a car parked at lot_group and lot_id. """

        super(Ticket, self).__init__()

        assert isinstance(lot_group, LotGroup)
        assert isinstance(lot_id, int)
        assert (0 <= lot_id) and (lot_id < lot_group.get_spot_count())


        self._lot_id = lot_id
        self._lot_group = lot_group

        self._cost_so_far = 0

        # time ticket was issued, this is only necessary if we need to print when this ticket was issued or something
        # like that. not needed for calculating cost.
        self._start_time_ticket_issue = TimeHelper.get_time()

        # time car is been resident in its current lot group. (this get reset when car is relocated to better spot)
        self._start_time_current_spot = TimeHelper.get_time()



    def get_current_car_spot(self):
        """ Return the spot as a 2-tuple of (lot_group, lot_id) for the car associated with this ticket"""

        return (self._lot_group, self._lot_id)




    def update_car_location(self, new_lot_id, new_lot_group):
        """ Update the location information for the car associated with this Ticket and handle counting the 
         cost of the ticket. """

        assert isinstance(new_lot_group, LotGroup)
        assert isinstance(new_lot_id, int)
        assert (0 <= new_lot_id) and (new_lot_id < new_lot_group.get_spot_count())

        # calculate the incurred cost so far on the existing lot group before updating location.
        hourly_rate = self._lot_group.get_hourly_rate()

        now = TimeHelper.get_time()

        seconds_in_this_lg = now - self._start_time_current_spot

        self._cost_so_far += (seconds_in_this_lg / 3600.0) * hourly_rate


        # now update location to new spot.
        self._start_time_current_spot = now
        self._lot_id = new_lot_id
        self._lot_group = new_lot_group



    def get_cost(self):
        """ Return the costs ran up on this ticket so far. s"""

        # calculate the incurred cost so far on the existing lot group before updating location.
        hourly_rate = self._lot_group.get_hourly_rate()

        now = TimeHelper.get_time()

        seconds_in_this_lg = now - self._start_time_current_spot

        return self._cost_so_far + ((seconds_in_this_lg / 3600.0) * hourly_rate)


class ParkingLotController(object):

    def __init__(self, small_count, small_rate, medium_count, medium_rate, large_count, large_rate):
        """ Initialize a new parking lot controller. """

        super(ParkingLotController, self).__init__()

        self._lot_groups = []
        self._lot_groups.append( LotGroup(lots_count=small_count, size=LotSize.SMALL, hourly_rate=small_rate) )
        self._lot_groups.append( LotGroup(lots_count=medium_count, size=LotSize.MEDIUM, hourly_rate=medium_rate) )
        self._lot_groups.append( LotGroup(lots_count=large_count, size=LotSize.LARGE, hourly_rate=large_rate) )


        # table of ticket id to ticket objects. -- a ticket has:
        # lot_id of where the car is at right now
        # arrival time. total cost so far.
        self._tickets_table = {}

        # use this to implement an auto increment like ticket id allocation
        self._next_ticket_id = 1000

    def _allocate_new_ticket_id(self):
        """ Return a new unique ticket id while keeping track of previously allocated ticket ids so as to not 
        re-use them. """

        tid = self._next_ticket_id
        self._next_ticket_id +=1
        return tid


    def _get_best_spot(self, car):
        """ Given a car find and return a suitable spot as a 2-tuple (lot_group, lot id) for it to park in. 
        return (None, None) if no such spot exists. 
        """

        # lot groups are ordered from smallest to largest.
        for lot_group in self._lot_groups:
            if lot_group.can_fit(car) and lot_group.has_space():

                # this code is not multi thread in general, so presumably we don't deal with possibility that
                # space can be exhausted underneath us, just after we check for existence of empty space.
                return (lot_group, lot_group.find_spot_and_park(car))

        return (None, None)




    def _relocate_car_to_best_spot(self, ticket):
        """ Given a ticket for a car, see if we can park this car in a better location and do so if possible. """

        assert isinstance(ticket, Ticket)

        existing_lot_group, existing_lot_id = ticket.get_current_car_spot()

        car = existing_lot_group.get_car(lot_id=existing_lot_id)

        assert isinstance(car, Car)

        for lot_group in self._lot_groups:

            if (lot_group.can_fit(car) and lot_group.has_space() and
                (lot_group.get_size_class() < existing_lot_group.get_size_class())):

                car2 = existing_lot_group.remove_car(lot_id=existing_lot_id)
                assert  car == car2

                new_lot_id = lot_group.find_spot_and_park(car=car)

                ticket.update_car_location(new_lot_id=new_lot_id, new_lot_group=lot_group)

    def __str__(self):

        parking_lot_state =  "--------------------------- Parking lot has " + str(len(self._lot_groups)) + " lot groups"
        for lot_group in self._lot_groups:
            parking_lot_state += "\n" + str(lot_group)


        if len(self._tickets_table):
            parking_lot_state += "--------------------------- Tickets table has these entries  \n"
            parking_lot_state += "########################### Tickets table (Ticket no -- cost so far -- Car):\n"
            for tid, ticket in self._tickets_table.iteritems():
                lot_group, lot_id = ticket.get_current_car_spot()
                car = lot_group.get_car(lot_id=lot_id)
                parking_lot_state += str(tid) + " -- " + "{:16.6f}".format(ticket.get_cost()) + " -- " + str(car) + '\n'
            parking_lot_state += "########################### End Tickets table\n"


        return parking_lot_state

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------- Public API
    def compactify_parking_lot(self):

        for ticket in self._tickets_table.itervalues():
            self._relocate_car_to_best_spot(ticket)



    def park_car_and_return_ticket_number(self, car):
        """ Given a Car object park it in the cheapest spot, and give back a string with ticket number
         that can be used to retrieve the car. Returns None if no spot is available. """

        lot_group, lot_id = self._get_best_spot(car=car)

        if lot_group == None or lot_id == None:
            return None

        ticket = Ticket(lot_group=lot_group, lot_id=lot_id)
        ticket_id = self._allocate_new_ticket_id()

        # save it into allocated tickets
        self._tickets_table[ticket_id] = ticket
        return ticket_id


    def return_car_and_get_cost_for_ticket_number(self, ticket_no):
        """ Given a ticket number previously given out by this parking lot controller, find and return 
        the original car object as well as the total cost incurred so far as 2-tuple (car, cost) . """

        if not self._tickets_table.has_key(ticket_no):
            return (None, None)

        ticket = self._tickets_table[ticket_no]
        del self._tickets_table[ticket_no]

        cost = ticket.get_cost()
        current_lot_group, current_lot_id = ticket.get_current_car_spot()
        car = current_lot_group.remove_car(lot_id=current_lot_id)

        return car, cost

    def get_cost_for_ticket_number(self, ticket_no):
        """ Return the total cost of a ticket so far, or None if invalid ticket no supplied. """

        if not self._tickets_table.has_key(ticket_no):
            return None

        return self._tickets_table[ticket_no].get_cost()
























