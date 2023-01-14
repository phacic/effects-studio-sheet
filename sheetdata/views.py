from rest_framework.views import APIView
from rest_framework.response import Response

from sheetdata.utils import load_sheet_data


class SheetView(APIView):
    def get(self, request, *args, **kwargs):
        """
        cache - save file
        refresh - don't use cache download fresh one on each request
        list -
        type - list or keyvalue
        """
        load_sheet_data()
        return Response(data={})
