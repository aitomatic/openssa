from openssm.utils.utils import Utils

class TestUtils:
    def test_canonicalize_user_input_str(self):
        assert Utils.canonicalize_user_input('hello') == [{'role': 'user', 'content': 'hello'}]

    def test_canonicalize_user_input_list(self):
        assert Utils.canonicalize_user_input([{'role': 'user', 'content': 'hello'}]) == [{'role': 'user', 'content': 'hello'}]
        assert Utils.canonicalize_user_input(['hello']) == [{'role': 'user', 'content': 'hello'}]
        assert Utils.canonicalize_user_input([{'message': 'hello'}]) == [{'role': 'user', 'content': "{'message': 'hello'}"}]

    def test_canonicalize_user_input_dict(self):
        assert Utils.canonicalize_user_input({'role': 'user', 'content': 'hello'}) == [{'role': 'user', 'content': 'hello'}]
        assert Utils.canonicalize_user_input({'message': 'hello'}) == [{'message': 'hello'}]

    def test_canonicalize_user_input_other(self):
        assert Utils.canonicalize_user_input(1) == [{'role': 'user', 'content': '1'}]

    def test_canonicalize_query_response_str(self):
        assert Utils.canonicalize_query_response('hello') == [{'role': 'assistant', 'content': 'hello'}]

    def test_canonicalize_query_response_list(self):
        assert Utils.canonicalize_query_response([{'role': 'assistant', 'content': 'hello'}]) == [{'role': 'assistant', 'content': 'hello'}]
        assert Utils.canonicalize_query_response(['hello']) == [{'role': 'assistant', 'content': 'hello'}]
        assert Utils.canonicalize_query_response([{'message': 'hello'}]) == [{'role': 'assistant', 'content': "{'message': 'hello'}"}]

    def test_canonicalize_query_response_dict(self):
        assert Utils.canonicalize_query_response({'role': 'assistant', 'content': 'hello'}) == [{'role': 'assistant', 'content': 'hello'}]
        assert Utils.canonicalize_query_response({'response': 'hello'}) == [{'role': 'assistant', 'content': 'hello'}]
        assert Utils.canonicalize_query_response({'message': 'hello'}) == [{'role': 'assistant', 'content': "{'message': 'hello'}"}]

    def test_canonicalize_query_response_other(self):
        assert Utils.canonicalize_query_response(1) == [{'role': 'assistant', 'content': '1'}]
