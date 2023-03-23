import database
import database_helper

def test_get_attr_from_sent_history():
    uid = database.create_user()
    assert database_helper.get_attr_from_sent_history("user_id",-1 * uid) == uid 
