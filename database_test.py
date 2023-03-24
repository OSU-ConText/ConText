import database
import database_helper

def test_get_attr_from_sent_history():
    uid = database.create_user()
    assert database_helper.get_attr_from_sent_history("user_id",-1 * uid) == uid 

#test with one convo
def test_get_all_sent_history_info_1():
    user_id = database.create_user()
    receiver_id = database.create_user()
    ids = database.create_sent_history(user_id, receiver_id)
    print(ids)
    sent_id = ids[0]
    recipient_history_id = ids[1]
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
    assert info.get("recipient_history_id") == str(recipient_history_id)
    assert info.get("conv_messages_lang") == "en"
    assert info.get("all_messages_lang") == "en"
    assert info.get("last_message_lang") == "es"
    assert info.get("is_all_messages") == "False"
    assert info.get("en") == str(4)
    assert info.get("fr") == str(2)
    assert info.get("es") == str(1)
    assert info.get("total") == str(7)

#test with two convos
def test_get_all_sent_history_info_2():
    user_id = database.create_user()
    receiver_id = database.create_user()
    ids = database.create_sent_history(user_id, receiver_id)
    sent_id = ids[0]
    database.update_history(sent_id, "en")
    database.update_history(sent_id, "en")
    database.update_history(sent_id, "fr")
    database.update_history(sent_id, "fr")
    database.update_history(sent_id, "en")
    user3 = database.create_user()
    sent_id2 = database.create_sent_history(user_id, user3)[0]
    database.update_history(sent_id2, "es")
    database.update_history(sent_id2, "es")
    database.update_history(sent_id2, "es")
    database.update_history(sent_id2, "es")
    database.update_history(sent_id2, "es")
    database.update_history(sent_id2, "es")
    database.update_history(sent_id2, "en")
    info = database.get_all_sent_history_info(sent_id)
    assert info.get("sent_id") == str(sent_id)
    assert info.get("user_id") == str(user_id)
    assert info.get("recipient_history_id") == str(ids[1])
    assert info.get("conv_messages_lang") == "en"
    assert info.get("all_messages_lang") == "es"
    assert info.get("last_message_lang") == "en"
    assert info.get("is_all_messages") == "False"
    assert info.get("en") == str(3)
    assert info.get("fr") == str(2)
    assert info.get("total") == str(5)

#test with all convos row
def test_get_all_sent_history_info_3():
    user_id = database.create_user()
    receiver_id = database.create_user()
    ids = database.create_sent_history(user_id, receiver_id)
    sent_id = ids[0]
    database.update_history(sent_id, "en")
    database.update_history(sent_id, "en")
    database.update_history(sent_id, "es")
    database.update_history(sent_id, "fr")
    database.update_history(sent_id, "en")
    database.update_history(sent_id, "en")
    database.update_history(sent_id, "af")
    database.update_history(sent_id, "af")
    user3 = database.create_user()
    sent_id2 = database.create_sent_history(user_id, user3)[0]
    database.update_history(sent_id2, "es")
    database.update_history(sent_id2, "fr")
    database.update_history(sent_id2, "es")
    database.update_history(sent_id2, "es")
    database.update_history(sent_id2, "es")
    database.update_history(sent_id2, "es")
    database.update_history(sent_id2, "en")
    info = database.get_all_sent_history_info(-user_id)
    assert info.get("sent_id") == str(-user_id)
    assert info.get("user_id") == str(user_id)
    assert info.get("recipient_history_id") == str(-user_id)
    assert info.get("conv_messages_lang") == None
    assert info.get("all_messages_lang") == "es"
    assert info.get("last_message_lang") == None
    assert info.get("is_all_messages") == "True"
    assert info.get("es") == str(6)
    assert info.get("en") == str(5)
    assert info.get("fr") == str(2)
    assert info.get("af") == str(2)
    assert info.get("total") == str(15)


