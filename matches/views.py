from django.shortcuts import render, redirect
from django.http import Http404
import datetime as dt
from datetime import date, timedelta,datetime
from collections import defaultdict
from matches.models import MatchResult
from .dateconvert import to_turkish_date_manual
from .format_league import format_league
from .last5 import get_last5
from .forms import NewsletterForm
from django.core.mail import send_mail
from django.conf import settings

lig_data = ["ingiltere", "italya", "türkiye"]

def home(request):
    data = {
        "ligler": lig_data,
        "images": "logo.png"
    }
    return render(request, "index.html", data)

def match_predictions_view(request):
    selected_date = request.GET.get("date")
    if not selected_date:
        today = date.today()
        today=today + timedelta(hours=+3)
        return redirect(f"{request.path}?date={today}")

    try:
        center_date = dt.datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        center_date = today

    qs = MatchResult.objects.filter(date=center_date)
    
    
    # Eğer seçilen tarihte hiç veri yoksa, kullanıcıya uygun bir mesaj gösterin.
    if not qs.exists():
        context = {
            "page_title": "BÜLTEN",
            "all_results": {},  # boş
            "date_list": [(center_date + timedelta(days=i)).isoformat() for i in range(-2, 3)],
            "league_names": {},
            "selected_date": selected_date,
            "message": "Seçilen tarihte veri bulunamadı."
        }
        return render(request, "matches.html", context)
    
    # Veri varsa devam et
    all_results = defaultdict(list)
    for match in qs:
        match_dict = match.to_dict()
        match_dict["display_date"] = to_turkish_date_manual(match.date)
        all_results[match.league if match.league else "Diğer"].append(match_dict)
        try:
            # Varsayalım match_dict["TIME"] 'nin formatı "HH:MM"
            time_obj = datetime.strptime(match_dict["TIME"], "%H:%M")
            time_obj_plus3 = time_obj + timedelta(hours=3)
            match_dict["TIME"] = time_obj_plus3.strftime("%H:%M")
        except Exception as e:
            print("Time ekleme hatası:", e)
    date_list = [(center_date + timedelta(days=i)).isoformat() for i in range(-2, 3)]
    
    all_leagues = {}
    custom_order = ["turkey-super-lig", "turkey-1-lig", "europe-uefa-champions-league","europe-uefa-europa-league","europe-uefa-conference-league","england-premier-league","spain-la-liga","italy-serie-a","germany-bundesliga","france-ligue-1",]

    for league in all_results:
        all_leagues[league] = format_league(league)


    ordered_results = {}
    for league in custom_order:
        if league in all_results:
            ordered_results[league] = all_results[league]
    for league in all_results:
        if league not in ordered_results:
            ordered_results[league] = all_results[league]        

    context = {
        "page_title": "BÜLTEN",
        "all_results": dict(ordered_results),
        "date_list": date_list,
        "league_names": all_leagues,
        "selected_date": selected_date,
    }
    return render(request, "matches.html", context)


def match_details_view(request, id):
    try:
        mr = MatchResult.objects.get(id=id)
    except MatchResult.DoesNotExist:
        raise Http404("Maç bulunamadı.")
    
    match = mr.to_dict()
    home_team_name = match["HomeTeam"]
    away_team_name = match["AwayTeam"]
    match_league = match.get("league", "Diğer")
    home_last5 = get_last5(match_league, home_team_name)
    away_last5 = get_last5(match_league, away_team_name)
    
    context = {
        "home_last5": home_last5,
        "away_last5": away_last5,
        "match": match,
        "page_title": f"{home_team_name} vs {away_team_name}",
    }
    return render(request, "details.html", context)

def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            # Kullanıcının gönderdiği mesajı kendi e-posta adresinize gönderiyoruz.
            send_mail(
                subject="Yeni Tahminai Kullanıcı Mesajı",
                message=message,
                from_email=settings.EMAIL_HOST_USER,  # Gönderen adresi
                recipient_list=['furkanyl509@gmail.com'],  # Kendi e-posta adresinizi buraya yazın
                fail_silently=False,
            )
            return redirect("newsletter_success")
    else:
        form = NewsletterForm()
    return render(request, "newsletter.html", {"form": form})

def newsletter_success(request):
    return render(request, "newsletter-success.html")

def googlesearchconsole(request):
    
    return render(request, "google67322d1adb8aa749.html")
from django.http import HttpResponse
from django.shortcuts import render

def ads_txt(request):
    response = HttpResponse(content_type="text/plain")
    response['Content-Disposition'] = 'inline; filename=ads.txt'
    response.write("google.com, pub-9818130828655195, DIRECT, f08c47fec0942fa0")
    return response
