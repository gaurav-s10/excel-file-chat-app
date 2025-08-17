import base64
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import pandas as pd
from io import BytesIO

SESSION_DATA = {}


class ExcelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_key = id(self)
        await self.accept()

    async def disconnect(self, code):
        SESSION_DATA.pop(self.session_key, None)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'upload':
            await self.handle_upload(data)
        elif action == 'operation':
            await self.handle_operation(data)
        elif action == 'request_download':
            await self.handle_download()
        else:
            await self.send(text_data=json.dumps({'error': "Unknown action"}))

    async def handle_upload(self, data):
        file_data = data['file']
        header, b64data = file_data.split(',', 1)
        xls_bytes = base64.b64decode(b64data)
        df = pd.read_excel(BytesIO(xls_bytes))

        SESSION_DATA[self.session_key] = df
        await self.send(text_data=json.dumps({
            'action': 'upload_response',
            'columns': list(df.columns),
            'message': 'Upload successful',
        }))

    async def handle_operation(self, data):
        df = SESSION_DATA.get(self.session_key)
        if df is None:
            await self.send(text_data=json.dumps({'error': 'No file uploaded'}))
            return

        operation = data['operation']
        params = data['params']

        if operation == 'add_column':
            try:
                cols = params['columns_to_sum']
                new_col = params['new_column_name']
                if not all(col in df.columns for col in cols):
                    raise ValueError("Column not found")
                df[new_col] = df[cols[0]] + df[cols[1]]
                SESSION_DATA[self.session_key] = df
                preview = df.head().to_dict(orient='records')
                await self.send(text_data=json.dumps({
                    'action': 'operation_response',
                    'columns': list(df.columns),
                    'preview': preview,
                }))
            except Exception as e:
                await self.send(text_data=json.dumps({'error': str(e)}))
        else:
            await self.send(text_data=json.dumps({'error': 'Unknown operation'}))

    async def handle_download(self):
        df = SESSION_DATA.get(self.session_key)
        if df is None:
            await self.send(text_data=json.dumps({'error': 'No file available for download'}))
            return

        out = BytesIO()
        df.to_excel(out, index=False)
        out.seek(0)
        b64_excel = base64.b64encode(out.read()).decode()
        await self.send(text_data=json.dumps({
            'action': 'download',
            'filename': 'result.xlsx',
            'file': 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + b64_excel
        }))
