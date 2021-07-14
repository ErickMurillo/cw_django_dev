from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from survey.models import Question, Answer, Like_Dislike
from django.db.models import Count,Q, Avg
from datetime import datetime


class QuestionListView(ListView):
    model = Question
    queryset = Question.objects.annotate(ranking = (Count('answers') * 10) + 
                                                    (Count('like_dislike__like',filter=Q(like_dislike__like=1)) * 5) -
                                                    (Count('like_dislike__like',filter=Q(like_dislike__like=0)) * 3) +
                                                    (Count('created',filter=Q(created=datetime.now())) + 10),
                                        avg = Avg('answers__value')
                                                    ).order_by('-ranking')[:20]

class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'description']
    redirect_url = ''

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['title', 'description']
    template_name = 'survey/question_form.html'


def answer_question(request):
    question_pk = request.POST.get('question_pk')
    print(request.POST)
    if not request.POST.get('question_pk'):
        return JsonResponse({'ok': False})
    question = Question.objects.filter(pk=question_pk)[0]
    answer = Answer.objects.get(question=question, author=request.user)
    answer.value = request.POST.get('value')
    answer.save()
    return JsonResponse({'ok': True})

# def like_dislike_question(request):
#     question_pk = request.POST.get('question_pk')
#     if not request.POST.get('question_pk'):
#         return JsonResponse({'ok': False})
#     question = Question.objects.filter(pk=question_pk)[0]
#     # TODO: Dar Like
#     return JsonResponse({'ok': True})

def like_dislike_question(request, pk, valor):
    question = Question.objects.get(pk = pk)
    #exist 
    exist = Like_Dislike.objects.filter(user=request.user,question=question).exists()
    if exist:
        update = Like_Dislike.objects.get(user=request.user,question=question)
        update.like = valor
        update.save()
    else:
        respuesta = Like_Dislike.objects.create(user=request.user,question=question,like=valor)
    return HttpResponseRedirect("/")
