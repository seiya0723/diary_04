from django import forms

from .models import Topic

class TopicForm(forms.ModelForm):

    class Meta:
        model   = Topic
        fields  = [ "title","comment" ]



#Adminで使う専用のフォームクラス
class TopicAdminForm(forms.ModelForm):

    #admin.pyで使うcommentのフォームをtextareaタグにする
    #https://stackoverflow.com/questions/430592/django-admin-charfield-as-textarea
    #https://docs.djangoproject.com/en/3.2/ref/forms/widgets/

    #maxlength属性がない、そこでフィールドオプションmax_lengthから参照を行い、属性値を割り当てる。ラベルもverbose_nameを参照する。
    #comment     = forms.CharField(widget=forms.Textarea)

    comment     = forms.CharField(  widget  = forms.Textarea( attrs={ "maxlength":str(Topic.comment.field.max_length), } ),
                                    label   = Topic.comment.field.verbose_name 
                                    )

    class Meta:
        model   = Topic
        fields  = [ "title","comment","dt" ] #←dtを追加して管理画面からでは日付を指定できるようにする。このフィールドの順番がadminに関わってくるので注意




#モデルを継承しないフォームクラス
class YearMonthForm(forms.Form):
    year    = forms.IntegerField()
    month   = forms.IntegerField()
