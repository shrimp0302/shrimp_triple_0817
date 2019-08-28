from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import cv2
from django.conf import settings
from detection import google_vision_api
from wordtest import getSynonym

def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        print("request:", request.method)
        form = DocumentForm()
        max_id = Document.objects.latest('id').id
        obj = Document.objects.get(id = max_id)
        input_path = settings.BASE_DIR + obj.photo.url
        output_path = settings.BASE_DIR + "/media/output/output.jpg"
        gray(input_path,output_path)
        label = google_vision_api(output_path)
        print("labels:", label)
        description = obj.description
        synonym = getSynonym(description)

    return render(request, 'blog/post_list.html', {
        'form': form,
        'obj':obj,
        'labels': label,
        'synonym': synonym,
    })


###########ここをカスタマイズ############

def gray(input_path,output_path):
    img = cv2.imread(input_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, img_gray)

######################################