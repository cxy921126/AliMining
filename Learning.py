# coding=utf-8
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import svm
import numpy as np
import datetime

# df = pd.read_csv('/Users/cxy/Desktop/mars_tianchi_songs.csv', header=None)
# grouped = df.groupby(df.columns[1])


def count_songs():
    """统计每位歌手的歌曲数量"""
    counts = grouped.size()
    counts.to_csv('songs_count.csv')
    plt = counts.plot(kind='bar', color='g', title='Songs_count').get_figure()
    plt.savefig('songs_count.png')


def count_preliminay():
    """统计每位歌手的初始播放量总和"""
    counts = grouped[3].sum()
    counts.to_csv('preliminary.csv')
    plt = counts.plot(kind='bar', title='Preliminary').get_figure()
    plt.savefig('preliminary.png')
    print counts


def count_gender():
    """统计歌手性别"""
    gender_arr = grouped.first()[5].values
    m = 0.0
    f = 0.0
    band = 0.0
    for gender in gender_arr:
        if gender == 1:
            m += 1
        elif gender == 2:
            f += 1
        elif gender == 3:
            band += 1
    rate = [m/len(gender_arr), f/len(gender_arr), band/len(gender_arr)]
    pyplot.pie(rate, colors=['blue', 'red', 'yellow'], labels=['Male', 'Female', 'Band'],
               autopct='%1.1f%%')
    pyplot.title('Gender pie')
    pyplot.savefig('gender.png')


def time_count():
    """统计每名歌手的发布日期与歌曲数"""
    names = []
    times = []
    for a, b in grouped[2]:
        names.append(a)
        times.append(b)

    i = 0
    for time in times:
        c = time.groupby(time.values)
        dates = c.first().values
        counts = c.size().values
        print dates, counts
        pyplot.figure(i)
        pyplot.plot(dates, counts, '--go')
        pyplot.xticks(rotation=15)
        pyplot.ticklabel_format(style='plain', useOffset=False, scilimits=(7, 7))
        pyplot.title('%s' % names[i])
        pyplot.savefig('%s' % names[i])
        i += 1


def read_user():
    """统计每名歌手每天的播放量"""
    action_names = ['user_id', 'song_id', 'gmt_create', 'action_type', 'Ds']
    user_df = pd.read_csv('/Users/cxy/Desktop/mars_tianchi_user_actions.csv', header=None, names=action_names)
    song_names = ['song_id', 'artist_id', 'publish_time', 'song_init_plays', 'language', 'Gender']
    song_df = pd.read_csv('/Users/cxy/Desktop/mars_tianchi_songs.csv', header=None, names=song_names)

    total_df = pd.merge(user_df, song_df)
    artist = total_df.groupby('artist_id').artist_id.nunique()

    id = 0
    while id < 50:
        artist_data = total_df[(total_df['artist_id'] == artist.index[id])]
        start_date = datetime.datetime.strptime('20150301', '%Y%m%d')
        end_date = datetime.datetime.strptime('20150831', '%Y%m%d')
        step_day = datetime.timedelta(days=1)

        res_list = []
        while start_date != end_date:

            day_list = []
            day_data = artist_data[(artist_data['Ds']) == int(start_date.strftime('%Y%m%d'))]

            plays = len(day_data[day_data['action_type'] == 1])
            downs = len(day_data[day_data['action_type'] == 2])
            favors = len(day_data[day_data['action_type'] == 3])

            # day_list.append(plays)
            # day_list.append(downs)
            # day_list.append(favors)
            day_list.append(plays)
            day_list.append(start_date.strftime('%Y%m%d'))

            res_list.append(day_list)
            start_date += step_day

        day_plays = pd.DataFrame(res_list)
        day_plays.to_csv(artist.index[id]+'.csv', header=None, Index=None)
        print artist.index[id]
        print day_plays
        id += 1

read_user()

