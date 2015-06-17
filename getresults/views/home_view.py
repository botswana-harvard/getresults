from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title="LIMS",
            receive_description="Receive samples",
            order_description="Order test",
            validate_description='Validate Results',
            result_description='View Results',
        )
        return context
