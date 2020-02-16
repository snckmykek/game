from sqlite_requests import db


def speech_parser():
    if not db.table_is_empty():
        return

    with open('/speech.txt', 'r', encoding='utf-8') as f:
        values = f.readlines()

    for s in values:
        if s == '\n':
            continue
        s2 = list()
        for val in s.split('|'):
            if '\n' == val[::-2]:
                val = val[-2]
            try:
                val = int(val)
            except:
                pass
            val = str(val)

            s2.append(val)
        s2[-1] = 0 if s2[-1] == '' else s2[-1]
        db.insert_speech(s2)
    db.commit()
