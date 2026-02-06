const severityConfig = {
  P1: {
    label: 'P1 - Critical',
    color: 'bg-red-500/10 text-red-400 border-red-500/30',
    dot: 'bg-red-400',
  },
  P2: {
    label: 'P2 - Major',
    color: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
    dot: 'bg-orange-400',
  },
  P3: {
    label: 'P3 - Minor',
    color: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30',
    dot: 'bg-yellow-400',
  },
  P4: {
    label: 'P4 - Info',
    color: 'bg-green-500/10 text-green-400 border-green-500/30',
    dot: 'bg-green-400',
  },
};

function IncidentCard({ result }) {
  const analysis = result.analysis;
  const severity = severityConfig[analysis.severity_level] || severityConfig.P3;

  return (
    <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 hover:border-slate-600/50 transition-all duration-200">
      {/* Header: Severity + Timestamp */}
      <div className="flex items-center justify-between mb-4">
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${severity.color}`}>
          <span className={`w-1.5 h-1.5 rounded-full ${severity.dot}`}></span>
          {severity.label}
        </span>
        <span className="text-xs text-slate-500">
          {new Date(result.created_at).toLocaleString()}
        </span>
      </div>

      {/* Summary */}
      <h3 className="text-base font-semibold text-white mb-3 leading-snug">
        {analysis.summary}
      </h3>

      {/* Details Grid */}
      <div className="space-y-3">
        {/* Root Cause */}
        <div className="bg-slate-900/50 rounded-lg p-3">
          <div className="flex items-center gap-2 mb-1">
            <svg className="w-4 h-4 text-cyan-400" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
            </svg>
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Root Cause</span>
          </div>
          <p className="text-sm text-slate-300">{analysis.root_cause}</p>
        </div>

        {/* Owner + Next Steps */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div className="bg-slate-900/50 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <svg className="w-4 h-4 text-violet-400" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" />
              </svg>
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Owner</span>
            </div>
            <p className="text-sm text-slate-300 font-medium">{analysis.recommended_owner}</p>
          </div>

          <div className="bg-slate-900/50 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <svg className="w-4 h-4 text-emerald-400" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
              </svg>
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Next Steps</span>
            </div>
            <p className="text-sm text-slate-300">{analysis.next_steps}</p>
          </div>
        </div>
      </div>

      {/* Logs Preview */}
      {result.logs && result.logs.length > 0 && (
        <details className="mt-4 group">
          <summary className="text-xs text-slate-500 cursor-pointer hover:text-slate-400 transition-colors">
            View {result.logs.length} analyzed log{result.logs.length !== 1 ? 's' : ''}
          </summary>
          <div className="mt-2 bg-slate-950 rounded-lg p-3 max-h-40 overflow-y-auto">
            {result.logs.map((log, i) => (
              <p key={i} className="text-xs text-slate-400 font-mono leading-relaxed">
                {log}
              </p>
            ))}
          </div>
        </details>
      )}
    </div>
  );
}

export default IncidentCard;
