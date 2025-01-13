import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [question, setQuestion] = useState('');
  const [answers, setAnswers] = useState([]);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploadStatus('Uploading...');
      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setUploadStatus(`Upload successful: ${response.data.chunks} chunks created.`);
    } catch (error) {
      setUploadStatus(`Upload failed: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleAskQuestion = async (e) => {
    e.preventDefault();
    if (!question) return;

    try {
      const response = await axios.post('http://localhost:8000/ask', { text: question });
      setAnswers((prev) => [
        {
          question,
          answer: response.data.answer,
          context: response.data.relevant_chunks,
        },
        ...prev,
      ]);
      setQuestion('');
    } catch (error) {
      console.error('Error asking question:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold text-center mb-6">PDF Q&A</h1>

      <form className="mb-6" onSubmit={handleFileUpload}>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:bg-blue-50 file:text-blue-700"
        />
        <button
          type="submit"
          className="mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
        >
          Upload PDF
        </button>
      </form>

      {uploadStatus && <p className="mb-4 text-center text-gray-700">{uploadStatus}</p>}

      <form className="mb-6" onSubmit={handleAskQuestion}>
        <input
          type="text"
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded mb-4"
        />
        <button
          type="submit"
          className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
        >
          Ask
        </button>
      </form>

      <div className="space-y-4">
        {answers.map((item, index) => (
          <div key={index} className="p-4 bg-white rounded shadow">
            <p className="font-bold">Q: {item.question}</p>
            <p className="text-green-700">A: {item.answer}</p>
            <details className="mt-2">
              <summary className="text-blue-600">Relevant Context</summary>
              <p className="text-gray-600 mt-1">{item.context.join(' ')}</p>
            </details>
          </div>
        ))}
      </div>
    </div>
  );
}