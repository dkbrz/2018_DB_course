WORK = {'INFO' : ['SELECT tests.* FROM tests WHERE {} ORDER BY discipline, c_date, id_test',
       {'id_test':'tests.id_test = {}', 't_name':'tests.t_name = \"{}\"', 'discipline':'tests.discipline = \"{}\"',
       'c_date':'tests.c_date = \"{}\"'},
                 ['<b>ID теста</b>','<b>Дисциплина</b>','<b>Название теста</b>','<b>Задание</b>']],

        'RESULTS': ['SELECT tests.discipline, tests.t_name, tests.c_date, results.mark, students.s_name, students.s_course, students.s_degree, students.s_program FROM students, results, tests WHERE results.id_test=tests.id_test AND results.id_student = students.id_student AND {} ORDER BY tests.discipline, tests.c_date, tests.id_test, students.s_degree, students.s_course, students.s_name',
        {'id_test':'tests.id_test = {}', 't_name':'tests.t_name = \"{}\"', 'discipline':'tests.discipline = \"{}\"','c_date':'tests.c_date = \"{}\"'},
                   ['<b>Дисциплина</b>','<b>Название</b>','<b>Дата проведения</b>','<b>Оценка</b>','<b>Имя</b>','<b>Курс</b>','<b>Степень</b>','<b>Программа</b>']]}

STUDENT = {'INFO' : ['SELECT DISTINCT students.* FROM students WHERE {} ORDER BY students.s_program, students.s_degree, students.s_course, students.s_name',
       {'id_student':'students.id_student = {}','s_course':'students.s_course = {}','s_name':'students.s_name = \"{}\"','s_program':'students.s_program = \"{}\"','s_degree':'students.s_degree = \"{}\"'},
                    ['<b>ID</b>','<b>Фамилия, имя</b>','<b>Курс</b>','<b>Степень</b>','<b>Программа</b>']],

        'RESULTS': ['SELECT DISTINCT tests.id_test, tests.discipline, tests.t_name, tests.c_date, results.mark FROM tests, students, results WHERE results.id_student=students.id_student AND results.id_test=tests.id_test AND {} ORDER BY tests.discipline, tests.c_date',
        {'id_student':'students.id_student = {}','s_course':'students.s_course = {}','s_name':'students.s_name = \"{}\"','s_program':'students.s_program = \"{}\"','s_degree':'students.s_degree = \"{}\"'},
                   ['<b>ID теста</b>','<b>Дисциплина</b>','<b>Название</b>','<b>Дата</b>','<b>Оценка</b>']]}

ADD = {'STUDENT':'INSERT INTO students (s_name, s_course, s_degree, s_program) VALUES (\"{}\", {}, \"{}\",\"{}\")',
       'TEST' :'INSERT INTO tests (discipline, task_text, t_name, c_date) VALUES (\"{}\", \"{}\", \"{}\",\"{}\")',
       'RESULTS':'INSERT INTO results (id_student, id_test, mark) VALUES ({},{},{})'}

