import json
from datetime import datetime, timezone, date, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView

from chat.models import ChatMessage, RoomChat
# from service.geoip.core import location_geoip
from user.models import Profile
from .models import Order, Category, Offer
from .forms import OrderForm, OfferForm, InactiveFilterForm


class CategoryDetailView(ListView):
    """Категории"""
    # model = Category
    slug_field = 'slug'
    paginate_by = 4
    template_name = 'tovars.html'

    def get_queryset(self):
        query = self.request.GET.get('city')
        print(query)
        if query == '0' or query == "Все города":
            order_list = Order.objects.filter(category__slug=self.kwargs.get('slug'), date_validity__gte=datetime.now(timezone.utc))
        else:
            order_list = Order.objects.filter(category__slug=self.kwargs.get('slug'), city=query, date_validity__gte=datetime.now(timezone.utc))
        return order_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetailView, self).get_context_data()
        cat = Category.objects.get(slug=self.kwargs.get('slug'))
        bread = []
        bread_id = []
        for i in cat.get_ancestors(include_self=True):
            crumb = i.name, i.get_absolute_url()
            bread.append(crumb)
            bread_id.append(i.id)
        context['breadcrumb'] = bread
        context['bread_id'] = bread_id
        # print(context['response_user'])
        # context['seller'] = seller
        return context


class OrderListView(View):
    """Вывод 4 объявлений на главной странице"""

    def get(self, request):
        order_list = Order.objects.filter(date_validity__gte=datetime.now(timezone.utc))[:4]
        # city = location_geoip(request)
        # print(location_geoip(request))
        return render(request, 'home.html', {'order_list': order_list})


class SearchOrderView(ListView):
    """Поиск по сайту"""
    template_name = "tovars.html"
    paginate_by = 4

    # Добавить поиск по категориям
    def get_queryset(self):
        if self.request.GET.get("q", None):
            return Order.objects.filter(name__icontains=self.request.GET.get("q"))\
                        .filter(date_validity__gte=datetime.now(timezone.utc))\
                        .order_by('date_validity')
        else:
            return []  # raise Http404()

    def get_context_data(self, **kwargs):
        context = super(SearchOrderView, self).get_context_data()
        # print(self.request.user)
        context["search"] = self.request.GET.get("q")
        return context


class CreateOrderView(CreateView):
    """Создание заявки, объявления"""
    model = Order
    form_class = OrderForm
    template_name = 'addpage.html'
    success_url = reverse_lazy('home')

    def string_list(self, value):
        # строковый список преобразуем в нормальный список
        result = [element.strip("'[()]") for element in value.split(", ")]
        return result

    def get_context_data(self, **kwargs):
        context = super(CreateOrderView, self).get_context_data()
        context["search"] = self.request.GET.get("q")
        bread_id = self.string_list(self.request.GET.get("bread_ids"))
        breadcrumb = self.string_list(self.request.GET.get("bread"))
        # a = breadcrumb[1::2] если надо будет ссылки на категории
        context["breadcrumb"] = breadcrumb[::2]
        context["breadcrumb_and_id"] = zip(breadcrumb[::2], bread_id)
        return context

    # def get_initial(self):
    #     #print(self.request.GET.get("bread_ids"))
    #     initial = super().get_initial()
    #     initial["category"] = self.request.GET.get("bread_ids")
    #     return initial

    def form_valid(self, form):
        form.instance.buyer = self.request.user
        form.instance.date_validity += timedelta(hours=23, minutes=59)
        # print(form.instance.category)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Invalid")
        return super().form_invalid(form)


class CalculateProfile:
    """Количество заявок и предложений у пользователя"""
    def get_sum_order(self):
        return Order.objects.filter(buyer=self.request.user)\
                        .filter(date_validity__gte=datetime.now(timezone.utc))\
                        .order_by('date_validity').count()

    def get_sum_offer(self):
        return Offer.objects.filter(seller=self.request.user).count()

    def get_sum_inactive(self):
        return Order.objects.filter(buyer=self.request.user)\
                    .filter(date_validity__lte=datetime.now(timezone.utc))\
                    .order_by('-date_validity').count() + \
               Offer.objects.filter(seller=self.request.user).exclude(status='approve').count()


class MyOrderListView(CalculateProfile, LoginRequiredMixin, ListView):
    """Мои заявки, объявления"""
    model = Order
    paginate_by = 5
    template_name = "myzapros.html"

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)\
                        .filter(date_validity__gte=datetime.now(timezone.utc))\
                        .order_by('date_validity')


class CheckDateView(LoginRequiredMixin, View):
    """Отклонить запрос, после нажатия на кнопку меняем дату"""
    def post(self, request):
        if request.is_ajax():
            my_order = Order.objects.get(id=request.POST.get('pk'), buyer=request.user)
            # my_order.delete()
            my_order.date_validity = datetime.now()
            print(datetime.now(timezone.utc))
            my_order.save()
            return redirect("/")


class ListOfferView(CalculateProfile, LoginRequiredMixin, DetailView):
    """Все предложения к заявке"""
    model = Order
    template_name = "mypredl-list.html"

    def get_context_data(self, **kwargs):  # --------------------------------------------------------------
        """"""
        context = super(ListOfferView, self).get_context_data()
        # context["offer_list"] = Offer.objects.filter(order=self.kwargs.get('pk')).exclude(status='reject')  # -------?
        context["count_approve"] = Offer.objects.filter(order=self.kwargs.get('pk'), status='approve').count()
        context["chat_message"] = ChatMessage.objects.all() # ---?
        print(context["count_approve"])
        return context

    def post(self, request, pk):
        """Одобрить или отклонить предложение"""
        if request.method == 'POST':
            offer = Offer.objects.get(pk=pk)
            if 'reject' in request.POST:
                offer.status = 'reject'
            elif 'approve' in request.POST:
                offer.status = 'approve'
            offer.save()
        return redirect(self.request.META['HTTP_REFERER'])


class GetChatMessageView(View):
    """"""
    def get(self, request, pk):
        messages = ChatMessage.objects.filter(room_id=pk).select_related("user__profile__avatar").values(
            "id", "user", "user__profile__avatar", "message", "timestamp"
        )
        chat = list(messages)
        return JsonResponse({"chat_message": chat}, safe=False)


class MakeAnOfferView(DetailView):
    """Детальное отображение заявки
    и возможность отправить предложение"""
    model = Order
    template_name = 'addpredl.html'

    def post(self, request, pk):
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.seller = request.user
            form.order = Order.objects.get(pk=pk)
            form.save()
            RoomChat.objects.create(offer=form, first=request.user, second=form.order.buyer)
        return redirect('my_offer')


class MyOfferListView(CalculateProfile, LoginRequiredMixin, ListView):
    """Мои предложения"""
    # model = Offer
    template_name = "mypredloz.html"
    paginate_by = 5

    def get_queryset(self):
        return Offer.objects.filter(seller=self.request.user)


class MyOfferInView(CalculateProfile, LoginRequiredMixin, DetailView):
    """Чат с покупателем"""
    model = Offer
    template_name = "mypredl-in.html"

    def get_context_data(self, **kwargs):
        context = super(MyOfferInView, self).get_context_data()
        context["chat_message"] = ChatMessage.objects.filter(room__offer=self.kwargs.get('pk'))
        context["room_id"] = RoomChat.objects.get(offer_id=self.kwargs.get('pk')).id
        return context


class InactiveView(CalculateProfile, LoginRequiredMixin, View):
    """Неактивные заявки и предложения и фильтр по дате"""
    # нужна пагинация

    def get_order(self):
        return Order.objects.filter(buyer=self.request.user)\
                    .filter(date_validity__lte=datetime.now(timezone.utc))\
                    .order_by('-date_validity')

    def get_offer(self):
        return Offer.objects.filter(seller=self.request.user).exclude(status='approve')

    def get_query_or_date(self, query):
        if self.form.is_valid():
            order = getattr(self, query)
            if self.form.cleaned_data["min_data"] and self.form.cleaned_data["max_data"]:
                return order().filter(
                    date_publication__range=(self.form.cleaned_data["min_data"], self.form.cleaned_data["max_data"]))
            elif self.form.cleaned_data["min_data"]:
                return order().filter(date_publication__gte=self.form.cleaned_data["min_data"])
            elif self.form.cleaned_data["max_data"]:
                return order().filter(date_publication__lte=self.form.cleaned_data["max_data"])
            else:
                return order()

    def get(self, request, sort):
        self.form = InactiveFilterForm(request.GET)

        self.context = {
            'form': self.form,
            'get_sum_inactive': self.get_sum_inactive(),
            'get_sum_offer': self.get_sum_offer(),
            'get_sum_order': self.get_sum_order(),
        }

        if sort == "order":
            self.context["order_list"] = self.get_query_or_date("get_order")
        elif sort == "offer":
            self.context['offer_list'] = self.get_query_or_date("get_offer")
        else:
            self.context["order_list"] = self.get_query_or_date("get_order")
            self.context['offer_list'] = self.get_query_or_date("get_offer")

        return render(request, 'actzapros.html', self.context)


