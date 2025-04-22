from backend.simulator.swagger.generator.printer_data_gen import PrinterDataGenerator


class PrinterService:
    def __init__(self):
        self.printer_memory = PrinterDataGenerator()

    def gen_basic_info(self) -> dict:
        return self.printer_memory.generate_printer_info()

    def get_printer_status(self) -> dict:
        return self.printer_memory.generate_printer_status()


if __name__ == "__main__":
    simulator = PrinterService()

    print(simulator.gen_basic_info())
    print(simulator.get_printer_status())

