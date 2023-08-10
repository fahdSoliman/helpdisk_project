from datetime import timedelta, datetime
from django.utils.timezone import now
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
import sqlite3, psycopg2
from product.models import HostDomain,ResDomain,SharedHosting,VPS
from .forms import Resdomain_Form, Hostdomain_Form,Shared_Form, Vps_Form,Botpress_form,Botpress_user
from .models import Botpress
# Create your views here.


###################
##  Agent views  ##
###################


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def view_new_request(request):
    today = now()
    last_7_days = datetime.now() - timedelta(days=7)
    hostdomain_products = HostDomain.objects.filter(start_date__gte = last_7_days, start_date__lte = today, is_active = 0).order_by('-updated')
    resdomain_products = ResDomain.objects.filter(start_date__gte = last_7_days, start_date__lte = today, is_active = 0).order_by('-updated')
    shared_products = SharedHosting.objects.filter(start_date__gte = last_7_days, start_date__lte = today, is_active = 0).order_by('-updated')
    vps_products = VPS.objects.filter(start_date__gte = last_7_days, start_date__lte = today, is_active = 0).order_by('-updated')  
    context = {
        'host_products': hostdomain_products,
        'resdomain_products': resdomain_products,
        'shared_products': shared_products,
        'vps_products': vps_products
    }
    return render(request, 'agent/view_new_request.html', context)



@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def view_old_request(request):
    today = now()
    forward_7_days = datetime.now() + timedelta(days=7)
    hostdomain_products = HostDomain.objects.filter(expire_date__gte = today, expire_date__lte = forward_7_days).order_by('-updated')
    resdomain_products = ResDomain.objects.filter(expire_date__gte = today, expire_date__lte = forward_7_days).order_by('-updated')
    shared_products = SharedHosting.objects.filter(expire_date__gte = today, expire_date__lte = forward_7_days).order_by('-updated')
    vps_products = VPS.objects.filter(expire_date__gte = today, expire_date__lte = forward_7_days).order_by('-updated')  
    context = {
        'host_products': hostdomain_products,
        'resdomain_products': resdomain_products,
        'shared_products': shared_products,
        'vps_products': vps_products
    }
    return render(request, 'agent/view_old_request.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def agent_process_resdomain(request, id):

    detail = get_object_or_404(ResDomain, id = id)
    print(detail.user)
    customer = User.objects.get(username = detail.user)
    if request.method == 'POST':
        resdomain = Resdomain_Form(request.POST, request.FILES, instance=detail)
        if resdomain.is_valid():
            resdomain.save()
            messages.success(request, f'تم تعديل بيانات الطلب بنجاح')
            return redirect('home')
    else:
        resdomain = Resdomain_Form(instance=detail)

    context = {
        'detail': detail,
        'customer': customer,
        'resdomain_form':resdomain,
    }
    return render(request, 'agent/process_resdomain.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def agent_process_hostdomain(request, id):

    detail = get_object_or_404(HostDomain, id = id)
    print(detail.user)
    customer = User.objects.get(username = detail.user)
    if request.method == 'POST':
        hostdomain = Hostdomain_Form(request.POST, instance=detail)
        if hostdomain.is_valid():
            hostdomain.save()
            print("success")
            messages.success(request, f'تم تعديل بيانات الطلب بنجاح')
            return redirect('home')
    else:
        hostdomain = Hostdomain_Form(instance=detail)

    context = {
        'detail': detail,
        'customer': customer,
        'hostdomain_form':hostdomain,
    }
    return render(request, 'agent/process_hostdomain.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def agent_process_shared(request, id):

    detail = get_object_or_404(SharedHosting, id = id)
    print(detail.user)
    customer = User.objects.get(username = detail.user)
    if request.method == 'POST':
        shared_form = Shared_Form(request.POST, request.FILES, instance=detail)
        if shared_form.is_valid():
            shared_form.save()
            messages.success(request, f'تم تعديل بيانات الطلب بنجاح')
            return redirect('home')
    else:
        shared_form = Shared_Form(instance=detail)

    context = {
        'detail': detail,
        'customer': customer,
        'shared_form':shared_form,
    }
    return render(request, 'agent/process_shared.html', context)



@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def agent_process_vps(request, id):

    detail = get_object_or_404(VPS, id = id)
    print(detail.user)
    customer = User.objects.get(username = detail.user)
    if request.method == 'POST':
        vps_form = Vps_Form(request.POST, request.FILES, instance=detail)
        if vps_form.is_valid():
            vps_form.save()
            messages.success(request, f'تم تعديل بيانات الطلب بنجاح')
            return redirect('home')
    else:
        vps_form = Shared_Form(instance=detail)

    context = {
        'detail': detail,
        'customer': customer,
        'vps_form':vps_form,
    }
    return render(request, 'agent/process_vps.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def agent_botpress_hitl(request):
    botpress = Botpress.objects.all().first()
    context = {
        'botpress': botpress
    }
    return render(request, 'agent/support_botpress_HITL.html', context)

# end of Agent Views


######################
##   Admin Views    ##
######################
@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def admin_botpress(request):
    try:
        botpress_info = Botpress.objects.all().first()
    except (Botpress.DoesNotExist) as e:
        print(e)
    if botpress_info is not None:
        if botpress_info.db_type == 'sqlite':
        # print(botpress_info)
            query = 'SELECT s.id, s.email, s.strategy, w.role FROM strategy_default as s, workspace_users as w WHERE s.email = w.email;'
            rows = connect_sqlite(botpress_info.db_url, query)
        # print(rows)
        else:
            print(1)
            query = 'SELECT s.id, s.email, s.strategy, w.role FROM strategy_default as s, workspace_users as w WHERE s.email = w.email;'
            rows = connect_postgres(query, botpress_info.db_url, botpress_info.db_name, botpress_info.db_username, botpress_info.db_password)
            # do some commands for postgresql
    else:
        rows = {}
        pass
    context = {
        'res': rows,
        'botpress_info': botpress_info
    }
    return render(request, 'agent/admin_botpress.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def admin_botpress_init(request):
    if request.method == 'POST':
        botpress_form = Botpress_form(request.POST)
        if botpress_form.is_valid():
            data = botpress_form.cleaned_data
            botpress_form.save()
            messages.success(request, f'''تم انشاء إعداد Botpress لقاعدة البيانات {data.get('db_type')} بنجاح''')
            return redirect('agent_botpress')
    else:
        botpress_form = Botpress_form()
    
    context = {
        'botpress_form': botpress_form
    }

    return render(request,'agent/admin_botpress_init.html', context)



@login_required()
@user_passes_test(lambda u: u.groups.filter(name='stuff').exists(), login_url='login')
def admin_botpress_create_user(request):
    '''
    view for creating Botpress user using SQL injuction, no matter if the DB is SQLITE or Postgresql.
    '''
    if request.method == 'POST':
        form = Botpress_user(request.POST)
        botpress_info = Botpress.objects.all().first()
        if botpress_info.db_type == 'sqlite':
            query = 'select password, salt, strategy from strategy_default where id = 1;'
            data = connect_sqlite(botpress_info.db_url, query)
            atribute ={}
            if form.is_valid():
                print(data[0][2])
                cd = form.cleaned_data
                print(cd.get('email'))
                query2 = f'''INSERT INTO strategy_default ( email, password, salt, strategy, attributes) VALUES ( '{cd.get('email')}', '{data[0][0]}', '{data[0][1]}', '{data[0][2]}', '{atribute}');'''
                save = connect_sqlite(botpress_info.db_url, query2)
                query3 = f''' INSERT INTO workspace_users ( email, strategy, workspace, role) VALUES ( '{cd.get('email')}', '{data[0][2]}', '{data[0][2]}', '{cd.get('role')}'); '''
                save = connect_sqlite(botpress_info.db_url, query3)
                messages.success(request, f'''تم انشاء حساب botpress للإيميل {cd.get('email')} بدور {cd.get('role')} بنجاح''')
                return redirect('agent_botpress')
        else:
            query = 'select password, salt, strategy from strategy_default where id = 1;'
            data = connect_postgres(query, botpress_info.db_url, botpress_info.db_name, botpress_info.db_username, botpress_info.db_password)
            atribute ={}
            if form.is_valid():
                print(data[0][2])
                cd = form.cleaned_data
                print(cd.get('email'))
                query2 = f'''INSERT INTO strategy_default ( email, password, salt, strategy, attributes) VALUES ( '{cd.get('email')}', '{data[0][0]}', '{data[0][1]}', '{data[0][2]}', '{atribute}');'''
                save = connect_postgres(query2, botpress_info.db_url, botpress_info.db_name, botpress_info.db_username, botpress_info.db_password)
                query3 = f''' INSERT INTO workspace_users ( email, strategy, workspace, role) VALUES ( '{cd.get('email')}', '{data[0][2]}', '{data[0][2]}', '{cd.get('role')}'); '''
                save = connect_postgres(query3, botpress_info.db_url, botpress_info.db_name, botpress_info.db_username, botpress_info.db_password)
                messages.success(request, f'''تم انشاء حساب botpress للإيميل {cd.get('email')} بدور {cd.get('role')} بنجاح''')
                return redirect('agent_botpress')
    else:
        form = Botpress_user()
    context = {
        'form': form
    }
    return render(request, 'agent/create_botpress_account.html', context)

def admin_botpress_del_user(request, email):
    botpress_info = Botpress.objects.all().first()
    if botpress_info.db_type == 'sqlite':
        query = f'''DELETE FROM strategy_default WHERE email = '{email}';'''
        connect_sqlite(botpress_info.db_url, query)
        query = f'''DELETE FROM workspace_users WHERE email = '{email}';'''
        connect_sqlite(botpress_info.db_url, query)
        messages.success(request, f'''تم حذف حساب Botpress ذو البريد {email}''')
    else:
        query = f'''DELETE FROM strategy_default WHERE email = '{email}';'''
        connect_postgres(query, botpress_info.db_url, botpress_info.db_name, botpress_info.db_username, botpress_info.db_password)
        query = f'''DELETE FROM workspace_users WHERE email = '{email}';'''
        connect_postgres(query, botpress_info.db_url, botpress_info.db_name, botpress_info.db_username, botpress_info.db_password)
        messages.success(request, f'''تم حذف حساب Botpress ذو البريد {email}''')

    return redirect('agent_botpress')
#  end of Admin Views


# helping func

def connect_sqlite(db_url,query):
    con = sqlite3.connect(db_url)
    cur = con.cursor()
    res = (())
    cur.execute(query)
    con.commit()
    rows = cur.fetchall()
    con.close()
    return rows


def connect_postgres(query, db_url, db_name, db_username, db_password):
    con = psycopg2.connect(
        host=db_url,
        dbname=db_name,
        user=db_username,
        password=db_password
    )
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    try:
        row = cur.fetchall()
    except:
        row = {}
        pass
    con.close()
    return row