from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    gender: str
    phone_number: str
    date_of_birth: str
    subject: str
    interests: str
    file: str
    current_address: str
    state: str
    city: str
