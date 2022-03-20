import json
import time
import random
import glob
from django.core.paginator import Paginator
from django.views.decorators.http import require_safe, require_http_methods
from django.shortcuts import render, redirect, get_object_or_404

from .models import Analysis
from .forms import ImagePathForm, UploadImageForm


@require_safe
def top(request, num=1):
    analyses = Analysis.objects.all()
    analyses = analyses.order_by('id').reverse()
    page = Paginator(analyses, 5)
    params = {
        'analyses': page.get_page(num),
    }
    return render(request, "analysis/top.html", params)


@require_http_methods(["GET", "POST", "HEAD"])
def analysis_new(request):

    # 画像パスの一覧を取得しフォームにセット
    choices = get_image_list()
    image_path_form = ImagePathForm()
    image_path_form.fields['image_path'].choices = choices

    # POST時の処理
    if request.method == 'POST':

        # POSTでimage_pathが送られた時の処理
        if request.POST.get('image_path'):

            # POSTされたimage_pathの値を取得
            image_path = request.POST.get('image_path').strip()

            # 現在時刻のUNIX時間（エポック秒）を取得
            request_timestamp = int(time.time())

            # 模擬API呼び出し
            response_json = analysis_api(image_path)

            # 現在時刻のUNIX時間（エポック秒）を取得
            response_timestamp = int(time.time())

            # APIから返ってきたjsonからDBに保存する値を取得
            response_json = json.loads(response_json)
            success = response_json['success']
            message = response_json['message']
            if response_json['estimated_data']:
                class_num = response_json['estimated_data']['class']
                confidence = response_json['estimated_data']['confidence']
            else:
                class_num = None
                confidence = None

            # モデルオブジェクトに値をセット
            analysis = Analysis(
                image_path=image_path,
                success=success,
                message=message,
                class_num=class_num,
                confidence=confidence,
                request_timestamp=request_timestamp,
                response_timestamp=response_timestamp,
            )

            # DBに保存
            analysis.save()

            context = {
                'analysis': analysis,
                'response_json': response_json,
            }

            return render(request, 'analysis/analysis_result.html', context)

        # ファイルがアップロードされた時の処理
        if request.FILES:
            upload_image_form = UploadImageForm(request.POST, request.FILES)

            filename_save = upload_image_form.save()

            # 画像パスの一覧を取得しフォームにセット
            choices = get_image_list()
            image_path_form = ImagePathForm()
            image_path_form.fields['image_path'].choices = choices

            context = {
                'image_path_form': image_path_form,
                'upload_image_form': upload_image_form,
                'filename_save': filename_save,
            }

            return render(request, 'analysis/analysis_new.html', context)

    upload_image_form = UploadImageForm()
    context = {
        'image_path_form': image_path_form,
        'upload_image_form': upload_image_form,
    }
    return render(request, 'analysis/analysis_new.html', context)


def analysis_api(image_path):
    # 成功失敗を判定し、結果に応じて値をセット
    success = random.choice([True, False])

    if success == True:
        message = 'success'
        class_num = random.randint(1, 9)
        confidence = round(random.random(), 4)
        estimated_data = {
            'class': class_num,
            'confidence': confidence,
        }
    else:
        message = 'Error:E50012'
        estimated_data = {}

    pre_json = {
        'success': success,
        'message': message,
        'estimated_data': estimated_data,
    }
    # jsonに変換
    result_json = json.dumps(pre_json)
    # jsonを返す
    return result_json


def get_image_list():
    # 画像ファイルの一覧を取得
    files = glob.glob('./image/*')

    # 画像パスの一覧をHTMLで使用できる形（tuple）に整形
    image_list = []
    for file in files:
        image_list.append(file)
    choices = []
    choices.append(['', '-- ファイルのパスを選択してください --'])
    for path in image_list:
        choice = [path, path]
        choices.append(choice)
    choices = tuple(choices)
    return choices


def analysis_detail(request, analysis_id):
    analysis = get_object_or_404(Analysis, pk=analysis_id)
    return render(request, 'analysis/analysis_detail.html', {'analysis': analysis})


def analysis_delete(request, analysis_id):
    analysis = get_object_or_404(Analysis, pk=analysis_id)
    if request.method == 'POST':
        analysis.delete()
        return redirect(to='top')
    params = {
        'id': analysis_id,
        'analysis': analysis,
    }
    return render(request, 'analysis/analysis_delete.html', params)
