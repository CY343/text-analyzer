async function getHistory() {
  const response = await fetch("http://127.0.0.1:8080/history");
  const data = await response.json();
  console.log(data);
}

getHistory();