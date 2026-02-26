
class Person:
    def __init__(self, id_num, name, phone):
        self.id_num = id_num  
        self.phone = phone    
        self._name = name     

    @property
    def id_num(self):
        return self.__id_num
    
    @id_num.setter
    def id_num(self, new_id):
        if len(str(new_id)) == 9:
            self.__id_num = new_id
        else:
            raise ValueError("ID number must be exactly 9 characters.")

    @property
    def phone(self):
        return self.__phone
    
    @phone.setter
    def phone(self, new_phone):
        if len(str(new_phone)) >= 9:
            self.__phone = new_phone
        else:
            raise ValueError("Phone number must contain at least 9 characters.")

    def __str__(self):
        return f"ID: {self.__id_num} | Name: {self._name} | Phone: {self.__phone}"

class Member(Person):
    def __init__(self, id_num, name, phone, member_type, balance=0, status="Active"):
        super().__init__(id_num, name, phone)
        self.member_type = member_type
        self.balance = balance
        self.status = status

    def renew_membership(self, entries):
        self.balance += entries
        self.status = "Active"

    def deduct_entry(self):
        if self.balance > 0:
            self.balance -= 1
            if self.balance == 0:
                self.status = "Deactive" 
            return True
        return False

    def deactivate(self):
        self.status = "Deactive"
    
    def active(self):
        return self.status == "Active"

    def __str__(self):
        base_info = super().__str__()
        return f"[Member] {base_info} | Type: {self.member_type} | Balance: {self.balance} | Status: {self.status}"

class Trainer(Person):
    def __init__(self, id_num, name, phone, specialty, rank):
        super().__init__(id_num, name, phone)
        self.specialty = specialty
        self.rank = rank

    def __str__(self):
        base_info = super().__str__()
        return f"[Trainer] {base_info} | Specialty: {self.specialty} | Rank: {self.rank}"

class WorkoutSession:
    def __init__(self, session_id, name, trainer, max_capacity=10):
        self.session_id = session_id
        self.name = name
        self.trainer = trainer  
        self.members = []       
        self.max_capacity = max_capacity

    def add_member(self, member):
        if len(self.members) < self.max_capacity:
            self.members.append(member)
            return True
        return False

    def __str__(self):
        trainer_name = self.trainer._name if self.trainer else "No Trainer"
        return f"[Session {self.session_id}] {self.name} | Trainer: {trainer_name} | Capacity: {len(self.members)}/{self.max_capacity}"