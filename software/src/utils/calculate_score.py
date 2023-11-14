from kivy.app import App
import re
import math
import operator

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
        app.GENERAL_SCORE[key] += result

        # if special section, collecting result in sct score
        if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
            app.SECTION_SCORE[app.SEC_CNT][key] += result

    app.QUESTION_SCORE.append(tmp)

    app.do_backup()

    #print classifica domanda a terminale
    Score_R_quest_term = [(key, app.QUESTION_SCORE[-1][key][0], app.QUESTION_SCORE[-1][key][1]) for key in app.QUESTION_SCORE[-1].keys() if app.QUESTION_SCORE[-1][key][0] > 0]
    Score_A_quest_term = [(key, app.QUESTION_SCORE[-1][key][0], app.QUESTION_SCORE[-1][key][1]) for key in app.QUESTION_SCORE[-1].keys() if app.QUESTION_SCORE[-1][key][0] == 0]
    Score_W_quest_term = [(key, app.QUESTION_SCORE[-1][key][0], app.QUESTION_SCORE[-1][key][1]) for key in app.QUESTION_SCORE[-1].keys() if app.QUESTION_SCORE[-1][key][0] < 0]
    sorted_R_quest_term = sorted(Score_R_quest_term, key=operator.itemgetter(2))
    sorted_R_quest_term = sorted(sorted_R_quest_term, key=operator.itemgetter(1), reverse= True)
    sorted_W_quest_term = sorted(Score_W_quest_term, key=operator.itemgetter(2), reverse=True)
    sorted_W_quest_term = sorted(sorted_W_quest_term, key=operator.itemgetter(1), reverse= True)
    sorted_x_quest_term = sorted_R_quest_term+Score_A_quest_term+sorted_W_quest_term

    print("\033[1;97m\033[1;100m")
    print("CLASSIFICA DOMANDA -----------------------------")
    print("                                RIS    TEM")
    for i in range(len(sorted_x_quest_term)):
        spacer = " "
        if sorted_x_quest_term[i][1] > 0:
            spacer += "\033[1;92m"
            spacer_2 = " "
            if sorted_x_quest_term[i][1] < 100:
                spacer_2 += " "
            if sorted_x_quest_term[i][1] < 10:
                spacer_2 += " "
        elif sorted_x_quest_term[i][1] == 0:
            spacer += "\033[1;93m"
            spacer_2 = " "
            if sorted_x_quest_term[i][1] < 100:
                spacer_2 += " "
            if sorted_x_quest_term[i][1] < 10:
                spacer_2 += " "
        else:
            spacer += "\033[1;91m"
            spacer_2 = ""
            if sorted_x_quest_term[i][1] > -100:
                spacer_2 += " "
            if sorted_x_quest_term[i][1] > -10:
                spacer_2 += " "

        try:
            answer_quest = qst_ans[sorted_x_quest_term[i][0]][0]

            if qst_ans[sorted_x_quest_term[i][0]][1] < 10:
                time_quest = "  "
            else:
                time_quest = " "

            time_quest += "%.2f" % round(qst_ans[sorted_x_quest_term[i][0]][1],2)
        except:
            answer_quest = "-"
            time_quest = "   -"

        separator = ''
        for k in range(26-len(app.dictIDName[sorted_x_quest_term[i][0]].decode('utf-8'))):
            separator += ' '

        print(spacer + spacer_2 + str(sorted_x_quest_term[i][1]) + "\033[1;97m " + str(app.dictIDName[sorted_x_quest_term[i][0]])+ separator + spacer + str(answer_quest) + "   " + str(time_quest))
    print("\033[0m\n")

    #print classifica sezione a terminale
    if app.SECTIONS[app.SEC_CNT]['type'] == 'special':
        Score_sect_term = [(key, app.SECTION_SCORE[app.SEC_CNT][key]) for key in app.SECTION_SCORE[app.SEC_CNT].keys()]
        sorted_x_sect_term = sorted(Score_sect_term, key=operator.itemgetter(1), reverse= True)
        print("\033[1;97m\033[1;100m")
        print("CLASSIFICA SEZIONE -----------------------------\n")
        for i in range(len(sorted_x_sect_term)):
            spacer = "\033[1;95m"
            if sorted_x_sect_term[i][1] >= 0:
                if sorted_x_sect_term[i][1] < 10000:
                    spacer += " "
                if sorted_x_sect_term[i][1] < 1000:
                    spacer += " "
                if sorted_x_sect_term[i][1] < 100:
                    spacer += " "
                if sorted_x_sect_term[i][1] < 10:
                    spacer += " "
            else:
                if sorted_x_sect_term[i][1] > -1000:
                    spacer += " "
                if sorted_x_sect_term[i][1] > -100:
                    spacer += " "
                if sorted_x_sect_term[i][1] > -10:
                    spacer += " "
            print(spacer + str(sorted_x_sect_term[i][1]) + "\033[1;97m " + str(app.dictIDName[sorted_x_sect_term[i][0]]))
        print("\033[0m\n")


    #print classifica generale a terminale
    Score_term = [(key, app.GENERAL_SCORE[key]) for key in app.GENERAL_SCORE.keys()]
    sorted_x_term = sorted(Score_term, key=operator.itemgetter(1), reverse= True)
    print("\033[1;97m\033[1;100m")
    print("CLASSIFICA GENERALE ----------------------------")
    print("                                AST     BAT")
    for i in range(len(sorted_x_term)):
        spacer = "\033[1;96m"
        if sorted_x_term[i][1] >= 0:
            if sorted_x_term[i][1] < 10000:
                spacer += " "
            if sorted_x_term[i][1] < 1000:
                spacer += " "
            if sorted_x_term[i][1] < 100:
                spacer += " "
            if sorted_x_term[i][1] < 10:
                spacer += " "
        else:
            if sorted_x_term[i][1] > -1000:
                spacer += " "
            if sorted_x_term[i][1] > -100:
                spacer += " "
            if sorted_x_term[i][1] > -10:
                spacer += " "
        if app.ABSTENTIONS[sorted_x_term[i][0]] < 5:
            spacer_ast = "\033[1;92m"
        elif app.ABSTENTIONS[sorted_x_term[i][0]] == 5:
            spacer_ast = "\033[1;93m"
        else:
            spacer_ast = "\033[1;91m"
        if app.ABSTENTIONS[sorted_x_term[i][0]] < 10:
            spacer_ast += " "

        if app.BATTERY_STATUS[sorted_x_term[i][0]] >= 200:
            battery_level = int(app.BATTERY_STATUS[sorted_x_term[i][0]]) - 200
            is_charging = True
        else:
            battery_level = app.BATTERY_STATUS[sorted_x_term[i][0]]
            is_charging = False

        if battery_level == 100:
            batStr = "\033[1;94m" + str(battery_level)
        elif battery_level >= 50:
            batStr = "\033[1;92m " + str(battery_level)
        elif battery_level >= 20:
            batStr = "\033[1;93m " + str(battery_level)
        elif battery_level >= 10:
            batStr = "\033[1;91m " + str(battery_level)
        elif is_charging:
            batStr = "\033[1;91m  " + str(battery_level)
        elif battery_level >= 0:
            batStr = "\033[1;91m\033[5m  " + str(battery_level)
        else:
            batStr = "\033[38;5;238mN/A"

        if is_charging:
            batStr += u"\u26a1"

        separator = ''
        for k in range(26-len(app.dictIDName[sorted_x_term[i][0]].decode('utf-8'))):
            separator += ' '

        print(spacer + str(sorted_x_term[i][1]) + "\033[1;97m " + str(app.dictIDName[sorted_x_term[i][0]]) + separator + spacer_ast + str(app.ABSTENTIONS[sorted_x_term[i][0]]) + "\t" + batStr + "\033[25m")
    print("\033[0m\n")

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
#    stop_time = int(app.times[-1])
    stop_time = app.stop_time

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
        elif key <= stop_time or (key - start_time < app.QUESTION_TOTAL_TIME*pow(10,6) and key - start_time > 0):
            dizionario[ID] = [app.saved_ans[key][1], dt]

    return dizionario

#return a dictionary {ID: [char, time], ...}
def DictOfAnswers_fake():
    dizionario = {}
    #dizionario['2142880870'] = ['A',2.0]
    #dizionario['3893145282'] = ['B',3.0]
    #dizionario['2142879773'] = ['C',4.0]
    #dizionario['3893136493'] = ['D',5.0]
    #dizionario['3893146321'] = ['E',7.0]
    return dizionario


#score_law: bool right, float time, int ast
def score_law(right, time, ast):
    if (ast > 5 and (time > app.QUESTION_TOTAL_TIME or time is None)):
        return -200
    else:
        # first check if tim is Name to avoid TypeError:
        # if the first proposition of an or is already True 
        # the second is not calculated because the or will be True
        if (time is None or time > app.QUESTION_TOTAL_TIME):
            return 0
        else:
            a = 300-math.sqrt((12500.0/3)*time/app.QUESTION_TOTAL_TIME*15)
            return int(a) if right else int(-(2.0/3)*a)
