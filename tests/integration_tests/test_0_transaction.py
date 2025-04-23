# class Test_Transaction(DBMixin, BaseTest_API):
#     http_method = HTTPMethod.POST
#     path_func = transaction_in
#     json = dict(
#         transaction_id=str(uuid4()),
#         user_id=str(uuid4()),
#         account_id=str(uuid4()),
#         amount=10.5,
#         signature="",
#     )
#     expected_response_json = []
