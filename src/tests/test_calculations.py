from logic.calculations import final_price_calculate

def test_calculate():
    assert final_price_calculate(100, 0.1) == 110