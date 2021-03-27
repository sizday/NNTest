def if_has_say(nv, name):
    if nv.has_record(name):
        nv.say(name)


def hello_logic(nv, count_null):
    with nv.listen(
            'confirm, wrong_time, repeat',
            entities=['confirm', 'wrong_time', 'repeat'],
    ) as r:
        if r.utterance() == "" and count_null == 0:
            return hello_null(nv)
        elif r.utterance() == "" and count_null == 1:
            return hangup_null(nv)
        elif not r.has_entities():
            return recommend_main(nv)
        elif r.entity('confirm'):
            return recommend_main(nv)
        elif not r.entity('confirm') or r.entity('wrong_time'):
            return hangup_wrong_time(nv)
        elif r.entity('repeat'):
            return hello_repeat(nv)


def hello(nv):
    if_has_say(nv, 'hello')
    return hello_logic(nv, 0)


def hello_null(nv):
    if_has_say(nv, 'hello_null')
    return hello_logic(nv, 1)


def hello_repeat(nv):
    if_has_say(nv, 'hello_repeat')
    return hello_logic(nv, 0)


def main_logic(nv, counts):
    with nv.listen(
            'recommendation_score, recommendation, repeat, wrong_time, question',
            entities=['recommendation_score', 'recommendation', 'repeat', 'wrong_time', 'question'],
    ) as r:
        if r.utterance() == "" and counts[0] == 0:
            return recommend_null(nv)
        elif r.utterance() == "" and counts[0] == 1:
            return hangup_null(nv)
        elif not r.has_entities() and counts[1] == 0:
            return recommend_default(nv)
        elif not r.has_entities() and counts[1] == 1:
            return hangup_null(nv)
        elif r.entity('recommendation_score') in range(0, 9):
            return hangup_negative(nv)
        elif r.entity('recommendation_score') in [9, 10]:
            return hangup_positive(nv)
        elif r.entity('recommendation') == 'negative':
            return recommend_score_negative(nv)
        elif r.entity('recommendation') == 'neutral':
            return recommend_score_neutral(nv)
        elif r.entity('recommendation') == 'positive':
            return recommend_score_positive(nv)
        elif r.entity('recommendation') == 'dont_know':
            return recommend_repeat_2(nv)
        elif r.entity('repeat'):
            return recommend_repeat(nv)
        elif r.entity('wrong_time'):
            return hangup_wrong_time(nv)
        elif r.entity('question'):
            return forward(nv)


def recommend_main(nv):
    if_has_say(nv, 'recommend_main')
    return main_logic(nv, [0, 0])


def recommend_repeat(nv):
    if_has_say(nv, 'recommend_repeat')
    return main_logic(nv, [0, 0])


def recommend_repeat_2(nv):
    if_has_say(nv, 'recommend_repeat_2')
    return main_logic(nv, [0, 0])


def recommend_score_negative(nv):
    if_has_say(nv, 'recommend_score_negative')
    return main_logic(nv, [0, 0])


def recommend_score_neutral(nv):
    if_has_say(nv, 'recommend_score_neutral')
    return main_logic(nv, [0, 0])


def recommend_score_positive(nv):
    if_has_say(nv, 'recommend_score_positive')
    return main_logic(nv, [0, 0])


def recommend_null(nv):
    if_has_say(nv, 'recommend_null')
    return main_logic(nv, [1, 0])


def recommend_default(nv):
    if_has_say(nv, 'recommend_main')
    return main_logic(nv, [0, 1])


def hangup_positive(nv):
    if_has_say(nv, 'hangup_positive')
    tag = 'высокая оценка'
    return tag


def hangup_negative(nv):
    if_has_say(nv, 'hangup_negative')
    tag = 'низкая оценка'
    return tag


def hangup_wrong_time(nv):
    if_has_say(nv, 'hangup_wrong_time')
    tag = 'нет времени для разговора'
    return tag


def hangup_null(nv):
    if_has_say(nv, 'hangup_null')
    tag = 'проблемы с распознаванием'
    return tag


def forward(nv):
    if_has_say(nv, 'forward')
    tag = 'перевод на оператора'
    return tag


nn = NeuroNetLibrary(nlu_call, event_loop)
nn.call('8**********', '25-03-2020 01:00:00')
nv_global = NeuroVoiceLibrary(nlu_call, loop)
hello(nv_global)
