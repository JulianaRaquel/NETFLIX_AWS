from django.shortcuts import render
from .models import Filme
from django.views.generic import TemplateView, ListView, DetailView

#def homepage(request):
    #return render(request, "homepage.html")

class Homepage(TemplateView):
    template_name = 'homepage.html'

# url - view - html
#def homefilmes(request):
    #lista_filmes = Filme.objects.all()
    #return render(request, "homefilmes.html", {'lista_filmes': lista_filmes})

class Homefilmes(ListView):
    template_name = 'homefilmes.html'
    model = Filme
    # object_filme --> lista de itens do modelo

class Detalhesfilme(DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme
    # object --> 1 item do nosso modelo

    def get(self, request, *args, **kwargs):
        # contabilizar uma visualização
        # descobrir qual filme o usuário está acessando
        filme = self.get_object()
        # somar 1 nas visualizações daquele filme
        filme.Vizualiizacoes += 1
        # salvar
        filme.save()  #
        return super().get(request, *args, **kwargs) # redireciona o usuário para a url final

    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        # filtrar a minha tabela de filme pegando os filmes cuja categoria é igual a categoria da página (object)
        # self.get_object()
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)
        context["filmes_relacionados"] = filmes_relacionados
        return context


class Pesquisafilme(ListView):
    template_name = 'pesquisa.html'
    model = Filme

    def get_queryset(self):
        termo_de_pesquisa = self.request.GET.get('query')
        if termo_de_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_de_pesquisa)
            return object_list
        else:
            return None



