# from django.shortcuts import render
# import os
# import json
# from io import BytesIO
# import pandas as pd
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt

# # Create your views here.

# session_storage = {}

# @csrf_exempt
# def upload_file(request):
#     if request.method == 'POST':
#         file = request.FILES.get('file')
#         if not file:
#             return JsonResponse({'error': 'No file'}, status=400)
#         ext = os.path.splitext(file.name)[1]
#         if ext not in ['.xls', '.xlsx']:
#             return JsonResponse({'error': 'Invalid file format'}, status=400)
#         try:
#             df = pd.read_excel(file)
#             session_storage[request.session.session_key] = df
#             return JsonResponse({'columns': list(df.columns)})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

# @csrf_exempt
# def perform_operation(request):
#     try:
#         body = json.loads(request.body)
#         operation = body.get('operation')
#         params = body.get('params')
#         df = session_storage.get(request.session.session_key)
#         if df is None:
#             return JsonResponse({'error': 'No file uploaded'}, status=400)

#         if operation == 'add_column':
#             cols = params['columns_to_sum']
#             new_col = params['new_column_name']
#             if not all(col in df.columns for col in cols):
#                 return JsonResponse({'error': 'Column not found'}, status=400)
#             df[new_col] = df[cols].sum(axis=1)
#             session_storage[request.session.session_key] = df
#             preview = df.head().to_dict(orient='records')
#             return JsonResponse({'columns': list(df.columns), 'preview': preview})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

# def download_file(request):
#     if request.method == 'GET':
#         df = session_storage.get(request.session.session_key)
#         if df is None:
#             return JsonResponse({'error': 'No file processed'}, status=400)
#         output = BytesIO()
#         df.to_excel(output, index=False)
#         output.seek(0)
#         response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#         response['Content-Disposition'] = 'attachment; filename=output.xlsx'
#         return response
