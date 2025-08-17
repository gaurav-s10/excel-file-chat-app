import React, { useRef, useState, useEffect } from "react";
import { saveAs } from 'file-saver';

const WS_URL = "ws://localhost:8000/ws/excel/";

export default function App() {
  const ws = useRef(null);
  const [connected, setConnected] = useState(false);
  const [columns, setColumns] = useState([]);
  const [preview, setPreview] = useState([]);
  const [file, setFile] = useState(null);

  useEffect(() => {
    ws.current = new window.WebSocket(WS_URL);

    ws.current.onopen = () => setConnected(true);
    ws.current.onclose = () => setConnected(false);

    ws.current.onmessage = (e) => {
      const msg = JSON.parse(e.data);

      if (msg.action === 'upload_response') {
        setColumns(msg.columns);
        setPreview([]);
      } else if (msg.action === 'operation_response') {
        setColumns(msg.columns);
        setPreview(msg.preview);
      } else if (msg.action === 'download') {
        // handle a base64 Excel download.
        const arr = msg.file.split(',');
        const bstr = atob(arr[1]);
        let n = bstr.length;
        let u8arr = new Uint8Array(n);
        while(n--) u8arr[n] = bstr.charCodeAt(n);
        const blob = new Blob([u8arr], {type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"});
        saveAs(blob, msg.filename);
      } else if (msg.error) {
        alert(msg.error);
      }
    };

    return () => ws.current.close();
  }, []);

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return; // guard for no file selected
    setFile(file);
    const reader = new FileReader();
    reader.onload = () => {
      ws.current.send(JSON.stringify({
        action: "upload",
        file: reader.result,
        filename: file.name,
      }));
    };
    reader.readAsDataURL(file);
  };

  const handleAddColumn = () => {
    const c1 = prompt("First column to sum:", columns);
    const c2 = prompt("Second column to sum:", columns[1]);
    const newCol = prompt("New column name:", "Sum");
    ws.current.send(JSON.stringify({
      action: "operation",
      operation: "add_column",
      params: {
        columns_to_sum: [c1, c2],
        new_column_name: newCol,
      }
    }));
  };

  const handleDownload = () => {
    ws.current.send(JSON.stringify({
      action: "request_download"
    }));
  };

  return (
    <div style={{padding: 40}}>
      <h2>Excel File Websocket Demo</h2>
      <div>
        <input type="file" accept=".xls,.xlsx" onChange={handleUpload}/>
        <button onClick={handleAddColumn} disabled={columns.length === 0}>Add Column (Sum)</button>
        <button onClick={handleDownload} disabled={columns.length === 0}>Download</button>
      </div>
      <div>
        <strong>Columns:</strong> {columns.join(', ')}
        <br/>
        <strong>Preview:</strong>
        <table border="1">
          <thead>
            <tr>{columns.map(c => <th key={c}>{c}</th>)}</tr>
          </thead>
          <tbody>
            {preview.map((row,i) => 
              <tr key={i}>{columns.map(c => <td key={c}>{row[c]}</td>)}</tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
