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
    analyses = analyses.order_by('-id')
    page = Paginator(analyses, 10)
    params = {
        'analyses': page.get_page(num),
    }
    return render(request, "analysis/top.html", params)


@require_http_methods(["GET", "POST", "HEAD"])
def analysis_new(request):
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():

            # jsonを返す模擬APIの処理

            # 現在時刻のUNIX時間（エポック秒）を取得
            request_timestamp = int(time.time())
            # POSTされた値を取得
            post_value = request.POST.get('image_path')

            # image_pathの値が画像の拡張子('.jpg', '.png')を含むかチェックし、各値をセット
            if re.compile(".jpg|.png").search(post_value):
                success = True
                message = 'success'
                class_num = random.randint(1, 9)
                confidence = round(random.random(), 4)
                pre_json = {
                    'success': success,
                    'message': message,
                    'estimated_data': {
                        'class': class_num,
                        'confidence': confidence,
                    }
                }
            else:
                success = False
                message = 'Error:E50012'
                class_num = 9999
                confidence = 0
                pre_json = {
                    'success': success,
                    'message': message,
                    'estimated_data': {}
                }
            # jsonに変換
            result_json = json.dumps(pre_json)

            # 現在時刻のUNIX時間（エポック秒）を取得
            response_timestamp = int(time.time())

            # モデルオブジェクトに値をセット
            analysis = Analysis(
                image_path=post_value,
                success=success,
                message=message,
                class_num=class_num,
                confidence=confidence,
                request_timestamp=request_timestamp,
                response_timestamp=response_timestamp,
            )
            # DBに保存
            analysis.save()

            # jsonを返す
            return HttpResponse(result_json)
    else:
        form = AnalysisForm()
    return render(request, "analysis/analysis_new.html", {'form': form})


def analysis_detail(request, analysis_id):
    analysis = get_object_or_404(Analysis, pk=analysis_id)
    return render(request, 'analysis/analysis_detail.html', {'analysis': analysis})


def analysis_delete(request, analysis_id):
    analysis = get_object_or_404(Analysis, pk=analysis_id)
    if request.method == 'POST':
        analysis.delete()
        return redirect(to='top')
    params = {
        'title': 'Hello',
        'id': analysis_id,
        'analysis': analysis,
    }
    return render(request, 'analysis/analysis_delete.html', params)
