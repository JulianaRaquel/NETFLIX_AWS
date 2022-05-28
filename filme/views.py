from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

#def homepage(request):
    #return render(request, "homepage.html")

class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:     # se o usuario está autenticado
            return redirect('filme:homefilmes')  # redireciona para a homeflmes
        else:    # se não está autenticado
            return super().get(request, *args, **kwargs)      # redireciona para a homepage

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')

# url - view - html
#def homefilmes(request):
    #lista_filmes = Filme.objects.all()
    #return render(request, "homefilmes.html", {'lista_filmes': lista_filmes})

class Homefilmes(LoginRequiredMixin, ListView):
    template_name = 'homefilmes.html'
    model = Filme
    # object_filme --> lista de itens do modelo

class Detalhesfilme(LoginRequiredMixin, DetailView):
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
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs) # redireciona o usuário para a url final

    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        # filtrar a minha tabela de filme pegando os filmes cuja categoria é igual a categoria da página (object)
        # self.get_object()
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)
        context["filmes_relacionados"] = filmes_relacionados
        return context


class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = 'pesquisa.html'
    model = Filme

    def get_queryset(self):
        termo_de_pesquisa = self.request.GET.get('query')
        if termo_de_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_de_pesquisa)
            return object_list
        else:
            return None

class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # a função get_success_url espera um link como resposta
        return reverse('filme:login')




