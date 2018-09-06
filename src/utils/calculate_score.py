from kivy.app import App
import re
import math

app = App.get_running_app()

'''
e.g. qst_ans = { 00000001 : ['A', '10.0'], ... }
'''
def result(qst_ans):

    tmp = {}

    for key in app.dictIDName.keys():
        if key in qst_ans.keys():
            if qst_ans[key][0] == app.QUESTIONS[app.SEC_CNT][app.QST_PAR_CNT]['OK']:
                right = True
                time = qst_ans[key][1]
            elif qst_ans[key][0] == None:
                right = None
                time = None
                if app.SECTIONS[app.SEC_CNT]['type'] != 'test':
                    app.ABSTENTIONS[key] += 1
            else:
                right = False
                time = qst_ans[key][1]
        else:
            right = None
            time = None
            if app.SECTIONS[app.SEC_CNT]['type'] != 'test':
                app.ABSTENTIONS[key] += 1

        ast = app.ABSTENTIONS[key]

        result = score_law(right, time, ast)
        tmp[key] = [result, time]

        # updating also general score
        if app.SECTIONS[app.SEC_CNT]['type'] != 'test':
            app.GENERAL_SCORE[key] += result

    print app.ABSTENTIONS

    app.QUESTION_SCORE.append(tmp)
    return tmp

def update_score(result, option='ans'):

    ans = {'R': 0, 'A': 0, 'W':0}
    RAWdic = {}

    for key in result.keys():

        if result[key][0] > 0:
            ans['R'] += 1
            RAWdic[str(key)] = 'R'
        if result[key][0] == 0:
            ans['A'] += 1
            RAWdic[str(key)] = 'A'
        if result[key][0] < 0:
            ans['W'] += 1
            RAWdic[str(key)] = 'W'

    if option == 'ans':
        return ans
    elif option == 'RAWdic':
        return RAWdic

#return a dictionary {ID: [char, time], ...}
def DictOfAnswers():

    dizionario = {}

#    start_time = int(app.times[0])
    start_time = app.start_time
    print(start_time)
#    stop_time = int(app.times[-1])
    stop_time = app.stop_time
    print(stop_time)

    app.start_time = None
    app.stop_time = None

    for key in app.saved_ans.keys():
        if key > start_time:
            dt = (key - start_time)*pow(10,-6)
        else:
            dt = (4294967296 - start_time + key)*pow(10,-6)
        ID = app.saved_ans[key][0]
        if dizionario.has_key(ID) and dizionario[ID][1] < dt:
            pass
        else:
            dizionario[ID] = [app.saved_ans[key][1], dt]

    return dizionario

#return a dictionary {ID: [char, time], ...}
def DictOfAnswers_fake():
    dizionario = {}
    dizionario['2142880870'] = ['A',2.0]
    dizionario['3893145282'] = ['B',3.0]
    dizionario['2142879773'] = ['C'',4.0]
    dizionario['3893136493'] = ['D',5.0]
    dizionario['3893146321'] = ['E',7.0]
    return dizionario


#score_law: bool right, float time, int ast
def score_law(right, time, ast):
    if (ast > 5 and (time > app.TOTAL_TIME or time is None)):
        return -200
    else:
        if (time > app.TOTAL_TIME or time is None):
            return 0
        else:
            a = 300-math.sqrt((12500.0/3)*time)
            return int(a) if right else int(-(2.0/3)*a)
