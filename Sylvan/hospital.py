class Hospital:
    def __init__(self, hospital_id, name, start_time, end_time, reservation_param):
        self._hospital_id = hospital_id
        self._name = name
        self._start_time = start_time
        self._end_time = end_time
        self._reservation_param = reservation_param
        self._key = 0

    def __str__(self):
        return f'str : {{\'id\':\'{self._hospital_id}\',\'name\':\'{self._name}\',\'start_time\':\'{self._start_time}\',\'end_time\':\'{self._end_time}\'}}'

    @property
    def hospital_id(self):
        return self._hospital_id

    @hospital_id.setter
    def hospital_id(self, hospital_id):
        self._hospital_id = hospital_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time

    @property
    def reservation_param(self):
        return self._reservation_param

    @reservation_param.setter
    def reservation_param(self, reservation_param):
        self._reservation_param = reservation_param

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key
