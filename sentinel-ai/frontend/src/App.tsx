import React, { useState, useEffect } from 'react';
import { Activity, Database, BrainCircuit, ShieldAlert, LineChart as ChartIcon, PlayCircle, ShieldCheck, Server, AlertTriangle, Filter, GitMerge, Cpu, BarChart as BarChartIcon, Clock } from 'lucide-react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar, Legend } from 'recharts';

// --- MOCK DATA FOR VISUALIZATIONS ---
const trafficData = [
  { time: '10:00', benign: 4000, ddos: 240, dos: 100 },
  { time: '10:05', benign: 3000, ddos: 1398, dos: 200 },
  { time: '10:10', benign: 2000, ddos: 9800, dos: 500 },
  { time: '10:15', benign: 2780, ddos: 3908, dos: 300 },
  { time: '10:20', benign: 1890, ddos: 4800, dos: 400 },
  { time: '10:25', benign: 2390, ddos: 3800, dos: 250 },
  { time: '10:30', benign: 3490, ddos: 4300, dos: 100 },
];

const attackDistribution = [
  { name: 'DDoS (TCP/UDP)', value: 65 },
  { name: 'DoS', value: 20 },
  { name: 'Brute Force', value: 10 },
  { name: 'Web Attack', value: 5 },
];
const COLORS = ['#ef4444', '#f97316', '#eab308', '#3b82f6'];

const experimentData = [
  { name: 'Random Forest', fullTime: 6.2, hybridTime: 10.0, fullAcc: 99.98, hybridAcc: 99.97 },
  { name: 'CatBoost', fullTime: 7.4, hybridTime: 6.1, fullAcc: 99.98, hybridAcc: 99.97 },
  { name: 'HistGradBoost', fullTime: 8.0, hybridTime: 4.4, fullAcc: 99.97, hybridAcc: 99.97 },
  { name: 'Voting Ensemble', fullTime: 30.2, hybridTime: 16.8, fullAcc: 99.98, hybridAcc: 99.97 },
];

// --- COMPONENTS ---

const Dashboard = () => (
  <div className="p-8 space-y-6 animate-in fade-in duration-500">
    <div className="flex justify-between items-center">
      <h2 className="text-2xl font-bold text-gray-800">Global Security Telemetry</h2>
      <div className="flex items-center gap-2 text-green-600 bg-green-50 px-3 py-1 rounded-full text-sm font-semibold">
        <ShieldCheck size={16} /> Backend Ensemble Active
      </div>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {[
        { label: 'Total Packets Analyzed', value: '1.2M', icon: Server, color: 'text-blue-600' },
        { label: 'Threats Blocked', value: '84,392', icon: ShieldAlert, color: 'text-red-600' },
        { label: 'Ensemble Accuracy', value: '99.98%', icon: Activity, color: 'text-green-600' },
        { label: 'Active DDOS Threats', value: '2', icon: AlertTriangle, color: 'text-orange-600' },
      ].map((stat, i) => (
        <div key={i} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div className={`p-3 rounded-lg bg-gray-50 ${stat.color}`}><stat.icon size={24} /></div>
          <div><p className="text-sm text-gray-500 font-medium">{stat.label}</p><p className="text-2xl font-bold text-gray-900">{stat.value}</p></div>
        </div>
      ))}
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 lg:col-span-2">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">Network Traffic vs Blocked Attacks (Live)</h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={trafficData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorBenign" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/><stop offset="95%" stopColor="#10b981" stopOpacity={0}/></linearGradient>
                <linearGradient id="colorDdos" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/><stop offset="95%" stopColor="#ef4444" stopOpacity={0}/></linearGradient>
              </defs>
              <XAxis dataKey="time" /><YAxis /><CartesianGrid strokeDasharray="3 3" vertical={false} /><Tooltip />
              <Area type="monotone" dataKey="benign" stroke="#10b981" fillOpacity={1} fill="url(#colorBenign)" name="Benign Traffic" />
              <Area type="monotone" dataKey="ddos" stroke="#ef4444" fillOpacity={1} fill="url(#colorDdos)" name="DDoS Blocked" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">Threat Distribution</h3>
        <div className="h-64 flex items-center justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={attackDistribution} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                {attackDistribution.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="flex flex-wrap gap-2 justify-center mt-2">
          {attackDistribution.map((item, i) => (
            <div key={i} className="flex items-center gap-1 text-xs text-gray-600"><div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[i] }}></div>{item.name}</div>
          ))}
        </div>
      </div>
    </div>
  </div>
);

const DatasetIntelligence = () => (
  <div className="p-8 space-y-6 animate-in fade-in duration-500">
    <div>
      <h2 className="text-2xl font-bold text-gray-800">Dataset Intelligence (Module 1)</h2>
      <p className="text-gray-500">Hybrid Feature Selection Pipeline reducing dimensionality before training.</p>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <Database className="mx-auto text-gray-400 mb-2" size={32} />
        <p className="text-3xl font-bold text-gray-800">78</p>
        <p className="text-sm text-gray-500">Original Features</p>
      </div>
      <div className="bg-blue-50 p-6 rounded-xl shadow-sm border border-blue-200 relative">
        <Filter className="mx-auto text-blue-500 mb-2" size={32} />
        <p className="text-3xl font-bold text-blue-800">35</p>
        <p className="text-sm text-blue-600">Filter (ANOVA)</p>
        <div className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 text-blue-300">➜</div>
      </div>
      <div className="bg-indigo-50 p-6 rounded-xl shadow-sm border border-indigo-200 relative">
        <Cpu className="mx-auto text-indigo-500 mb-2" size={32} />
        <p className="text-3xl font-bold text-indigo-800">30</p>
        <p className="text-sm text-indigo-600">Wrapper (RFE)</p>
        <div className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 text-indigo-300">➜</div>
      </div>
      <div className="bg-green-50 p-6 rounded-xl shadow-sm border border-green-200">
        <GitMerge className="mx-auto text-green-500 mb-2" size={32} />
        <p className="text-3xl font-bold text-green-800">22</p>
        <p className="text-sm text-green-600">Hybrid Consensus</p>
      </div>
    </div>
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">Top Selected Features (Consensus Results)</h3>
      <div className="flex flex-wrap gap-3">
        {['Packet_Rate', 'Flow_Duration', 'Header_Length', 'SYN_Flag_Count', 'ACK_Flag_Count', 'Avg_Packet_Size', 'Protocol_Type', 'Subflow_Fwd_Bytes', 'Init_Bwd_Win_Bytes', 'Active_Max'].map(f => (
          <span key={f} className="px-3 py-1 bg-gray-100 border border-gray-200 rounded-full text-sm font-mono text-gray-700">{f}</span>
        ))}
      </div>
    </div>
  </div>
);

const ModelLaboratory = () => (
  <div className="p-8 space-y-6 animate-in fade-in duration-500">
    <div>
      <h2 className="text-2xl font-bold text-gray-800">Model Laboratory (Module 2)</h2>
      <p className="text-gray-500">Configure and train the Ensemble Detection Engine.</p>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 space-y-4">
        <h3 className="text-lg font-semibold text-gray-800 border-b pb-2">Base Classifiers</h3>
        <label className="flex items-center gap-3 p-3 border rounded-lg bg-indigo-50 border-indigo-200 cursor-pointer">
          <input type="checkbox" checked readOnly className="w-5 h-5 text-indigo-600" />
          <span className="font-medium text-indigo-900">Random Forest (n_estimators=100)</span>
        </label>
        <label className="flex items-center gap-3 p-3 border rounded-lg bg-indigo-50 border-indigo-200 cursor-pointer">
          <input type="checkbox" checked readOnly className="w-5 h-5 text-indigo-600" />
          <span className="font-medium text-indigo-900">CatBoost (iterations=100, balanced)</span>
        </label>
        <label className="flex items-center gap-3 p-3 border rounded-lg bg-indigo-50 border-indigo-200 cursor-pointer">
          <input type="checkbox" checked readOnly className="w-5 h-5 text-indigo-600" />
          <span className="font-medium text-indigo-900">HistGradientBoosting (LightGBM Equivalent)</span>
        </label>
      </div>
      <div className="bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-800 text-white space-y-4">
        <h3 className="text-lg font-semibold border-b border-slate-700 pb-2">Ensemble Configuration</h3>
        <p className="text-sm text-slate-400">The meta-model aggregates probabilities from the base classifiers using a Soft Voting algorithm.</p>
        <div className="p-4 bg-slate-800 rounded-lg font-mono text-sm text-green-400">
          <p>Ensemble Method: Soft Voting</p>
          <p>Weights: Uniform</p>
          <p>Status: TRAINED (Accuracy: 99.98%)</p>
        </div>
        <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-bold shadow-lg transition-colors">
          RE-TRAIN ENSEMBLE
        </button>
      </div>
    </div>
  </div>
);

const PredictionStudio = () => (
  <div className="p-8 space-y-6 animate-in fade-in duration-500">
    <div>
      <h2 className="text-2xl font-bold text-gray-800">Prediction Studio & SHAP (Module 3)</h2>
      <p className="text-gray-500">Deep-dive explainability for a single network packet/flow prediction.</p>
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 col-span-1 space-y-4">
        <h3 className="text-lg font-semibold text-gray-800">Packet Inspection</h3>
        <div className="space-y-2 font-mono text-sm bg-gray-50 p-4 rounded-lg border border-gray-200">
          <p><span className="text-gray-500">Protocol:</span> UDP</p>
          <p><span className="text-gray-500">Flow_Duration:</span> 0.001ms</p>
          <p><span className="text-gray-500">Packet_Rate:</span> 450,000 p/s</p>
          <p><span className="text-gray-500">Total_Length:</span> 45 Bytes</p>
          <p><span className="text-gray-500">SYN_Flag:</span> 0</p>
        </div>
        <div className="mt-4 p-4 rounded-lg bg-red-50 border border-red-200 text-center">
          <p className="text-sm text-red-600 font-bold uppercase tracking-wider mb-1">Prediction Result</p>
          <p className="text-3xl font-extrabold text-red-700">DDoS Attack</p>
          <p className="text-sm text-red-500 mt-1">Confidence: 99.87%</p>
        </div>
      </div>
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 col-span-2">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">SHAP Local Explanation (Feature Contributions)</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart layout="vertical" data={[
              { feature: 'Packet_Rate', importance: 0.85 },
              { feature: 'Flow_Duration', importance: 0.72 },
              { feature: 'Header_Length', importance: 0.45 },
              { feature: 'Total_Length', importance: 0.30 },
              { feature: 'SYN_Flag', importance: 0.15 },
            ]} margin={{ top: 0, right: 30, left: 60, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" domain={[0, 1]} />
              <YAxis dataKey="feature" type="category" width={100} tick={{fontSize: 12}} />
              <Tooltip cursor={{fill: 'transparent'}} />
              <Bar dataKey="importance" fill="#4f46e5" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  </div>
);

const ExperimentAnalysis = () => (
  <div className="p-8 space-y-6 animate-in fade-in duration-500">
    <div>
      <h2 className="text-2xl font-bold text-gray-800">Experiment Analysis</h2>
      <p className="text-gray-500">Comparing Full Features (78) vs Hybrid Features (22) Performance and Cost.</p>
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-96">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2"><Clock size={20} className="text-indigo-500"/> Training Time (Seconds)</h3>
        <ResponsiveContainer width="100%" height="80%">
          <BarChart data={experimentData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="name" tick={{fontSize: 12}} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="fullTime" name="Full Features (78)" fill="#94a3b8" radius={[4, 4, 0, 0]} />
            <Bar dataKey="hybridTime" name="Hybrid Features (22)" fill="#4f46e5" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-96">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2"><BarChartIcon size={20} className="text-green-500"/> Accuracy (%)</h3>
        <ResponsiveContainer width="100%" height="80%">
          <BarChart data={experimentData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="name" tick={{fontSize: 12}} />
            <YAxis domain={[99.5, 100]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="fullAcc" name="Full Features (78)" fill="#94a3b8" radius={[4, 4, 0, 0]} />
            <Bar dataKey="hybridAcc" name="Hybrid Features (22)" fill="#10b981" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  </div>
);

const AttackSimulator = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [shapData, setShapData] = useState([
    { feature: 'Waiting for packets...', importance: 0 }
  ]);

  useEffect(() => {
    const handleShap = (e: any) => setShapData(e.detail);
    window.addEventListener('shap-update', handleShap);
    return () => window.removeEventListener('shap-update', handleShap);
  }, []);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRunning) {
      interval = setInterval(async () => {
        try {
          const res = await fetch('http://localhost:8000/api/simulate');
          if (!res.ok) throw new Error('API Error');
          const data = await res.json();
          
          if (data.error) {
            setLogs(prev => [`[ERROR] ${data.error}`, ...prev].slice(0, 15));
            return;
          }

          const msg = data.is_attack 
            ? `[ALERT] ${data.true_label_from_csv} Detected | Src: ${data.src_ip} | Confidence: ${data.confidence}% -> BLOCKED`
            : `[OK] Normal Traffic (${data.true_label_from_csv}) | Src: ${data.src_ip} | Confidence: ${data.confidence}% -> PASSED`;
          
          setLogs(prev => [msg, ...prev].slice(0, 15));
          
          // Update the SHAP chart dynamically with real backend features!
          if (data.top_features && data.top_features.length > 0) {
            // we need to dispatch this to a state variable. 
            // Let's rely on window event or just modify the component state.
            window.dispatchEvent(new CustomEvent('shap-update', { detail: data.top_features }));
          }

        } catch (e) {
          setLogs(prev => ['[!] Connection to Backend Failed. Is FastAPI running?', ...prev].slice(0, 15));
        }
      }, 1000); // 1 packet per second for readability
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  return (
    <div className="p-8 space-y-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">DDoS Scenario Replay</h2>
          <p className="text-gray-500 mt-1">Safely inject held-out CSV attack data into the ML ensemble to test defenses.</p>
        </div>
        <button onClick={() => setIsRunning(!isRunning)} className={`px-6 py-3 rounded-lg font-bold text-white flex items-center gap-2 transition-all ${isRunning ? 'bg-red-600 hover:bg-red-700 shadow-red-200 shadow-lg' : 'bg-indigo-600 hover:bg-indigo-700 shadow-indigo-200 shadow-lg'}`}>
          {isRunning ? <ShieldAlert /> : <PlayCircle />}{isRunning ? 'STOP SIMULATION' : 'START SIMULATION'}
        </button>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-900 rounded-xl shadow-xl overflow-hidden flex flex-col h-96">
          <div className="bg-gray-800 px-4 py-2 flex items-center justify-between border-b border-gray-700">
            <span className="text-gray-300 font-mono text-sm">backend_firewall_logs.tail</span>
            <div className="flex gap-2"><div className="w-3 h-3 rounded-full bg-red-500"></div><div className="w-3 h-3 rounded-full bg-yellow-500"></div><div className="w-3 h-3 rounded-full bg-green-500"></div></div>
          </div>
          <div className="p-4 overflow-hidden flex-1 font-mono text-xs space-y-2">
            {logs.length === 0 && <span className="text-gray-500">Waiting for simulation to start...</span>}
            {logs.map((log, i) => (
              <div key={i} className={`${log.includes('ALERT') ? 'text-red-400' : 'text-green-400'} opacity-${Math.max(100 - i * 10, 10)}`}>
                <span className="text-gray-500">{new Date().toISOString().split('T')[1].slice(0,-1)}</span> {log}
              </div>
            ))}
          </div>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-96 flex flex-col">
          <h3 className="text-lg font-semibold mb-2 text-gray-800">SHAP Explainability (Why was it blocked?)</h3>
          <p className="text-xs text-gray-500 mb-6">Top Features contributing to the DDoS prediction (Module 3)</p>
          <div className="flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart layout="vertical" data={shapData} margin={{ top: 0, right: 30, left: 40, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" domain={[0, 1]} />
                <YAxis dataKey="feature" type="category" width={120} tick={{fontSize: 10}} />
                <Tooltip cursor={{fill: 'transparent'}} />
                <Bar dataKey="importance" fill="#4f46e5" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  )
}

// --- MAIN APP ROUTER ---
function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'dataset', label: 'Dataset Intelligence', icon: Database },
    { id: 'models', label: 'Model Laboratory', icon: BrainCircuit },
    { id: 'prediction', label: 'Prediction Studio', icon: ShieldAlert },
    { id: 'experiments', label: 'Experiment Analysis', icon: ChartIcon },
    { id: 'simulator', label: 'Attack Simulator', icon: PlayCircle },
  ]

  const renderContent = () => {
    switch(activeTab) {
      case 'dashboard': return <Dashboard />
      case 'dataset': return <DatasetIntelligence />
      case 'models': return <ModelLaboratory />
      case 'prediction': return <PredictionStudio />
      case 'experiments': return <ExperimentAnalysis />
      case 'simulator': return <AttackSimulator />
      default: return <Dashboard />
    }
  }

  return (
    <div className="flex h-screen bg-gray-50 font-sans text-gray-900">
      <div className="w-72 bg-[#0f172a] text-white flex flex-col shadow-2xl z-10">
        <div className="p-6 border-b border-slate-800">
          <h1 className="text-2xl font-extrabold flex items-center gap-3 tracking-tight">
            <ShieldAlert className="text-indigo-500" size={28} />
            Sentinel<span className="text-indigo-400">AI</span>
          </h1>
          <p className="text-xs text-slate-400 mt-2 font-medium tracking-wide">MULTI-CLASS IDS PLATFORM</p>
        </div>
        <nav className="flex-1 overflow-y-auto py-6 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = activeTab === item.id
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-4 px-8 py-3 text-sm font-medium transition-all duration-200 border-r-4 ${
                  isActive 
                    ? 'bg-indigo-900/50 text-indigo-200 border-indigo-500 shadow-inner' 
                    : 'border-transparent text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                }`}
              >
                <Icon size={20} className={isActive ? "text-indigo-400" : ""} />
                {item.label}
              </button>
            )
          })}
        </nav>
        <div className="p-6 border-t border-slate-800 text-xs text-slate-500 text-center">Module 1, 2, 3 Active</div>
      </div>
      <div className="flex-1 overflow-auto flex flex-col relative">
        <header className="bg-white border-b border-gray-200 px-8 py-5 flex items-center justify-between sticky top-0 z-10 backdrop-blur-sm bg-white/90">
          <h2 className="text-xl font-bold text-slate-800">{navItems.find(i => i.id === activeTab)?.label}</h2>
          <div className="flex items-center gap-4"><div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold">AI</div></div>
        </header>
        <main className="flex-1">
          {renderContent()}
        </main>
      </div>
    </div>
  )
}

export default App
