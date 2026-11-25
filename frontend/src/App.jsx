import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8080";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

async function loadHistory() {
  try {
    const response = await fetch(`${API_URL}/history`);
    const data = await response.json();
    setHistory(data);
  } catch {
    console.log("Could not load history. Is the backend running?");
  }
}
  useEffect(() => {
    loadHistory();
  },[])

  async function handleAnalyze() {
    const response = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text }),
    });
    const data = await response.json();
    setResult(data);
    await loadHistory();
  } 

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Text Analyzer</h1>
      <textarea
        rows={5}
        style={{ width: "100%" }}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type something..."
      />
      <button onClick={handleAnalyze}>Analyze</button>

      {result && (
        <p>
          Result: <b>{result.label}</b> ({result.score})
        </p>
      )}
      <h2>History</h2>
      <ul>
        {history.map((item) => (
        <li key= {item.id}>
          {item.text}: <b>{item.label}</b> ({item.score})
          </li>
          ))}
          </ul>
    </div>
  );
}

export default App;