from django.contrib import admin

from .models import Topic
from .forms import TopicAdminForm

class TopicAdmin(admin.ModelAdmin):

    #textareaを表示させるフォームクラスを指定。
    form            = TopicAdminForm

    #表示するフィールド
    list_display    = [ "id","title","comment","dt" ]


    #検索対象のフィールド指定
    search_fields   = [ "title","comment" ]

    #日付ごとに絞り込む、ドリルナビゲーションの設置
    date_hierarchy      = "dt"


    #1ページ当たりに表示する件数、全件表示を許容する最大件数(ローカルでも5000件を超えた辺りから遅くなるので、10000~50000辺りが無難)
    list_per_page       = 1000
    list_max_show_all   = 20000

admin.site.register(Topic,TopicAdmin)

