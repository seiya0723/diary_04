from django.shortcuts import render,redirect
from django.views import View

from .models import Topic
from .forms import TopicForm,YearMonthForm

import datetime 


class BbsView(View):

    def get(self, request, *args, **kwargs):

        form    = YearMonthForm(request.GET)

        #フォームクラスを使用してバリデーションをすることで、数値以外のyearとmonthが指定された場合、未指定の場合はバリデーションNGとなり、elseに行く。
        if form.is_valid():

            #バリデーション済みのデータは.clean()で出力できる。
            cleaned_data    = form.clean()


            print(cleaned_data["month"])
            print(cleaned_data["year"])

            topics  = Topic.objects.filter(dt__year=cleaned_data["year"],dt__month=cleaned_data["month"]).order_by("dt")
            dt      = datetime.date(cleaned_data["year"],cleaned_data["month"],1) #←.clean()でバリデーションされたデータはすでに数値型になっているので変換不要

        else:

            dt      = datetime.datetime.now()
            dt      = dt.replace(day=1)

            topics  = Topic.objects.filter(dt__year=dt.year,dt__month=dt.month).order_by("dt")


        #来月と先月のリンクを作る(timedeltaでmonthを加算することはできない。別途ライブラリを使うか、下記のように計算する。)
        #https://stackoverflow.com/questions/546321/how-do-i-calculate-the-date-six-months-from-the-current-date-using-the-datetime
        if dt.month == 12:
            #来月の計算はyearを1追加、monthを1にする。先月はそのまま1減らす。
            next_month  = "?year=" + str(dt.year + 1) + "&month=" + str(1)
            prev_month  = "?year=" + str(dt.year) + "&month=" + str(dt.month -1)

        elif dt.month == 1:
            #先月の計算はyearを1減らす、monthを12にする。来月はそのまま1追加。
            next_month  = "?year=" + str(dt.year) + "&month=" + str(dt.month + 1)
            prev_month  = "?year=" + str(dt.year - 1) + "&month=" + str(12)

        else:
            #来月、先月それぞれ1追加、1減らすだけでいい
            next_month  = "?year=" + str(dt.year) + "&month=" + str(dt.month + 1)
            prev_month  = "?year=" + str(dt.year) + "&month=" + str(dt.month - 1)


        #topicsの中にある日付のリストを作る
        topic_dts   = []
        for topic in topics:
            topic_dts.append(str(topic.dt.year) + str(topic.dt.month) + str(topic.dt.day))

        print(topic_dts)

        year        = dt.year
        month       = dt.month
        days        = []
        weekdays    = []

        #.weekday()で数値化した曜日が出力される(月曜日が0、日曜日が6)
        #一ヶ月の最初が日曜日であればそのまま追加、それ以外の曜日であれば、曜日の数値に1追加した数だけ空文字を追加
        if dt.weekday() != 6:
            for i in range(dt.weekday()+1):
                weekdays.append("")

        #1日ずつ追加して月が変わったらループ終了
        while month == dt.month:
            dic = { "num":"","id":"" }

            #カレンダーの日付に投稿した日記がある場合、idに年月日の文字列型をセットする。(このidがリンクになる)
            for topic_dt in topic_dts:
                str_dt  = str(year) + str(month) + str(dt.day)
                if topic_dt == str_dt:
                    dic["id"]   = str_dt
                    break

            dic["num"]  = dt.day

            weekdays.append(dic)

            dt  = dt + datetime.timedelta(days=1)
            if dt.weekday() == 6:
                days.append(weekdays)
                weekdays    = []

        if dt.weekday() != 6:
            days.append(weekdays)
            weekdays    = []

        print(days)

        """
        [ ['  ', '  ', '1 ', '2 ', '3 ', '4 ', '5 '],
          ['6 ', '7 ', '8 ', '9 ', '10', '11', '12'],
          ['13', '14', '15', '16', '17', '18', '19'],
          ['20', '21', '22', '23', '24', '25', '26'],
          ['27', '28', '29', '30']
          ]
        """

        """
        [['', '', '', '', {'num': 1, 'id': ''}, {'num': 2, 'id': ''}, {'num': 3, 'id': ''}],
         [{'num': 4, 'id': '202174'}, {'num': 5, 'id': ''}, {'num': 6, 'id': ''}, {'num': 7, 'id': ''}, {'num': 8, 'id': ''}, {'num': 9, 'id': ''}, {'num': 10, 'id': ''}],
         [{'num': 11, 'id': ''}, {'num': 12, 'id': ''}, {'num': 13, 'id': ''}, {'num': 14, 'id': ''}, {'num': 15, 'id': ''}, {'num': 16, 'id': ''}, {'num': 17, 'id': ''}],
         [{'num': 18, 'id': ''}, {'num': 19, 'id': ''}, {'num': 20, 'id': ''}, {'num': 21, 'id': ''}, {'num': 22, 'id': ''}, {'num': 23, 'id': ''}, {'num': 24, 'id': ''}],
         [{'num': 25, 'id': ''}, {'num': 26, 'id': ''}, {'num': 27, 'id': ''}, {'num': 28, 'id': ''}, {'num': 29, 'id': ''}, {'num': 30, 'id': ''}, {'num': 31, 'id': ''}]
         ]

        """


        #最新と最古の記事を検索し、現在選択されている年と比較。カレンダーの年のプルダウンメニューの配列を作る
        newest  = Topic.objects.all().order_by("-dt").first()
        oldest  = Topic.objects.all().order_by("dt").first()

        year_list  = []

        if newest and oldest:
            #投稿したことがある

            if year < oldest.dt.year:
                #セレクトされている年は最古の記事より古い
                
                for i in range(year,newest.dt.year+1):
                    year_list.append(i)

            elif newest.dt.year < year:
                #セレクトされている年は最新の記事より新しい

                for i in range(oldest.dt.year,year+1):
                    year_list.append(i)

            else:
                #セレクトされている年は投稿データの範囲内

                for i in range(oldest.dt.year,newest.dt.year+1):
                    year_list.append(i)

        else:
            #未投稿
            year_list.append(year)

        print("カレンダーのプルダウンメニューに表示する年のリスト")
        print(year_list)


        context = { "topics":topics,
                    "days":days,
                    "year":year,
                    "month":month,
                    "next_month":next_month,
                    "prev_month":prev_month,
                    "year_list":year_list,
                }

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        form    = TopicForm(request.POST)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")

        return redirect("bbs:index")



index   = BbsView.as_view()

