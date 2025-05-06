class AuthDataGenerator:
    def __init__(self):
        self._message_check_by_id = None
        self._message_auth_verify = None
        self.generate_data()

    def generate_data(self):
        self._message_check_by_id = "authorized"
        self._message_auth_verify = "ok"

    def get_message_check_by_id(self):
        return self._message_check_by_id

    def get_message_auth_verify(self):
        return self._message_auth_verify


if __name__ == "__main__":
    generator = AuthDataGenerator()
    print("Check by ID:", generator.get_message_check_by_id())
    print("Verify:", generator.get_message_auth_verify())