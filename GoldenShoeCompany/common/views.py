from django.shortcuts import render

# Create your views here.
def main_page(request):
    return render(request,  'html/main_page.html')

def men_page(request):
    return render(request, 'html/product_page.html', {"gender" : "MEN"})