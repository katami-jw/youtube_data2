import streamlit as st
import pandas as pd

st.title("Youtubeチャンネル調査")
st.write("気になるYouTubeチャンネルのチャンネルIDを入力してチャンネルの情報を見てみましょう")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    video_data = pd.read_csv(uploaded_file,encoding="Shift-JIS")
    video_data['date'] = pd.to_datetime(video_data['snippet.publishedAt']).dt.date
    video_data['month'] = pd.to_datetime(video_data['snippet.publishedAt']).dt.to_period('M').dt.start_time
    video_data['video_url'] = 'https://www.youtube.com/watch?v='+video_data['id.videoId']
    video_data=video_data.rename(columns={'statistics.viewCount': 'view_count'})
    video_data_dic = video_data.to_dict(orient='records')
    st.write(video_data)

    #サイドメニュー設定
    st.sidebar.write('フィルター設定')
    date_start = st.sidebar.date_input('開始日',value=video_data['date'].min(), min_value=video_data['date'].min())
    date_end = st.sidebar.date_input('終了日')
    view_min = st.sidebar.number_input('再生数下限',step=100)

    #フィルター後のデータ
    data = video_data.query('@date_end >= date >= @date_start & view_count > @view_min')

    #基本データ
    st.subheader('動画の再生数')
    col1, col2, col3 = st.columns(3)
    col1.metric("最大", data['view_count'].max())
    col2.metric("最小", data['view_count'].min())
    col3.metric("平均", data['view_count'].mean())

    #月別のグラフ
    st.subheader('月別の再生数')
    chart_data = data[['date', 'month', 'snippet.title','view_count','statistics.likeCount','statistics.commentCount']]
    st.bar_chart(chart_data, x="month", y=['view_count','statistics.likeCount'])

    #一覧
    st.subheader('動画のデータ')
    st.dataframe(data[['snippet.thumbnails.medium.url','snippet.title','video_url','snippet.description']],
        column_config={
            'snippet.thumbnails.medium.url':st.column_config.ImageColumn('thumbnails'),
            'snippet.title':'title',
            'video_url':st.column_config.LinkColumn('URL'),
            'snippet.description':'description'
        }
    )
