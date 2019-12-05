from rest_framework import status
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from snippets import log
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.schema import custom_schema
from rest_framework import schemas
from rest_framework.compat import coreapi, coreschema

from celery.decorators import task
from celery.utils.log import get_task_logger
from celery.result import AsyncResult




import coreapi, coreschema
from rest_framework.schemas import AutoSchema, ManualSchema
# custom_schema = AutoSchema(manual_fields=[
#     coreapi.Field("username", required=True, location="form", type="string", description="username here"),
#     coreapi.Field("password", required=True, location="form", type="string", description="password field"
# ]
@task(name="call_execution_api")
def call_execution_api(data):
    resp = {"data": data, 'status': "success"}
    return resp

@api_view(['POST'])
def snippet_abc(request):
    data  = request.data
    result = call_execution_api.delay(data)
    print(dir(result))
    print(result.task_id)
    resp = {"data": result.task_id, 'status': "success"}
    return Response(resp, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def snippet_result(request, task_id):
    resp = {"result": None, 'status': "success"}
    result = AsyncResult(task_id)
    resp.update({'status': result.status})
    if 'SUCCESS' ==result.status:
        resp.update({'result':result.result})
    return Response(resp, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@schema(custom_schema)
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.

    """
    log.info("request.method %s" % request.method)
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        log.info("rserializer.data %s" % serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    GET:

    This is get method

    PUT:

    This is post method

    DELETE:

    This is delete method
    """

    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
