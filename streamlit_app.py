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
    video_data_dic = video_data.to_dict(orient='records')
    st.write(video_data)

    st.subheader('動画の再生数')
    col1, col2, col3 = st.columns(3)
    col1.metric("最大", video_data['statistics.viewCount'].max())
    col2.metric("最小", video_data['statistics.viewCount'].min())
    col3.metric("平均", video_data['statistics.viewCount'].mean())

    st.subheader('月別の再生数')
    chart_data = video_data[['date', 'month', 'snippet.title','statistics.viewCount','statistics.likeCount','statistics.commentCount']]
    st.bar_chart(chart_data, x="month", y=['statistics.viewCount','statistics.likeCount'])

    st.subheader('動画のデータ')
    st.dataframe(video_data[['snippet.thumbnails.medium.url','snippet.title','video_url','snippet.description']],
        column_config={
            'snippet.thumbnails.medium.url':st.column_config.ImageColumn('thumbnails'),
            'snippet.title':'title',
            'video_url':st.column_config.LinkColumn('URL'),
            'snippet.description':'description'
        }
    )