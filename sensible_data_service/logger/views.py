from django.shortcuts import render, get_object_or_404

#from polls.models import Poll

def index(request):
 #   latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
  #  context = {'latest_poll_list': latest_poll_list}
#    return render(request, 'polls/index.html', context)
    return HttpResponse("You're voting on poll.")



def functionTest(request):
    return HttpResponse("CIAO")

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)
