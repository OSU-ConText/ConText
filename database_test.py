import database
import database_helper

def test_get_attr_from_sent_history():
    uid = database.create_user()
    assert database_helper.get_attr_from_sent_history("user_id",-1 * uid) == uid 

def test_get_attr_from_sent_history_1():
    uid = database.create_user()
    sid = database.create_sent_history(uid, 1)
    database.update_history(sid[0], "af")
    assert database_helper.get_attr_from_sent_history("user_id",sid[0]) == uid
    assert database_helper.get_attr_from_sent_history("sent_id",sid[0]) == sid[0]
    assert database_helper.get_attr_from_sent_history("recipient_history_id",sid[0]) == sid[1]
    assert database_helper.get_attr_from_sent_history("af",sid[0]) == 1
    assert database_helper.get_attr_from_sent_history("en",sid[0]) == 0
    assert database_helper.get_attr_from_sent_history("conv_messages_lang",sid[0]) == 'af'
    assert database_helper.get_attr_from_sent_history("last_message_lang",sid[0]) == 'af'

def test_update_history():
    uid1 = database.create_user()
    uid2 = database.create_user()
    info = database.get_all_sent_history_info(-uid1)
    assert info.get("sent_id") == str(-uid1)
    assert info.get("user_id") == str(uid1)
    assert info.get("recipient_history_id") == str(-uid1)
    assert info.get("conv_messages_lang") == None
    assert info.get("all_messages_lang") == None
    assert info.get("last_message_lang") == None
    assert info.get("is_all_messages") == "True"
    assert info.get("total") == str(0)
    ids = database.create_sent_history(uid1, uid2)
    database.update_history(ids[0], 'en')
    info = database.get_all_sent_history_info(ids[0])
    assert info.get("sent_id") == str(ids[0])
    assert info.get("user_id") == str(uid1)
    assert info.get("recipient_history_id") == str(ids[1])
    assert info.get("conv_messages_lang") == "en"
    assert info.get("all_messages_lang") == "en"
    assert info.get("last_message_lang") == "en"
    assert info.get("is_all_messages") == "False"
    assert info.get("en") == str(1)
    assert info.get("total") == str(1)
    database.update_history(ids[0], 'fr')
    database.update_history(ids[0], 'en')
    info = database.get_all_sent_history_info(ids[0])
    assert info.get("sent_id") == str(ids[0])
    assert info.get("user_id") == str(uid1)
    assert info.get("recipient_history_id") == str(ids[1])
    assert info.get("conv_messages_lang") == "en"
    assert info.get("all_messages_lang") == "en"
    assert info.get("last_message_lang") == "en"
    assert info.get("is_all_messages") == "False"
    assert info.get("en") == str(2)
    assert info.get("fr") == str(1)
    assert info.get("total") == str(3)
    uid1 = database.create_user()
    uid2 = database.create_user()
    info = database.get_all_sent_history_info(-uid1)
    database.update_history(ids[0], 'zu')
    database.update_history(ids[0], 'zu')

def test_update_history_1():
    uid1 = database.create_user()
    uid2 = database.create_user()
    ids = database.create_sent_history(uid1, uid2)
    database.update_history(ids[0], 'zu')
    info = database.get_all_sent_history_info(ids[0])
    assert info.get("sent_id") == str(ids[0])
    assert info.get("user_id") == str(uid1)
    assert info.get("recipient_history_id") == str(ids[1])
    assert info.get("conv_messages_lang") == "zu"
    assert info.get("all_messages_lang") == "zu"
    assert info.get("last_message_lang") == "zu"
    assert info.get("is_all_messages") == "False"
    assert info.get("zu") == str(1)
    assert info.get("total") == str(1)

def test_get_sent_ids():
    uid1 = database.create_user()
    uid2 = database.create_user()
    uid3 = database.create_user()
    uid4 = database.create_user()
    uid5 = database.create_user()
    sid1 = database.create_sent_history(uid1, uid2)[0]
    sid2 = database.create_sent_history(uid1, uid3)[0]
    sid3 = database.create_sent_history(uid1, uid4)[0]
    sid4 = database.create_sent_history(uid1, uid5)[0]
    ids = database.get_sent_ids(uid1)
    assert ids == [-uid1, sid1, sid2, sid3, sid4]

def test_get_sent_ids_1():
    uid1 = database.create_user()
    ids = database.get_sent_ids(uid1)
    assert ids == [-uid1]

def test_get_sent_ids_2():
    uid1 = database.create_user()
    uid2 = database.create_user()
    uid3 = database.create_user()
    uid4 = database.create_user()
    uid5 = database.create_user()
    sid1 = database.create_sent_history(uid1, uid2)[0]
    sid2 = database.create_sent_history(uid2, uid3)
    sid3 = database.create_sent_history(uid2, uid4)
    sid4 = database.create_sent_history(uid2, uid5)
    ids = database.get_sent_ids(uid1)
    assert ids == [-uid1, sid1]

def test_get_users_sent_history():
    uid1 = database.create_user()
    uid2 = database.create_user()
    sid1 = database.create_sent_history(uid1, uid2)
    assert database.get_users_sent_history(sid1[0]) == [uid1, uid2]
    assert database.get_users_sent_history(sid1[1]) == [uid2, uid1]

def test_get_users_sent_history_1():
    uid1 = database.create_user()
    uid2 = database.create_user()
    uid3 = database.create_user()
    uid4 = database.create_user()
    uid5 = database.create_user()
    sid1 = database.create_sent_history(uid1, uid2)
    sid2 = database.create_sent_history(uid2, uid3)
    sid3 = database.create_sent_history(uid1, uid4)
    sid4 = database.create_sent_history(uid3, uid5)
    assert database.get_users_sent_history(sid1[0]) == [uid1, uid2]
    assert database.get_users_sent_history(sid2[0]) == [uid2, uid3]
    assert database.get_users_sent_history(sid3[0]) == [uid1, uid4]
    assert database.get_users_sent_history(sid4[0]) == [uid3, uid5]

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


