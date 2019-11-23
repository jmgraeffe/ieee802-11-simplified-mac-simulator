import copy


class Simulation:
    class _Log(list):
        def append(self, obj):
            super().append(copy.deepcopy(obj))

    def __init__(self):
        self.frame_log = Simulation._Log()  # history of what happened in a time slot (e.g. data sent by station x, or a collision, or nothing)
        self.station_log = Simulation._Log()  # history of station states (backoff counter etc.)
        self.collisions_stations = 0  # collisions over all stations, e.g. if you've multiple stations there can be multiple collisions per time slot
        self.collisions_ap = 0  # collisions as seen from the AP, so even if multiple stations are trying to send, there will be only one collision
        self.successful_transmissions = 0  # since collisions do not occur even when no data is transmitted in a time slot at all, this is also an important factor
        # you could alternatively calculate that afterwards by counting the None values in frame_log by iterating over it, but for performance we just do it on the go


class Medium:
    def __init__(self, ap):
        self.iteration = 0
        self.sending_stations_this_iteration = []
        self.ap = ap

    def evaluate_iteration(self):
        num_sending_stations = len(self.sending_stations_this_iteration)

        if num_sending_stations > 0:
            if num_sending_stations == 1:
                station = self.sending_stations_this_iteration[0]

                # tell station and AP that the station succeeded
                station.feedback(False)
                self.ap.data(station)

                return DataFrame(station)
            else:
                # tell every collided station that it collided as feedback
                # (theoretically, this would be done by the station/AP itself, e.g. by sensing the medium)
                for station in self.sending_stations_this_iteration:
                    station.feedback(True)

                # tell the AP that collisions occured
                # (theoretically, the AP won't know which stations caused the collision,
                # but it's simpler for programming to just pass it to the AP directly
                # and it does not change anything)
                self.ap.collision(self.sending_stations_this_iteration)

                return CollisionFrame(num_sending_stations)
        else:
            return None

    def next_iteration(self):
        self.iteration += 1
        self.sending_stations_this_iteration.clear()

    def send(self, station):
        self.sending_stations_this_iteration.append(station)


class Station:
    def __init__(self, num, medium):
        self.num = num
        self.medium = medium

    def feedback(self, collision):
        pass


class AccessPoint(Station):
    def __init__(self, medium):
        super().__init__(-1, medium)

    def data(self, station):
        pass

    def collision(self, stations):
        pass


class DataFrame:
    def __init__(self, station):
        self.station = station


class CollisionFrame:
    def __init__(self, collisions):
        self.collisions = collisions
