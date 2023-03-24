import database
import database_helper

def test_get_attr_from_sent_history():
    uid = database.create_user()
    assert database_helper.get_attr_from_sent_history("user_id",-1 * uid) == uid 

def test_get_all_sent_history_info():
    user_id = database.create_user()
    receiver_id = database.create_user()
    ids = database.create_sent_history(user_id, receiver_id)
    print(ids)
    sent_id = ids[0]
    database.update_history(sent_id, "en")
    database.update_history(sent_id, "en")
    database.update_history(sent_id, "en")
    database.update_history(sent_id, "en")
    database.update_history(sent_id, "fr")
    database.update_history(sent_id, "fr")
    database.update_history(sent_id, "es")
    info = database.get_all_sent_history_info(sent_id)
    assert info.get("sent_id") == str(sent_id)
    assert info.get("user_id") == str(user_id)
    assert info.get("recipient_history_id") == str(ids[1])
    assert info.get("conv_messages_lang") == "en"
    assert info.get("all_messages_lang") == "en"
    assert info.get("last_message_lang") == "es"
    assert info.get("is_all_messages") == "False"
    assert info.get("en") == str(4)
    assert info.get("fr") == str(2)
    assert info.get("es") == str(1)
    assert info.get("total") == str(7)


