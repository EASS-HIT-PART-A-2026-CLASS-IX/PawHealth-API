import pytest
from frontend.client import add_dog, get_dogs

def test_ui_to_backend_flow():
    test_name = "Joey_Test"
    add_dog(name=test_name, breed="Golden", age=3)
    dogs = get_dogs()
    assert any(d["name"] == test_name for d in dogs)
