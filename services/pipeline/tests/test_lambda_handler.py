import pytest
from pipeline.aws.lambda_handler import lambda_handler

def test_lambda_handler(monkeypatch):
    calls = []
    
    monkeypatch.setattr(
        "pipeline.aws.lambda_handler.main",
        lambda: calls.append("raw")
    )
    monkeypatch.setattr(
        "pipeline.aws.lambda_handler.load_gold",
        lambda: calls.append("gold")
    )
    monkeypatch.setattr(
        "pipeline.aws.lambda_handler.load_insight",
        lambda: calls.append("insight")
    )
    
    # sample event
    event = {}
    
    # call handler
    response = lambda_handler(event, None)
    
    # check response
    assert response["statusCode"] == 200
    assert response["body"] == "ok"
    
    # check execution order
    assert calls == ["raw", "gold", "insight"]