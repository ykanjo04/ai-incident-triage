import { useState, useRef } from 'react';
import { uploadLogs, uploadLogFile, uploadDemoLogs } from '../services/api';

function UploadLogs({ onUploadSuccess }) {
  const [logText, setLogText] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleTextUpload = async () => {
    if (!logText.trim()) return;
    setIsUploading(true);
    setError(null);
    setUploadResult(null);
    try {
      const logs = logText.split('\n').filter(l => l.trim());
      const result = await uploadLogs(logs);
      setUploadResult(result);
      setLogText('');
      if (onUploadSuccess) onUploadSuccess(result);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setIsUploading(true);
    setError(null);
    setUploadResult(null);
    try {
      const result = await uploadLogFile(file);
      setUploadResult(result);
      if (onUploadSuccess) onUploadSuccess(result);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'File upload failed');
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleDemoLoad = async () => {
    setIsUploading(true);
    setError(null);
    setUploadResult(null);
    try {
      const result = await uploadDemoLogs();
      setUploadResult(result);
      if (onUploadSuccess) onUploadSuccess(result);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Demo load failed');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6">
      <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
        <svg className="w-5 h-5 text-cyan-400" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
        </svg>
        Upload Logs
      </h2>

      {/* Text Input */}
      <textarea
        className="w-full h-40 bg-slate-900/80 border border-slate-700 rounded-lg p-3 text-sm text-slate-300 font-mono placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 resize-none"
        placeholder="Paste system logs here (one per line)...&#10;&#10;Example:&#10;ERROR: Order execution timeout&#10;WARNING: API latency spike detected&#10;User report: Cannot close trade position"
        value={logText}
        onChange={(e) => setLogText(e.target.value)}
        disabled={isUploading}
      />

      {/* Action Buttons */}
      <div className="flex flex-wrap items-center gap-3 mt-4">
        <button
          onClick={handleTextUpload}
          disabled={isUploading || !logText.trim()}
          className="inline-flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 disabled:bg-slate-700 disabled:text-slate-500 text-white text-sm font-medium rounded-lg transition-colors duration-200 cursor-pointer disabled:cursor-not-allowed"
        >
          {isUploading ? (
            <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          ) : (
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
            </svg>
          )}
          Upload Logs
        </button>

        <label className="inline-flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white text-sm font-medium rounded-lg transition-colors duration-200 cursor-pointer">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m6.75 12-3-3m0 0-3 3m3-3v6m-1.5-15H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
          </svg>
          Upload File
          <input
            ref={fileInputRef}
            type="file"
            accept=".json,.csv,.txt,.log"
            onChange={handleFileUpload}
            className="hidden"
            disabled={isUploading}
          />
        </label>

        <div className="h-8 w-px bg-slate-700"></div>

        <button
          onClick={handleDemoLoad}
          disabled={isUploading}
          className="inline-flex items-center gap-2 px-4 py-2 bg-violet-600 hover:bg-violet-500 disabled:bg-slate-700 disabled:text-slate-500 text-white text-sm font-medium rounded-lg transition-colors duration-200 cursor-pointer disabled:cursor-not-allowed"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 0 0-1.883 2.542l.857 6a2.25 2.25 0 0 0 2.227 1.932H19.05a2.25 2.25 0 0 0 2.227-1.932l.857-6a2.25 2.25 0 0 0-1.883-2.542m-16.5 0V6A2.25 2.25 0 0 1 6 3.75h3.879a1.5 1.5 0 0 1 1.06.44l2.122 2.12a1.5 1.5 0 0 0 1.06.44H18A2.25 2.25 0 0 1 20.25 9v.776" />
          </svg>
          Load Demo Logs
        </button>
      </div>

      {/* Success Message */}
      {uploadResult && (
        <div className="mt-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3">
          <p className="text-sm text-emerald-400 font-medium">
            Successfully uploaded {uploadResult.logs_received} logs ({uploadResult.embeddings_stored} embeddings stored).
            Total vectors in index: {uploadResult.total_vectors}
          </p>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-4 bg-red-500/10 border border-red-500/20 rounded-lg p-3">
          <p className="text-sm text-red-400 font-medium">{error}</p>
        </div>
      )}
    </div>
  );
}

export default UploadLogs;
