import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Calendar, Clock, Percent } from 'lucide-react';
import { MoodEntry } from '../App';

interface MoodAnalyticsProps {
  moodHistory: MoodEntry[];
}

export function MoodAnalytics({ moodHistory }: MoodAnalyticsProps) {
  // Process data for charts
  const emotionCounts = moodHistory.reduce((acc, entry) => {
    acc[entry.emotion] = (acc[entry.emotion] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const pieData = Object.entries(emotionCounts).map(([emotion, count]) => ({
    name: emotion.charAt(0).toUpperCase() + emotion.slice(1),
    value: count,
    emotion
  }));

  const emotionColors: Record<string, string> = {
    focused: '#6366f1',
    happy: '#f59e0b',
    tired: '#8b5cf6',
    stressed: '#f43f5e',
    neutral: '#64748b'
  };

  // Group by hour for timeline
  const hourlyData = moodHistory.reduce((acc, entry) => {
    const hour = new Date(entry.timestamp).getHours();
    if (!acc[hour]) {
      acc[hour] = { focused: 0, happy: 0, tired: 0, stressed: 0, neutral: 0 };
    }
    acc[hour][entry.emotion]++;
    return acc;
  }, {} as Record<number, Record<string, number>>);

  const timelineData = Object.entries(hourlyData)
    .map(([hour, emotions]) => ({
      hour: `${hour}:00`,
      ...emotions
    }))
    .sort((a, b) => parseInt(a.hour) - parseInt(b.hour));

  // Calculate stats
  const totalEntries = moodHistory.length;
  const avgConfidence = moodHistory.reduce((sum, entry) => sum + entry.confidence, 0) / totalEntries;
  const mostCommon = Object.entries(emotionCounts).sort((a, b) => b[1] - a[1])[0];

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid md:grid-cols-4 gap-4">
        <Card className="p-4 bg-slate-800/30 border-violet-500/20 backdrop-blur-xl">
          <div className="flex items-center gap-3 mb-2">
            <Calendar className="w-5 h-5 text-violet-400/70" />
            <p className="text-slate-400 text-sm font-light">Total Sessions</p>
          </div>
          <p className="text-white/90 text-2xl font-light">{totalEntries}</p>
        </Card>

        <Card className="p-4 bg-slate-800/30 border-amber-500/20 backdrop-blur-xl">
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="w-5 h-5 text-amber-400/70" />
            <p className="text-slate-400 text-sm font-light">Most Common</p>
          </div>
          <p className="text-white/90 text-2xl font-light capitalize">{mostCommon?.[0] || 'N/A'}</p>
        </Card>

        <Card className="p-4 bg-slate-800/30 border-rose-500/20 backdrop-blur-xl">
          <div className="flex items-center gap-3 mb-2">
            <Percent className="w-5 h-5 text-rose-400/70" />
            <p className="text-slate-400 text-sm font-light">Avg Confidence</p>
          </div>
          <p className="text-white/90 text-2xl font-light">{(avgConfidence * 100).toFixed(0)}%</p>
        </Card>

        <Card className="p-4 bg-slate-800/30 border-indigo-500/20 backdrop-blur-xl">
          <div className="flex items-center gap-3 mb-2">
            <Clock className="w-5 h-5 text-indigo-400/70" />
            <p className="text-slate-400 text-sm font-light">Tracking Period</p>
          </div>
          <p className="text-white/90 text-2xl font-light">48h</p>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Emotion Distribution */}
        <Card className="p-6 bg-slate-800/30 border-violet-500/20 backdrop-blur-xl">
          <h3 className="text-white/90 mb-4 font-light">Emotion Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={emotionColors[entry.emotion]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#581c87', 
                  border: '1px solid #7c3aed',
                  borderRadius: '8px',
                  color: '#e9d5ff'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </Card>

        {/* Emotion Frequency */}
        <Card className="p-6 bg-slate-800/30 border-amber-500/20 backdrop-blur-xl">
          <h3 className="text-white/90 mb-4 font-light">Emotion Frequency</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={pieData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#8b5cf6" opacity={0.15} />
              <XAxis dataKey="name" stroke="#cbd5e1" style={{ fontSize: '12px', fontWeight: 300 }} />
              <YAxis stroke="#cbd5e1" style={{ fontSize: '12px', fontWeight: 300 }} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #8b5cf6',
                  borderRadius: '8px',
                  color: '#f1f5f9'
                }}
              />
              <Bar dataKey="value" fill="url(#colorGradient)" radius={[8, 8, 0, 0]} />
              <defs>
                <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#a78bfa" stopOpacity={0.7}/>
                  <stop offset="100%" stopColor="#6366f1" stopOpacity={0.7}/>
                </linearGradient>
              </defs>
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Timeline */}
        <Card className="p-6 bg-slate-800/30 border-indigo-500/20 backdrop-blur-xl lg:col-span-2">
          <h3 className="text-white/90 mb-4 font-light">Mood Timeline (Last 24 Hours)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={timelineData.slice(-24)}>
              <CartesianGrid strokeDasharray="3 3" stroke="#8b5cf6" opacity={0.15} />
              <XAxis dataKey="hour" stroke="#cbd5e1" style={{ fontSize: '12px', fontWeight: 300 }} />
              <YAxis stroke="#cbd5e1" style={{ fontSize: '12px', fontWeight: 300 }} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #8b5cf6',
                  borderRadius: '8px',
                  color: '#f1f5f9'
                }}
              />
              <Legend wrapperStyle={{ color: '#f1f5f9', fontWeight: 300 }} />
              <Line type="monotone" dataKey="focused" stroke="#6366f1" strokeWidth={2} />
              <Line type="monotone" dataKey="happy" stroke="#f59e0b" strokeWidth={2} />
              <Line type="monotone" dataKey="tired" stroke="#8b5cf6" strokeWidth={2} />
              <Line type="monotone" dataKey="stressed" stroke="#f43f5e" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      </div>
    </div>
  );
}
