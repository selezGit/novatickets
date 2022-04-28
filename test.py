class Err(Exception):
    def __init__(self):
        self.message = "test"
        super().__init__(self.message)


try:
    raise Err()

except Err as error:
    print(Err.message)
