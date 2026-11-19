# mock
# ===============================
# TEST 1
# def test_handler_runs_backfill(monkeypatch):
#     called = []

#     monkeypatch.setattr(
#         lambda_handler,
#         "run_backfill",
#         lambda: called.append("backfill")
#     )

#     result = lambda_handler.lambda_handler({"mode": "backfill"}, None)

#     assert called == ["backfill"]
#     assert result == {"status": "ok", "mode": "backfill"}

# # ===============================
# # TEST 2
# def test_handler_runs_incremental(monkeypatch):
#     called = []

#     monkeypatch.setattr(
#         lambda_handler,
#         "run_incremental",
#         lambda: called.append("incremental")
#     )

#     result = lambda_handler.lambda_handler(
#         {"mode": "incremental"}, None
#     )

#     assert called == ["incremental"]
#     assert result == {"status": "ok", "mode": "incremental"}

# # ===============================
# # TEST 3
# def test_handler_rejects_invalid_mode():
#     with pytest.raises(ValueError):
#         lambda_handler.lambda_handler(
#             {"mode": "invalid"}, None
#         )
