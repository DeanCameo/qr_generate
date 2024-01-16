from django.contrib import messages
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
import qrcode
import io
import base64
from PIL import Image
from django.views.decorators.csrf import csrf_protect


def home(request):
    return render(request, 'gimics/home.html')

@csrf_protect
def qr_code_view(request):
    if request.method == 'GET':
        return render(request, 'gimics/generator.html')
    elif request.method == 'POST' and 'generator' in request.POST:
        qr_input = request.POST.get('qr_input', '').strip()
        qr_image = request.FILES.get('qr_image')
        qr_color = request.POST.get('qr_color', '').strip()
        qr_logo = request.FILES.get('qr_logo')

        if not qr_input and not qr_image:
            messages.error(request, "Please enter text or upload an image to generate a QR code.")
            return render(request, 'gimics/generator.html')

        if qr_image:
            filename = default_storage.save(qr_image.name, qr_image)
            qr_image_path = default_storage.path(filename)
            img = qrcode.make(qr_image_path)
        else:
            qr_data = qr_input if qr_input.startswith(('http://', 'https://')) else qr_input.encode()
            img = qrcode.make(qr_data)

        if qr_color:
            img = img.convert("RGB")
            qr_color = tuple(int(qr_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
            data = img.getdata()
            new_data = [qr_color if item[:3] == (0, 0, 0) else item for item in data]
            img.putdata(new_data)

        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        qr_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return render(request, 'gimics/generator_result.html', {'qr_image_base64': qr_image_base64, 'qr_color': qr_color, 'qr_logo': qr_logo})
    
    return render(request, 'gimics/generator.html')
