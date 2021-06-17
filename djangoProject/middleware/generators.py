from djangoProject import settings


class GenarateCLient:
    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, *args, **kwargs):
        # print( request.POST["client_id"])
        post_dict=request.POST.copy()
        post_dict["client_id"]=settings.CLIENT_ID
        post_dict["client_secret"]=settings.CLIENT_SECRET
        request.POST=post_dict