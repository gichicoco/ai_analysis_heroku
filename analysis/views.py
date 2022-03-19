import re
import json
import time
import random
from django.core.paginator import Paginator
from django.views.decorators.http import require_safe, require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import Analysis
from .forms import AnalysisForm


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
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():

            # 現在時刻のUNIX時間（エポック秒）を取得
            request_timestamp = int(time.time())
            # POSTされたimage_pathの値を取得
            image_path = request.POST.get('image_path')
            image_path = image_path.strip()

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

            params = {
                'analysis': analysis,
                'response_json': response_json,
            }

            return render(request, 'analysis/analysis_result.html', params)

    else:
        form = AnalysisForm()
    return render(request, "analysis/analysis_new.html", {'form': form})


def analysis_api(image_path):
    # 入力をチェックし、変数に値をセット
    if (image_path.endswith('.jpg') or image_path.endswith('.png')) \
            and not image_path.startswith('.') \
            and not re.compile('.+[\s].+').search(image_path):
        success = True
        message = 'success'
        class_num = random.randint(1, 9)
        confidence = round(random.random(), 4)
        estimated_data = {
            'class': class_num,
            'confidence': confidence,
        }
    else:
        success = False
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
