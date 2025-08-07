from models.wardrobe import wardrobe

def test_wardrobe_basic():
    w = wardrobe()
    assert w is not None