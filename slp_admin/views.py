from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect

from SLP.settings import EMAIL_HOST_USER
from slp_admin.models import *


# Create your views here.

def dashboard(request):
    return render(request, 'slp_admin/dashboard.html')


def merchant(request, id):
    merchant_detail = Merchant.objects.get(id=id)
    products_detail = Product.objects.filter(merchant_id=merchant_detail.id)


    context = {'merchant_detail': merchant_detail,'products_detail':products_detail }

    return render(request, 'slp_admin/merchant.html', context)


def add_merchant(request):
    if request.method == 'POST':
        merchant_name = request.POST['merchant_name']
        merchant_email = request.POST['merchant_email']
        merchant_phone_number = request.POST['merchant_phone_number']
        merchant = Merchant(name=merchant_name, email=merchant_email, phone=merchant_phone_number)

        # token = default_token_generator.make_token(merchant.name)
        # uid = urlsafe_base64_encode(force_bytes(merchant.pk))
        # print(token)

        import string
        import random
        import urllib.parse
        letters = string.digits + string.ascii_letters
        code = ''.join([random.choice(letters) for i in range(10)])
        params = {'token': code}

        letters = string.digits + string.ascii_letters
        code = ''.join([random.choice(letters) for i in range(10)])
        params = {'token': code}

        token = ResetToken(token=code, email=merchant_email)
        token.save()

        if not ResetToken.objects.filter(token=token.token):
            print("not found")
        else:
            message = 'http://127.0.0.1:8000/merchant/reset_password?' + urllib.parse.urlencode(params)

            print("already reset")
        # message = 'http://127.0.0.1:8000/merchant/reset_password'+str(Merchant.objects.get(email = merchant_email).id)+"/"

        subject = "This mail for reset password just Click Below link to reset password Thank you for using our services parasdabhi2021@gmail.com"

        send_mail(subject, message, EMAIL_HOST_USER, [merchant_email], fail_silently=False)

        merchant.save()
        return redirect('view_merchant')
    else:
        return render(request, 'slp_admin/add_merchant.html')


def view_merchant(request):
    # merchant_list = Product.objects.select_related('merchant')

    merchant_list = Merchant.objects.annotate(num_of_products=models.Count('product')).filter(is_deleted="False")
    context = {
        'merchant_list': merchant_list,

    }
    return render(request, 'slp_admin/view_merchant.html', context)


def delete_merchant(request, id):
    Merchant.objects.filter(id=id).update(is_deleted="True")
    return redirect('view_merchant')


def merchant_status(request):
    """Update merchant status like Block/ Unblock"""
    status = request.POST['status']
    merchant_id = request.POST['id']
    if request.method == 'POST':
        status = request.POST['status']
        merchant_id = request.POST['id']

        if status == 'Unblock':
            merchant_update = Merchant.objects.filter(id=merchant_id).update(status='Block')
            merchant = Merchant.objects.get(id=merchant_id)
            return HttpResponse({'status': merchant.status})
        else:
            merchant_update = Merchant.objects.filter(id=merchant_id).update(status='Unblock')
            merchant = Merchant.objects.get(id=merchant_id)
            return HttpResponse({'status': merchant.status})


def add_products(request):
    if request.method == 'POST':

        techncal_file_count = int(request.POST['technical_uploaded_file_count'])
        technical_file_list = []
        for tech_count in range(techncal_file_count):
            techcou = str(tech_count)
            tech_file = request.FILES.get('technical_datasheet_' + techcou + '')

            if tech_file is None:
                continue
                techfileobj = TechnicalFiles.objects.create(
                    technical_data_sheet=request.FILES.get('technical_datasheet_' + techcou + '')
                )
                technical_file_list.append(techfileobj)
            else:
                techfileobj = TechnicalFiles.objects.create(
                    technical_data_sheet=request.FILES.get('technical_datasheet_' + techcou + '')
                )
                technical_file_list.append(techfileobj)

        guideline_file_count = int(request.POST['guidelines_uploaded_file_count'])
        guideline_file_list = []
        for guide_count in range(guideline_file_count):
            guidecou = str(guide_count)
            guide_file = request.FILES.get('application_guidelines_' + guidecou + '')

            if guide_file is None:
                continue
                guidefileobj = TechnicalFiles.objects.create(
                    application_guidelines=request.FILES.get('application_guidelines_' + guidecou + '')
                )
                guideline_file_list.append(guidefileobj)
            else:
                guidefileobj = AppilicationGuideLineFiles.objects.create(
                    application_guidelines=request.FILES.get('application_guidelines_' + guidecou + '')
                )
                guideline_file_list.append(guidefileobj)

        video_file_count = int(request.POST['video_uploaded_file_count'])
        video_file_list = []
        for video_count in range(video_file_count):
            videocou = str(video_count)
            video_file = request.FILES.get('videofile_' + videocou + '')

            if video_file is None:
                continue
                videofileobj = VideoFiles.objects.create(
                    video=request.FILES.get('videofile_' + videocou + '')
                )
                video_file_list.append(videofileobj)
            else:
                videofileobj = VideoFiles.objects.create(
                    video=request.FILES.get('videofile_' + videocou + '')
                )
                video_file_list.append(videofileobj)

        safety_file_count = int(request.POST['safety_datasheet_uploaded_file_count'])
        safety_file_list = []
        for safety_count in range(safety_file_count):
            safetycou = str(safety_count)
            safety_file = request.FILES.get('safety_datasheet_file_' + safetycou + '')

            if safety_file is None:
                continue
                safetyfileobj = SafetyFiles.objects.create(
                    safety_data_sheet=request.FILES.get('safety_datasheet_file_' + safetycou + '')
                )
                safety_file_list.append(safetyfileobj)
            else:
                safetyfileobj = SafetyFiles.objects.create(
                    safety_data_sheet=request.FILES.get('safety_datasheet_file_' + safetycou + '')
                )
                safety_file_list.append(safetyfileobj)

        certificate_file_count = int(request.POST['certificate_file_count'])
        certificate_file_list = []
        for certificate_count in range(certificate_file_count):
            certificatecou = str(certificate_count)
            certificate_file = request.FILES.get('certificate_file_' + certificatecou + '')

            if certificate_file is None:
                continue
                certificatefileobj = Certificate.objects.create(
                    certificate=request.FILES.get('certificate_file_' + certificatecou + '')
                )
                certificate_file_list.append(certificatefileobj)
            else:
                certificatefileobj = Certificate.objects.create(
                    certificate=request.FILES.get('certificate_file_' + certificatecou + '')
                )
                certificate_file_list.append(certificatefileobj)

        # Product model fields
        merchant_id = request.POST['merchant_id']
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        product_image = request.FILES.get('product_image')
        # print("product image is ",product_image)

        # ProductActivationDetail model fields
        a_side_batch = request.POST['a_side_batch']
        b_side_set_temp = request.POST['b_side_set_temp']
        a_side_set_temp = request.POST['a_side_set_temp']
        hot_set_temp = request.POST['hot_set_temp']
        mixing_chamber_size = request.POST['mixing_chamber_size']
        pressure_set = request.POST['pressure_set']
        starting_drum_temperature = request.POST['starting_drum_temperature']

        # ArrayModelField all model

        qr_code_scan_reward = request.POST['qr_code_scan_reward']
        a_side_batch_reward = request.POST['a_side_batch_reward']
        a_side_set_temp_reward = request.POST['a_side_set_temp_reward']
        b_side_set_temp_reward = request.POST['b_side_set_temp_reward']
        hot_set_temp_reward = request.POST['hot_set_temp_reward']
        pressure_set_reward = request.POST['pressure_set_reward']
        mixing_chamber_size_reward = request.POST['mixing_chamber_size_reward']
        photo_of_install_foam_reward = request.POST['photo_of_install_foam_reward']
        starting_drum_temperature_point_reward = request.POST['starting_drum_temperature_point_reward']
        total_point = request.POST['total_points']
        product = Product(merchant_id=merchant_id, product_name=product_name,
                          product_description=product_description,
                          product_image=product_image, Technical_file=technical_file_list,
                          application_guidelines=guideline_file_list,
                          video=video_file_list,
                          safety_data_sheet=safety_file_list,
                          certificate=certificate_file_list,
                          a_side_batch=a_side_batch,
                          a_side_set_temp=a_side_set_temp,
                          b_side_set_temp=b_side_set_temp,
                          hot_set_temp=hot_set_temp,
                          mixing_chamber_size=mixing_chamber_size,
                          pressure_set=pressure_set,
                          starting_drum_temperature=starting_drum_temperature,
                          qr_code_scan_reward=qr_code_scan_reward,
                          a_side_batch_reward=a_side_batch_reward,
                          a_side_set_temp_reward=a_side_set_temp_reward,
                          b_side_set_temp_reward=b_side_set_temp_reward,
                          hot_set_temp_reward=hot_set_temp_reward,
                          pressure_set_reward=pressure_set_reward,
                          mixing_chamber_size_reward=mixing_chamber_size_reward,
                          photo_of_install_foam_reward=photo_of_install_foam_reward,
                          starting_drum_temperature_point_reward=starting_drum_temperature_point_reward,
                          total_point=total_point,
                          )

        product.save()

        merchant_list = Merchant.objects.all()
        context = {'merchant_list': merchant_list}
        return render(request, 'slp_admin/add-products.html', context)

    else:
        merchant_list = Merchant.objects.all()
        context = {'merchant_list': merchant_list}
        return render(request, 'slp_admin/add-products.html', context)


def products(request):
    product_list = Product.objects.select_related('merchant').filter(merchant__is_deleted=False, is_deleted=False)
    print(product_list)
    context = {'product_list': product_list}
    return render(request, 'slp_admin/products.html', context)


def view_products(request, id):
    if request.method == 'GET':
        product_detail = Product.objects.select_related('merchant').get(pk=id)

        return render(request, 'slp_admin/view-products.html', {'product_detail': product_detail})


def delete_product(request, id):
    Product.objects.filter(id=id).update(is_deleted="True")
    return redirect('products')


def edit_product(request, id):
    if request.method == 'GET':
        numbers = []
        mixing_chamber_size = []
        pressure_set = []
        starting_drum_temperature = []
        for i in range(100, 150):
            numbers.append(i)
        for i in range(0, 4):
            mixing_chamber_size.append(i)
        for i in range(900, 1500, 25):
            pressure_set.append(i)
        for i in range(40, 120):
            starting_drum_temperature.append(i)

        product_detail = Product.objects.get(id=id)
        merchant_list = Merchant.objects.all()
        merchant_name = []
        for merchanob in merchant_list:
            merchant_name.append(merchanob)
        count = 0
        context = {
            'product_detail': product_detail,
            'numbers': numbers,
            'mixing_chamber_size': mixing_chamber_size,
            'pressure_set': pressure_set,
            'count': count,
            'starting_drum_temperature': starting_drum_temperature,
            'merchant_list': merchant_list,
            'merchant_name': merchant_name,
        }
        return render(request, 'slp_admin/edit-product.html', context)
    if request.method == 'POST':

        techncal_file_count = int(request.POST['technical_uploaded_file_count'])
        technical_file_list = []
        product_data = Product.objects.get(id=id)
        previous_tech_data = product_data.Technical_file
        for techobj in previous_tech_data:
            technical_file_list.append(techobj)
        for tech_count in range(techncal_file_count):
            techcou = str(tech_count)
            tech_file = request.FILES.get('technical_datasheet_' + techcou + '')

            if tech_file is None:
                continue
                techfileobj = TechnicalFiles.objects.create(
                    technical_data_sheet=request.FILES.get('technical_datasheet_' + techcou + '')
                )
                technical_file_list.append(techfileobj)
            else:
                techfileobj = TechnicalFiles.objects.create(
                    technical_data_sheet=request.FILES.get('technical_datasheet_' + techcou + '')
                )
                technical_file_list.append(techfileobj)

        guideline_file_count = int(request.POST['guidelines_uploaded_file_count'])
        guideline_file_list = []
        previous_guide_data = product_data.application_guidelines
        for guideobj in previous_guide_data:
            guideline_file_list.append(guideobj)
        for guide_count in range(guideline_file_count):
            guidecou = str(guide_count)
            guide_file = request.FILES.get('application_guidelines_' + guidecou + '')

            if guide_file is None:
                continue
                guidefileobj = TechnicalFiles.objects.create(
                    application_guidelines=request.FILES.get('application_guidelines_' + guidecou + '')
                )
                guideline_file_list.append(guidefileobj)
            else:
                guidefileobj = AppilicationGuideLineFiles.objects.create(
                    application_guidelines=request.FILES.get('application_guidelines_' + guidecou + '')
                )
                guideline_file_list.append(guidefileobj)

        video_file_count = int(request.POST['video_uploaded_file_count'])
        video_file_list = []
        previous_video_data = product_data.video
        for vidobj in previous_video_data:
            video_file_list.append(vidobj)
        for video_count in range(video_file_count):
            videocou = str(video_count)
            video_file = request.FILES.get('videofile_' + videocou + '')

            if video_file is None:
                continue
                videofileobj = VideoFiles.objects.create(
                    video=request.FILES.get('videofile_' + videocou + '')
                )
                video_file_list.append(videofileobj)
            else:
                videofileobj = VideoFiles.objects.create(
                    video=request.FILES.get('videofile_' + videocou + '')
                )
                video_file_list.append(videofileobj)

        safety_file_count = int(request.POST['safety_datasheet_uploaded_file_count'])
        safety_file_list = []
        previous_safety_data = product_data.safety_data_sheet
        for safetyobj in previous_safety_data:
            safety_file_list.append(safetyobj)
        for safety_count in range(safety_file_count):
            safetycou = str(safety_count)
            safety_file = request.FILES.get('safety_datasheet_file_' + safetycou + '')

            if safety_file is None:
                continue
                safetyfileobj = SafetyFiles.objects.create(
                    safety_data_sheet=request.FILES.get('safety_datasheet_file_' + safetycou + '')
                )
                safety_file_list.append(safetyfileobj)
            else:
                safetyfileobj = SafetyFiles.objects.create(
                    safety_data_sheet=request.FILES.get('safety_datasheet_file_' + safetycou + '')
                )
                safety_file_list.append(safetyfileobj)

        certificate_file_count = int(request.POST['certificate_file_count'])
        certificate_file_list = []
        previous_certificate_data = product_data.certificate
        for certiobj in previous_certificate_data:
            certificate_file_list.append(certiobj)
        for certificate_count in range(certificate_file_count):
            certificatecou = str(certificate_count)
            certificate_file = request.FILES.get('certificate_file_' + certificatecou + '')
            if certificate_file is None:
                continue
                certificatefileobj = Certificate.objects.create(
                    certificate=request.FILES.get('certificate_file_' + certificatecou + '')
                )
                certificate_file_list.append(certificatefileobj)
            else:
                certificatefileobj = Certificate.objects.create(
                    certificate=request.FILES.get('certificate_file_' + certificatecou + '')
                )
                certificate_file_list.append(certificatefileobj)

        # Product model fields
        merchant_id = request.POST['merchant_id']
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        product_image = request.FILES.get('product_image')
        # print("product image is ",product_image)

        # ProductActivationDetail model fields
        a_side_batch = request.POST['a_side_batch']
        b_side_set_temp = request.POST['b_side_set_temp']
        a_side_set_temp = request.POST['a_side_set_temp']
        hot_set_temp = request.POST['hot_set_temp']
        mixing_chamber_size = request.POST['mixing_chamber_size']
        pressure_set = request.POST['pressure_set']
        starting_drum_temperature = request.POST['starting_drum_temperature']

        # ArrayModelField all model

        qr_code_scan_reward = request.POST['qr_code_scan_reward']
        a_side_batch_reward = request.POST['a_side_batch_reward']
        a_side_set_temp_reward = request.POST['a_side_set_temp_reward']
        b_side_set_temp_reward = request.POST['b_side_set_temp_reward']
        hot_set_temp_reward = request.POST['hot_set_temp_reward']
        pressure_set_reward = request.POST['pressure_set_reward']
        mixing_chamber_size_reward = request.POST['mixing_chamber_size_reward']
        photo_of_install_foam_reward = request.POST['photo_of_install_foam_reward']
        starting_drum_temperature_point_reward = request.POST['starting_drum_temperature_point_reward']
        total_point = request.POST.get('total_points')
        print("Total point is ", total_point)

        product = Product.objects.filter(id=id).update(merchant_id=merchant_id, product_name=product_name,
                                                       product_description=product_description,
                                                       product_image=product_image,
                                                       Technical_file=technical_file_list,
                                                       application_guidelines=guideline_file_list,
                                                       video=video_file_list,
                                                       safety_data_sheet=safety_file_list,
                                                       certificate=certificate_file_list,
                                                       a_side_batch=a_side_batch,
                                                       a_side_set_temp=a_side_set_temp,
                                                       b_side_set_temp=b_side_set_temp,
                                                       hot_set_temp=hot_set_temp,
                                                       mixing_chamber_size=mixing_chamber_size,
                                                       pressure_set=pressure_set,
                                                       starting_drum_temperature=starting_drum_temperature,
                                                       qr_code_scan_reward=qr_code_scan_reward,
                                                       a_side_batch_reward=a_side_batch_reward,
                                                       a_side_set_temp_reward=a_side_set_temp_reward,
                                                       b_side_set_temp_reward=b_side_set_temp_reward,
                                                       hot_set_temp_reward=hot_set_temp_reward,
                                                       pressure_set_reward=pressure_set_reward,
                                                       mixing_chamber_size_reward=mixing_chamber_size_reward,
                                                       photo_of_install_foam_reward=photo_of_install_foam_reward,
                                                       starting_drum_temperature_point_reward=starting_drum_temperature_point_reward,
                                                       total_point=total_point,
                                                       )
        return redirect('products')


def edit_product_tech_file(request):
    if request.method == 'POST':
        tech_id = request.POST.get('tech_file_id')
        product_id = request.POST.get('product_id')
        tech_detail = TechnicalFiles.objects.get(tech_file_id=tech_id)
        productObj = Product.objects.get(id=product_id)
        techfileObj = productObj.Technical_file
        for obj in techfileObj:
            if int(tech_id) == obj.tech_file_id:
                productObj.Technical_file.pop(techfileObj.index(obj))
                print("success delete")
        productObj.save()
        tech_detail.delete()
        return HttpResponse({'messgae': 'Deleted'})


def edit_product_guide_file(request):
    if request.method == 'POST':
        guide_file_id = request.POST.get('guide_file_id')
        product_id = request.POST.get('product_id')
        guide_detail = AppilicationGuideLineFiles.objects.get(app_guide_file_id=guide_file_id)
        print("guide_detail", guide_detail)
        productObj1 = Product.objects.get(id=product_id)
        guidefileObj = productObj1.application_guidelines
        for obj in guidefileObj:
            if int(guide_file_id) == obj.app_guide_file_id:
                productObj1.application_guidelines.pop(guidefileObj.index(obj))
        productObj1.save()
        guide_detail.delete()
    return HttpResponse({'messgae': 'Deleted'})


def edit_product_video_file(request):
    if request.method == 'POST':
        video_file_id = request.POST.get('video_file_id')
        product_id = request.POST.get('product_id')
        video_detail = VideoFiles.objects.get(video_file_id=video_file_id)
        print("guide_detail", video_detail)
        productObj1 = Product.objects.get(id=product_id)
        videofileObj = productObj1.video
        for obj in videofileObj:
            if int(video_file_id) == obj.video_file_id:
                productObj1.video.pop(videofileObj.index(obj))
        productObj1.save()
        video_detail.delete()
    return HttpResponse({'messgae': 'Deleted'})


def edit_product_safety_file(request):
    if request.method == 'POST':
        safety_file_id = request.POST.get('safety_file_id')
        product_id = request.POST.get('product_id')
        safety_detail = SafetyFiles.objects.get(safety_file_id=safety_file_id)
        print("safety_detail", safety_detail)
        productObj1 = Product.objects.get(id=product_id)
        safetyfileObj = productObj1.safety_data_sheet
        for obj in safetyfileObj:
            if int(safety_file_id) == obj.safety_file_id:
                productObj1.safety_data_sheet.pop(safetyfileObj.index(obj))
        productObj1.save()
        safety_detail.delete()
    return HttpResponse({'messgae': 'Deleted'})


def edit_product_certificate_file(request):
    if request.method == 'POST':
        certificate_file_id = request.POST.get('certificate_file_id')
        product_id = request.POST.get('product_id')
        certificate_detail = Certificate.objects.get(certificate_id=certificate_file_id)
        print("safety_detail", certificate_detail)
        productObj1 = Product.objects.get(id=product_id)
        certificatefileObj = productObj1.certificate
        for obj in certificatefileObj:
            if int(certificate_file_id) == obj.certificate_id:
                productObj1.certificate.pop(certificatefileObj.index(obj))
        productObj1.save()
        certificate_detail.delete()
    return HttpResponse({'messgae': 'Deleted'})
