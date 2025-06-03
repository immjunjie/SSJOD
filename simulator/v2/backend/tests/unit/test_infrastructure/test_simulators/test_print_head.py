from simulator.v2.backend.app.infrastructure.simulators.print_head_sim import PrintHeadSimulator
import pytest

@pytest.mark.asyncio
async def test_get_temperature_returns_fixed_value():
    simulator = PrintHeadSimulator()
    temperature = await simulator.get_temperature()
    assert temperature == 50.0