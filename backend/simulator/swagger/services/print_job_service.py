from backend.simulator.swagger.generators.print_job_gen import PrintJobDataGenerator
from typing import Dict, Any


class PrintJobService:
    def __init__(self):
        self.printer_memory = PrintJobDataGenerator()
        self.message = '{"service message": "testing"}'

    def gen_basic_info(self) -> dict:
        print(self.printer_memory.current_job)
        self.printer_memory.refresh_job()
        print(self.printer_memory.get_component("metadata"))
        return self.printer_memory.current_job

    def get_message(self):
        return self.message


if __name__ == "__main__":
    service = PrintJobService()
    print(service.get_message())
    print(service.gen_basic_info())