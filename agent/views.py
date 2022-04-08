from django.shortcuts import render
import sqlite3
# Create your views here.


def view_request(request):
    
    return render(request, 'agent/view_request.html')

def admin_settings(request):
    return render(request, 'agent/admin_settings.html')

def admin_botpress_accounts(request):
    con = sqlite3.connect("C:\\botpress\\data\\storage\\core.sqlite")
    cur = con.cursor()
    res = (())
    cur.execute('select * from strategy_default')
    rows = cur.fetchall()
    print(rows)
    
    context = {
        'res': rows,
    }
    return render(request, 'agent/admin_botpress_accounts.html', context)