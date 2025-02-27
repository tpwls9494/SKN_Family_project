# # 2. from-import 구문 사용
# # our_class.py 모듈을 가져와서
# from our_class import teacher_name, student_count
# from our_class import study, lecture, go_lunch

# # 선생님의 이름과 학생 수를 출력하고
# print(teacher_name, student_count)

# # study() 함수와 lecture() 함수를 호출하고
# study(), lecture()

# # 먹고 싶은 메뉴명이 5개 담긴 menus 배열을 만들어
# many_menus = ['김밥', '유부초밥', '샌드위치', '오리고기', '불고기']

# # go_lunch() 함수를 호출해 오늘의 점심 메뉴를 출력해 봅시다.
# print(go_lunch(many_menus))

######################################################################

# 3. 패키지 내의 모듈 import
# our_class.py 모듈을 가져와서

import our_class_dir.official.official_module as of
from our_class_dir.unofficial.unofficial_module import study, go_lunch

# 선생님의 이름과 학생 수를 출력하고
print(of.teacher_name, of.student_count)

# study() 함수와 lecture() 함수를 호출하고
study(), of.lecture()

# 먹고 싶은 메뉴명이 5개 담긴 menus 배열을 만들어
many_menus = ['김밥', '유부초밥', '샌드위치', '오리고기', '불고기']

# go_lunch() 함수를 호출해 오늘의 점심 메뉴를 출력해 봅시다.
print(go_lunch(many_menus))



