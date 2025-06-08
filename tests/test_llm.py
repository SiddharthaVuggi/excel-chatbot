from llm_engine.llm import call_llm

def test_llm():
    out = call_llm("Hello")
    assert isinstance(out, str)