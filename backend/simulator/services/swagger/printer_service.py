from backend.simulator.generators.printer_status_gen import PrinterStatusGenerator


class PrinterService:
    def __init__(self):
        self.status_generator = PrinterStatusGenerator()

    def get_basic_info(self) -> dict:
        return self.status_generator.generate_general_status()

    def get_printer_status(self) -> dict:
        return self.status_generator.generate_printer_status()


if __name__ == "__main__":
    print("testing")
    o1 = PrinterService()

    t1 = o1.get_basic_info()
    print(t1)

    t2 = o1.get_printer_status()
    print(t2)

