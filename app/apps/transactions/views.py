from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from app.apps.transactions.serializers import TransactionCreateSerializer, TransactionUpdateSerializer, TransactionReadSerializer
from app.apps.transactions.services.transaction_service import TransactionService
from app.apps.transactions.repositories.transactionrepo import TransactionRepository
from app.apps.transactions.filters import TransactionFilter
from app.apps.transactions.utils import filter_response_fields
from app.apps.base.pagination import StandardResultsSetPagination


class TransactionViewSet(viewsets.ModelViewSet):
    """Transaction ViewSet."""
    queryset = TransactionRepository.get_all_queryset()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TransactionFilter
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == "create":
            return TransactionCreateSerializer
        if self.action == "partial_update":
            return TransactionUpdateSerializer
        if self.action == "retrieve" or self.action == "list":
            return TransactionReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        transaction = TransactionService.create_transaction(data)
        data = TransactionReadSerializer(transaction).data
        return Response(data, status=201)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, context={"instance": instance}, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        transaction = TransactionService.update_transaction(instance, data)
        data = TransactionReadSerializer(transaction).data
        return Response(data, status=200)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        fields = filter_response_fields(model=TransactionRepository.get_model(),request=request)
        data = self.get_serializer(instance, fields=fields).data
        return Response(data, status=200)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        fields = filter_response_fields(model=TransactionRepository.get_model(),request=request)
        # pagination
        paginate = int(request.query_params.get("page_size", 1) or 1)
        if not paginate:
            self._paginator = None
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self.get_serializer(page, many=True, fields=fields).data
            return self.get_paginated_response(data)
        # no pagination
        data = self.get_serializer(queryset, many=True, fields=fields).data
        return Response(data, status=200)


