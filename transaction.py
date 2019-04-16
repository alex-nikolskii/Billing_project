
class Transaction:
    def __init__(self, service, volume, date, location, sender,
                 recipient):
        self.service = service
        self.volume = volume
        self.date = date
        self.send_loc, self.recip_loc = location.lower().split('-')
        self.sender = sender
        self.recipient = recipient

    # Доделать форматирование вывода
    def __str__(self):
        return f'{self.service} {self.volume} {self.date} ' \
               f'{self.send_loc} {self.recip_loc} ' \
               f'{self.sender} {self.recipient}'
