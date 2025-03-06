import random

# 테스트 리뷰 및 라벨 샘플 생성
test_reviews = [
    # 긍정적 리뷰 (라벨 1)
    {"review": "정말 맛있는 음식과 친절한 서비스로 완벽한 식사를 즐겼습니다.", "label": 1},
    {"review": "이 호텔은 정말 깨끗하고 스태프가 매우 친절했습니다.", "label": 1},
    {"review": "전체적으로 좋은 경험이었고 다시 방문하고 싶습니다.", "label": 1},
    {"review": "가격 대비 훌륭한 품질과 서비스를 제공합니다.", "label": 1},
    {"review": "매우 유용한 앱입니다. 사용하기 쉽고 디자인이 아름답습니다.", "label": 1},
    {"review": "최고의 제품입니다. 강력 추천합니다!", "label": 1},
    {"review": "이 영화는 정말 감동적이고 연출이 훌륭했습니다.", "label": 1},
    {"review": "배송이 빠르고 제품 상태도 완벽했습니다.", "label": 1},
    {"review": "직원들이 매우 도움이 되었고 문제를 신속하게 해결해 주었습니다.", "label": 1},
    {"review": "놀라운 기능과 성능을 갖춘 제품입니다.", "label": 1},
    {"review": "친절한 직원들과 쾌적한 환경이 인상적이었습니다.", "label": 1},
    {"review": "기대 이상으로 좋았고 가격도 합리적이었습니다.", "label": 1},
    {"review": "정말 즐거운 경험이었고 모든 것이 완벽했습니다.", "label": 1},
    {"review": "강력 추천! 최고의 서비스와 품질을 경험했습니다.", "label": 1},
    {"review": "모든 측면에서 만족스러웠고 기대 이상이었습니다.", "label": 1},
    
    # 부정적 리뷰 (라벨 0)
    {"review": "서비스가 너무 느리고 음식도 기대에 미치지 못했습니다.", "label": 0},
    {"review": "방이 더럽고 직원들은 불친절했습니다.", "label": 0},
    {"review": "가격이 너무 비싸고 품질은 형편없었습니다.", "label": 0},
    {"review": "시간 낭비였습니다. 다시는 방문하지 않을 것입니다.", "label": 0},
    {"review": "이 앱은 계속 충돌하고 사용자 인터페이스가 혼란스럽습니다.", "label": 0},
    {"review": "배송이 지연되었고 제품이 손상된 상태로 도착했습니다.", "label": 0},
    {"review": "스토리가 지루하고 연기가 형편없었습니다.", "label": 0},
    {"review": "제품이 설명과 완전히 다르고 품질이 매우 낮습니다.", "label": 0},
    {"review": "고객 서비스가 형편없고 문제 해결에 도움이 되지 않았습니다.", "label": 0},
    {"review": "많은 결함이 있고 전혀 작동하지 않습니다.", "label": 0},
    {"review": "실망스러운 경험이었고 돈을 낭비한 것 같습니다.", "label": 0},
    {"review": "제품 품질이 매우 낮고 내구성이 없습니다.", "label": 0},
    {"review": "최악의 서비스를 경험했습니다. 절대 추천하지 않습니다.", "label": 0},
    {"review": "기대 이하였으며 많은 불편함이 있었습니다.", "label": 0},
    {"review": "시간과 돈을 낭비한 느낌입니다. 매우 실망스럽습니다.", "label": 0},
    
    # 중립적/혼합 리뷰 (라벨은 컨텍스트에 따라 0 또는 1)
    {"review": "음식은 괜찮았지만 서비스가 좀 느렸습니다.", "label": 0},
    {"review": "위치는 좋았지만 방은 기대했던 것보다 작았습니다.", "label": 0},
    {"review": "몇 가지 장점이 있지만 개선이 필요한 부분도 많습니다.", "label": 0},
    {"review": "가격은 합리적이지만 품질은 평균 이하입니다.", "label": 0},
    {"review": "일부 기능은 유용하지만 전반적인 사용성이 떨어집니다.", "label": 0},
    {"review": "디자인은 좋지만 내구성이 부족합니다.", "label": 0},
    {"review": "연기는 훌륭했지만 스토리가 예측 가능했습니다.", "label": 1},
    {"review": "배송은 빨랐지만 포장이 부실했습니다.", "label": 0},
    {"review": "직원들은 친절했지만 문제 해결 능력이 부족했습니다.", "label": 0},
    {"review": "좋은 기능이 많지만 사용법이 복잡합니다.", "label": 1}
]

# 테스트 리뷰 데이터셋 생성
with open('test_review_dataset.txt', 'w', encoding='utf-8') as output_file:
    # 헤더 추가
    output_file.write("id\tsentence\tlabel\n")
    
    for i, review_data in enumerate(test_reviews):
        review_id = f"review_{i+1}"
        review_text = review_data["review"].replace('\t', ' ').replace('\n', ' ')
        label = review_data["label"]
        
        output_file.write(f"{review_id}\t{review_text}\t{label}\n")

print(f"테스트 리뷰 데이터셋이 test_review_dataset.txt 파일에 생성되었습니다.")
print(f"총 {len(test_reviews)}개의 리뷰가 포함되어 있습니다.")
