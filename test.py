class WithoutRepr():
    def __init__(self):
        self.value = "Hello, World!"

class WithRepr():
    def __init__(self) -> None:
        self.value = "Hello, World!"

    def __repr__(self) -> str:
        return self.value

if __name__ == "__main__":
    # driver code

    dummy1 = WithoutRepr()
    dummy2 = WithRepr()

    print(dummy1)
    print(dummy2)