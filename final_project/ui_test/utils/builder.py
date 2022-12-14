from dataclasses import dataclass
import faker

fake = faker.Faker()


class Builder:
    @staticmethod
    def app_user(fake_username=None, fake_password=None):
        @dataclass
        class User:
            fake_name: str
            fake_surname: str
            fake_middle_name: str
            fake_username: str
            fake_email: str
            fake_password: str

        if fake_username is None:
            fake_username = 'ui' + fake.user_name()
            while True:
                if len(fake_username) in range(6, 17):
                    fake_username = fake_username
                    break
                else:
                    fake_username = 'ui' + fake.user_name()

        if fake_password is None:
            fake_password = fake.password()

        fake_name = fake.name().split()[0]
        fake_surname = fake.name().split()[-1]
        fake_middle_name = 'middle'
        fake_email = 'api' + fake.email()

        return User(fake_username=fake_username, fake_password=fake_password, fake_name=fake_name,
                    fake_email=fake_email, fake_surname=fake_surname, fake_middle_name=fake_middle_name)
