from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sheetdata.utils import load_sheet_data


class SheetView(APIView):
    def get(self, request, *args, **kwargs):
        """

        Query parameters
        nocache - get a fresh copy on each request, else download and save a copy of the sheet
        page - pagination page to fetch (saves a copy)
        page_size - number of items to fetch
        """
        nocache = bool(self.request.query_params.get("nocache"))
        page: str = self.request.query_params.get("page")
        page_size: str = self.request.query_params.get("page_size")

        if page is not None and not page.isnumeric():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"msg": "page query parameter should be an integer"},
            )

        if page_size is not None and not page_size.isnumeric():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"msg": "page_size query parameter should be an integer"},
            )

        page = int(page) if page else None
        page_size = int(page_size) if page_size else None

        err, data = load_sheet_data(no_cache=nocache, page=page, page_size=page_size)
        if err:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"msg": "Cannot load external resource."},
            )

        return Response(data=data)
