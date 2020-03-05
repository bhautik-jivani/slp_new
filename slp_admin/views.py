from django.shortcuts import render, redirect
from . import models, forms
from django.shortcuts import render,HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect
from passlib.hash import pbkdf2_sha256

from django.core.mail import send_mail
from SLP.settings import EMAIL_HOST_USER

from slp_admin.models import *
import jwt,json
import string
import random
import urllib.parse

from django.core.mail import EmailMultiAlternatives , EmailMessage
from rest_framework.decorators import api_view
from rest_framework.response import Response

def add_video(request):
    if request.method == "POST":
        category = request.POST['category_id']
        title = request.POST['title']
        video = request.FILES.get('video')
        description = request.POST['description']
        video = models.Video(category_id=category, title=title, description=description, video=video)
        video.save()
        return redirect('videos')
    else:
        category = models.Category.objects.all()
        context = {
            "categories": category
        }
        return render(request, "add-videos.html", context)


def edit_video(request, video_id):
    if request.method == "POST":
        video1 = models.Video.objects.filter(id=video_id)
        category = request.POST['category_id']
        title = request.POST['title']
        # video = request.FILES.get('video')
        description = request.POST['description']
        cat = models.Category.objects.get(id=category)
        video1.update(title=title, category=cat, description=description)
        return redirect('videos')
    else:
        video = models.Video.objects.get(id=video_id)
        category = models.Category.objects.all()
        context = {
            "categories": category,
            "videos": video
        }
        return render(request, "edit-videos.html", context)


def delete_video(request, video_id):
    video = models.Video.objects.get(id=video_id)
    video.delete()
    return redirect('videos')


def videos(request):
    video = models.Video.objects.all()
    context = {
        "videos": video
    }
    return render(request, "videos.html", context)


def category(request):
    if request.method == "POST":
        category = request.POST['category']
        category_new = models.Category(name=category)
        category_new.save()
        return redirect('category')
    else:
        category = models.Category.objects.all()
        context = {
            "categories": category
        }
        return render(request, "videos-categories.html", context)


def delete_category(request, category_id):
    category = models.Category.objects.get(id=category_id)
    category.delete()
    return redirect('category')


def dashboard(request):
    return render(request, "admin_dashboard.html", {})


def contractor_list(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        context = {
                    'message': "Session Expired!",
                    'url': '/slp_admin/login/',
                    'icon': 'error',
                }
        return render(request , "admin_login.html" , context)

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token = admin_session)
        admin_info = SlpAdmin.objects.get(id = admin_token.admin.id)
        print(request.build_absolute_uri().rsplit("/",3)[0])
        contractors = Contractor.objects.all()
        return render(request, 'contractors.html', {'contractors':contractors,"name" : admin_info.first_name})
    

    if request.method == 'POST':
        contractor_name = request.POST['name']
        contractor_email = request.POST['email']
        contractor_contact = request.POST['contact']
        contractor_company = request.POST['company_name']
        
        # Create Token
        letters = string.digits + string.ascii_letters
        code = ''.join([random.choice(letters) for i in range(10)])
        params = {'token': code}

        try:
            contra = Contractor.objects.get(email = contractor_email)
            data = {"title":'Try again', "message":'Email already exist', "icon":'warning','url':'/slp_admin/contractors/'}
            return render(request, 'contractors.html', data)
        except ObjectDoesNotExist:
            try:
                contra = Contractor.objects.get(email = contractor_email)
                data = {"title":'Try again', "message":'Email already exist', "icon":'warning','url':'/slp_admin/contractors/'}
                return render(request, 'contractors.html', data)
            except ObjectDoesNotExist:
                try:
                    contra = Contractor.objects.get(contact = contractor_contact)
                    data = {"title":'Try again', "message":'Contact number already exist', "icon":'warning','url':'/slp_admin/contractors/'}
                    return render(request, 'contractors.html', data)
                except ObjectDoesNotExist:
                        contra = Contractor.objects.create(
                            name = contractor_name,
                            email = contractor_email,
                            contact = contractor_contact,
                            company_name = contractor_company,
                        )
                        contra.save()
                        
                        # Add token and mail in ResetToken Model
                        
                        token = ResetToken(token=code, email=contractor_email)
                        token.save()

                        absolute_url = request.build_absolute_uri().rsplit("/",3)[0]
                        message = absolute_url+'/contractor/set_password?' + urllib.parse.urlencode(params)
                        subject = "This mail for set a password just Click Below link to set a password Thank you for using our services demotestmail007@gmail.com"
                        
                        send_mail(subject, message, EMAIL_HOST_USER, [contractor_email], fail_silently=False)

                        data = {"title":'Contractor added successfully', "message":'Please check mail for set password...', "icon":'success'}
                        return render(request, 'contractors.html', data)

# Contractor Details
def contractor_dtl(request, contraId):
    try:
        admin_session = request.session['Admintoken']
    except:
        context = {
                    'message': "Session Expired!",
                    'url': '/slp_admin/login/',
                    'icon': 'error',
                }
        return render(request , "admin_login.html" , context)
    admin_token = AdminToken.objects.get(token = admin_session)
    admin_info = SlpAdmin.objects.get(id = admin_token.admin.id)
    contra = Contractor.objects.get(id = contraId)
    users = SlpUser.objects.filter(company = contra.company_name)
    return render(request, 'contractor-profile.html', {'contra':contra, 'users':users, "name" : admin_info.first_name})

# Points Requests
def points_request(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        context = {
                    'message': "Session Expired!",
                    'url': '/slp_admin/login/',
                    'icon': 'error',
                }
        return render(request , "admin_login.html" , context)

    if request.method == 'GET':
        admin_token = AdminToken.objects.get(token = admin_session)
        admin_info = SlpAdmin.objects.get(id = admin_token.admin.id)
        add_points = AdditionalPointRequest.objects.all()
        choices = AdditionalPointRequest._meta.get_field('action').choices
        defaultChoices = dict((x,y) for x,y in choices)
        return render(request, 'points-request.html',{'add_points':add_points,'defaultChoices':defaultChoices,"name" : admin_info.first_name})
    if request.method == 'POST':
        try:
            print("\n",request.POST)
            addpointsId = request.POST['addpoint_id']
            print("\nAdditional id",addpointsId)
            pointsaction = request.POST['points_action']
            
            add_points = AdditionalPointRequest.objects.get(id = addpointsId)
            add_points.action = pointsaction
            
            print('\nPoints action',pointsaction == 'Resolved')
            add_points.save()
            if pointsaction == 'Resolved':
                user = SlpUser.objects.get(id = add_points.user.id)
                user.total_points += add_points.additional_points
                user.available_points += add_points.additional_points
                user.save()
                print("\nAvailabel points: ",user.available_points)
            # return redirect('/slp_admin/points-request/')
            data = {"icon": "success", "title":"Done", "message": "Action applied successfully...",'url':'/slp_admin/points-request/'}
            return HttpResponse(json.dumps(data), content_type='application/json')
            
        except ObjectDoesNotExist:
            return redirect('/slp_admin/points-request/')

@api_view(['GET'])
def dashboard(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        context = {
                    'message': "Session Expired!",
                    'url': '/slp_admin/login/',
                    'icon': 'error',
                }
        return render(request , "admin_login.html" , context)
    if request.method == "GET":
        admin_token = AdminToken.objects.get(token = admin_session)
        admin_info = SlpAdmin.objects.get(id = admin_token.admin.id)
        try:
            user_count = SlpUser.objects.all()
            print("count " , user_count.count())
            dashboar_list = {"user_count" : user_count.count() ,
            "merchant_count" : 0,
            "videos_count" : 0,
            "products_count" : 0,
            "banner_count" : 0
            }
        except:
            print("SlpUser model Empty")
            user_count = 0
        
        try:
            merchant_count = Merchant.objects.all()
            dashboar_list = {"user_count" : user_count.count() ,
            "merchant_count" : merchant_count.count(),
            "videos_count" : 0,
            "products_count" : 0,
            "banner_count" : 0
            }
        except:
            print("Merchant model Empty")
            merchant_count = 0

        try:
            video_count = Video.objects.all()
            dashboar_list = {"user_count" : user_count.count() ,
            "merchant_count" : merchant_count.count(),
            "videos_count" : video_count.count(),
            "products_count" : 0,
            "banner_count" : 0
            }
        except:
            print("Video model Empty")
            video_count = 0

        try:
            product_count = Product.objects.all()
            dashboar_list = {"user_count" : user_count.count() ,
            "merchant_count" : merchant_count.count(),
            "videos_count" : video_count.count(),
            "products_count" : product_count.count(),
            "banner_count" : 0
            }
        except:
            print("Product model Empty")
            product_count = 0

        try:
            banner_count = Banner.objects.all()
            dashboar_list = {"user_count" : user_count.count() ,
            "merchant_count" : merchant_count.count(),
            "videos_count" : video_count.count(),
            "products_count" : product_count.count(),
            "banner_count" : banner_count.count()
            }
        except:
            print("Banner model Empty")
            banner_count = 0

        context = {"count" : dashboar_list , "name" : admin_info.first_name}
        return render(request , "admin_dashboard.html" , context )

        
@api_view(['POST' , 'GET'])
def change_password(request):
    verify_token = request.session['Admintoken']
    # return render(request , "admin_login.html" , {"context" : "Session Expired"})
    print("token" , verify_token)
    try:
        admin = AdminToken.objects.get(token = verify_token)
    except:
        context = {
                    'message': "Invalid token or Account not found!",
                    'url': '/slp_admin/login/',
                    'icon': 'error',
                }
        return render(request , "admin_edit-profile.html" , context)
    try:
        admin_info = SlpAdmin.objects.get(id = admin.admin.id)
    except:
        context = {
                    'message': "Admin account not found!",
                    'url': '/slp_admin/login/',
                    'icon': 'error',
                }
        return render(request , "admin_login.html" , context)

    if request.method =='GET':
        context = {"name" : admin_info.first_name}
        return render(request , "admin_edit-profile.html" , context)

    if request.method == 'POST':
       
        password = request.POST['password']
        old_passwrd = request.POST['old_pass']
        confrm_password = request.POST['cnfm_pass']

        try:
            SlpAdmin.objects.get(password = old_passwrd)
        except:
            context = {"message" : "Password Incorrect" , 
            'icon': 'error',
            "password" : password , 
            "old_passwrd" : old_passwrd , 
            "name" : admin_info.first_name}
            return render(request , "admin_edit-profile.html" , context)

        if password == old_passwrd:
            context = {"message" : "Old Password same as New Password" ,
            'icon': 'error',
            "password" : password , 
            "old_passwrd" : old_passwrd , 
            "name" : admin_info.first_name}
            return render(request , "admin_edit-profile.html" , context)

        if password != confrm_password:
            context = {"message" : "Password and Confirm Password aren't same" , 
            'icon': 'error',
            "password" : password , 
            "old_passwrd" : old_passwrd , 
            "name" : admin_info.first_name}
            return render(request , "admin_edit-profile.html" , context)

        admin_pass = SlpAdmin.objects.get(id = admin.admin.id)
        admin_pass.password = password
        print("idddddddd" , admin.admin.id)
        admin_pass.save()
        context = {"message" : "Password Updated" ,
        'icon': 'success',
        'url' : '/slp_admin/login/',
        "name" : admin_info.first_name}
        return render(request , "admin_edit-profile.html" , context)


@api_view(['GET' , 'POST'])
def forget_password(request):
    print("in method forget")
    if request.method == 'POST':
        email = request.POST['resetEmail']
        try:
            admin_email = SlpAdmin.objects.get(email = email)
        except:
            context = {
                    'message': "Email not Registerd!",
                    'url': '/slp_admin/login/',
                    'icon': 'error',
                }
            return render(request , "admin_login.html" , context)
        try:
            ids = admin_email.id
            subject = 'hello'
            text_content = 'http://127.0.0.1:8000/slp_admin/reset_password/admin_email.id/'
            data = 'Please Click the link to Reset your Password'
            content = '<br><a href="http://127.0.0.1:8000/slp_admin/reset_password/'+ str(ids)+'/"><button type="button"> CLICK </button></a>'
            html_content = data + content
            # msg = send_mail(subject,message, EMAIL_HOST_USER, [email], fail_silently = False)
            # send_mail(subject,message, EMAIL_HOST_USER, [email], fail_silently = False)
            msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, [email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("email sent")
        except Exception as e:
            print(e)
            return Response("error")
        context = {
                    'message': "Email is Sent",
                    'url': '/slp_admin/login/',
                    'icon': 'success',
                }
        return render(request , "admin_login.html" , context)


@api_view(['POST' , 'GET'])
def reset_password(request , id):
    print("idddd_reset" , id)
    if request.method == 'GET':
        resetPass = SlpAdmin.objects.get(id = id)
        return render(request , "admin_2reset_password.html")

    if request.method == 'POST':
        newPass = request.POST['new_password']
        cnfmPass = request.POST['confirm_password']
        print("new pass",newPass)
        if newPass != cnfmPass:
            context = {
                    'message': "Your New Password and Confirm Password Does not Match!",
                    'url': '/slp_admin/reset_password/'+ str(id) +'/',
                    'icon': 'error',
                }
            return render(request ,"admin_2reset_password.html" , context )
        resetPass = SlpAdmin.objects.get(id = id)
        resetPass.password = newPass
        resetPass.save()
        context = {
                    'message': "Password Reset",
                    'url': '/slp_admin/login/',
                    'icon': 'success',
                }
        return render(request ,"admin_2reset_password.html" , context )

def purchased_gift_page(request):
    try:
        admin_session = request.session['Admintoken']
    except:
        context = {
            'message': "Session Expired!",
            'url': '/slp_admin/login/',
            'icon': 'error',
        }
        return render(request, "admin_login.html", context)
    obj = PurchasedGifts.objects.all()
    template_name = "purchased_gifts.html"
    return render(request, template_name, {'gift_log': obj})
from slp_admin import models


def qr_codes(request):
    scanned_qr = models.ScannedQRCode.objects.all()
    context = {
        "scanned_qr": scanned_qr
    }
    return render(request, "qr-codes.html", context)


def dispute_requests(request):
    disputes = models.Dispute.objects.all()
    context = {
        "disputes": disputes
    }
    return render(request, "dispute-request.html", context)
