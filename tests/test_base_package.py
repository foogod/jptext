import jptext

def test_imports():
    "Make sure that importing the toplevel jptext module also imports all the relevant submodules"
    assert "charset" in jptext.__dict__
    assert "romaji" in jptext.__dict__
    assert "furigana" in jptext.__dict__
    assert "jmdict" in jptext.__dict__
    assert "kanjidic" in jptext.__dict__
