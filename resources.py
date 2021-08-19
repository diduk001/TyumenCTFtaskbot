class Resources:
    COMMANDS_LIST = ['/register', '/admin', '/help']
    ADMIN_PASS = (open("admin_pass.txt", "r")).readlines()[0][0:-1]
    ADMIN_SUCCESS = 'О привет киберпидорский админ'
    ADMIN_FAILURE = 'Увы, пороль неверный (лох)'
    START_MSG = "Добрый вечер, я диспетчер. Зарегистрируйтесь!"
    NAME = "Введите своё киберимя"
    SURNAME = "Введите свою киберфамилию"
    MAIL = "Введите своё кибермыло"
    MAIL_INVALID = "Твоё кибермыло киберинвалидно"
    NICKNAME = "Введите своё киберник"
    CITY = "Введите свой кибергород"
    AGE = "Введите свой кибервозраст"
    GRADE = "Введите свой киберкласс"
    SCHOOL = "Введите свою кибершколу"
    REGISTRATION_COMPLETE = "Спасибо за регистрацию!"
    ALR_REGISTERED = "Вы уже зарегистрированы, для просмотра всех компанд напишите /help"
