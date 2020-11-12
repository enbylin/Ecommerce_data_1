import pandas as pd
import datetime
from datetime import datetime

# 파일 읽기
order_df = pd.read_csv('./data/order_df_final.csv', encoding='utf-8-sig')
geo_df = pd.read_csv('./data/geo.csv', encoding='utf-8-sig')
mem_df = pd.read_csv('./data/member_final.csv', encoding='utf-8-sig')

# 날짜 형태 컬럼 데이터 타입 변경
order_df['주문날짜'] = pd.to_datetime(order_df['주문날짜'], format='%Y-%m-%d %H:%M:%S', errors='raise')
order_df['가입일'] = pd.to_datetime(order_df['가입일'], format='%Y-%m-%d %H:%M:%S', errors='raise')
mem_df['가입일'] = pd.to_datetime(mem_df['가입일'], format='%Y-%m-%d %H:%M:%S', errors='raise')

# 연도별 결제금액/결제횟수 DF 생성
year_sum_data = order_df.groupby(pd.Grouper(key='주문날짜', freq='Y'))['결제금액'].sum()
year_cnt_data = order_df.groupby(pd.Grouper(key='주문날짜', freq='Y'))['order_id'].count()
year_data = pd.merge(year_sum_data, year_cnt_data, how='left', on='주문날짜')
year_data.rename(columns={'결제금액': '매출액', 'order_id': '결제건수'}, inplace=True)
year_data = year_data.reset_index()
year_data['연도'] = year_data['주문날짜'].dt.year

# 월별 결제금액 DF 생성
month_sum_data = order_df.groupby(pd.Grouper(key='주문날짜', freq='M'))['결제금액'].sum()
month_sum_data = month_sum_data.reset_index()

# 분류/성별/결제방법/주소별 판매액 추이
year_sum_data = order_df.groupby([pd.Grouper(key='주문날짜', freq='Y'), '분류', '성별', '결제방법', '주소'])[['결제금액']].sum()
year_sum_data = year_sum_data.reset_index()
# year_sum_cate_data // 분류
year_sum_cate_data = year_sum_data[['주문날짜', '분류', '결제금액']].copy()
year_sum_cate_data = year_sum_cate_data.groupby(by=['주문날짜', '분류']).sum().reset_index()
year_sum_cate_data['연도'] = year_sum_cate_data['주문날짜'].dt.year
# year_sum_sex_data // 성별
year_sum_sex_data = year_sum_data[['주문날짜', '분류', '성별', '결제금액']]
year_sum_sex_data = year_sum_sex_data.groupby(by=['주문날짜', '분류', '성별']).sum().reset_index()
year_sum_sex_data['연도'] = year_sum_sex_data['주문날짜'].dt.year
# year_sum_payment_data // 결제방법
year_sum_payment_data = year_sum_data[['주문날짜', '분류', '결제방법', '결제금액']]
year_sum_payment_data = year_sum_payment_data.groupby(by=['주문날짜', '분류', '결제방법']).sum().reset_index()
year_sum_payment_data['연도'] = year_sum_payment_data['주문날짜'].dt.year
# year_sum_geo_data // 지역
year_sum_geo_data = year_sum_data[['주문날짜', '분류', '주소','결제금액']]
year_sum_geo_data = year_sum_geo_data.groupby(by=['주문날짜', '분류', '주소']).sum().reset_index()
year_sum_geo_data['연도'] = year_sum_geo_data['주문날짜'].dt.year
year_sum_geo_data = pd.merge(year_sum_geo_data, geo_df, how='left', left_on='주소', right_on='지역명')

# 요일/시간대별 결제건수
order_df_temp = order_df.copy()
order_df_temp['요일'] = order_df_temp['주문날짜'].dt.day_name()
order_df_temp['요일_숫자'] = order_df_temp['주문날짜'].dt.weekday
order_df_temp['주문시간'] = order_df_temp['주문날짜'].dt.hour
order_df_weekday_hour = order_df_temp.groupby(by=['요일', '주문시간', '요일_숫자'])['order_id'].count().reset_index()
order_df_weekday_hour = order_df_weekday_hour.rename(columns={'order_id': '결제건수'}).sort_values(by='요일_숫자', ascending=True)

# 많이 팔린 제품 TOP10 / 구매 많은 지역 TOP10 / 회원가입 추이
order_df_top10_sum = order_df.groupby(by='상품명')['결제금액'].sum()
order_df_top10_sum = order_df_top10_sum.reset_index()
order_df_top10_sum = order_df_top10_sum.sort_values(by='결제금액', ascending=False).head(10)
order_df_top10_cnt = order_df.groupby(by='주소')['order_id'].count()
order_df_top10_cnt = order_df_top10_cnt.reset_index()
order_df_top10_cnt = order_df_top10_cnt.rename(columns={'order_id': '결제건수'})
order_df_top10_cnt = order_df_top10_cnt.sort_values(by='결제건수', ascending=False).head(10)
mem_df = mem_df.groupby(pd.Grouper(key='가입일', freq='M')).count()
mem_df = mem_df.reset_index()
mem_df = mem_df.rename(columns={'아이디': '가입회원수'})
mem_df = mem_df[['가입일', '가입회원수']]


if __name__ == '__main__':
    pass
    # 파일 읽기
    # order_df = pd.read_csv('./data/order_df_final.csv', encoding='utf-8-sig')
    # geo_df = pd.read_csv('./data/geo.csv', encoding='utf-8-sig')
    # mem_df = pd.read_csv('./data/member_final.csv', encoding='utf-8-sig')

    # # 날짜 형태 컬럼 데이터 타입 변경
    # order_df['주문날짜'] = pd.to_datetime(order_df['주문날짜'], format='%Y-%m-%d %H:%M:%S', errors='raise')
    # order_df['가입일'] = pd.to_datetime(order_df['가입일'], format='%Y-%m-%d %H:%M:%S', errors='raise')
    # mem_df['가입일'] = pd.to_datetime(mem_df['가입일'], format='%Y-%m-%d %H:%M:%S', errors='raise')
