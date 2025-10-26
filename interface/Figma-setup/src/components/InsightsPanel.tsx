import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Brain, TrendingUp, AlertCircle, Sparkles, Sun, Moon, Zap } from 'lucide-react';
import { MoodEntry } from '../App';
import { Progress } from './ui/progress';

interface InsightsPanelProps {
  moodHistory: MoodEntry[];
}

export function InsightsPanel({ moodHistory }: InsightsPanelProps) {
  // Calculate insights
  const emotionCounts = moodHistory.reduce((acc, entry) => {
    acc[entry.emotion] = (acc[entry.emotion] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const totalEntries = moodHistory.length;
  const focusedPercentage = ((emotionCounts.focused || 0) / totalEntries) * 100;
  const stressedPercentage = ((emotionCounts.stressed || 0) / totalEntries) * 100;
  const happyPercentage = ((emotionCounts.happy || 0) / totalEntries) * 100;

  // Time-based insights
  const morningEntries = moodHistory.filter(e => {
    const hour = new Date(e.timestamp).getHours();
    return hour >= 6 && hour < 12;
  });
  
  const afternoonEntries = moodHistory.filter(e => {
    const hour = new Date(e.timestamp).getHours();
    return hour >= 12 && hour < 18;
  });
  
  const eveningEntries = moodHistory.filter(e => {
    const hour = new Date(e.timestamp).getHours();
    return hour >= 18 || hour < 6;
  });

  const getMostCommonEmotion = (entries: MoodEntry[]) => {
    const counts = entries.reduce((acc, e) => {
      acc[e.emotion] = (acc[e.emotion] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
    
    return Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] || 'neutral';
  };

  const insights = [
    {
      icon: Brain,
      title: 'Productivity Score',
      description: `You're spending ${focusedPercentage.toFixed(0)}% of your time in a focused state. ${focusedPercentage > 40 ? 'Excellent concentration!' : 'Room for improvement.'}`,
      color: 'indigo',
      score: focusedPercentage
    },
    {
      icon: Sparkles,
      title: 'Wellbeing Index',
      description: `${happyPercentage.toFixed(0)}% positive emotions detected. ${happyPercentage > 30 ? 'Your mood is generally upbeat!' : 'Consider taking more breaks.'}`,
      color: 'amber',
      score: happyPercentage
    },
    {
      icon: AlertCircle,
      title: 'Stress Indicator',
      description: `Stress levels at ${stressedPercentage.toFixed(0)}%. ${stressedPercentage > 30 ? 'Consider stress management techniques.' : 'Well managed!'}`,
      color: 'rose',
      score: stressedPercentage
    }
  ];

  const timeInsights = [
    {
      icon: Sun,
      period: 'Morning',
      emotion: getMostCommonEmotion(morningEntries),
      count: morningEntries.length
    },
    {
      icon: Zap,
      period: 'Afternoon',
      emotion: getMostCommonEmotion(afternoonEntries),
      count: afternoonEntries.length
    },
    {
      icon: Moon,
      period: 'Evening',
      emotion: getMostCommonEmotion(eveningEntries),
      count: eveningEntries.length
    }
  ];

  const recommendations = [
    {
      title: 'Peak Performance Window',
      description: 'Your focus is highest during afternoon hours. Schedule important tasks then.',
      icon: TrendingUp
    },
    {
      title: 'Energy Management',
      description: 'Stress tends to increase in the evening. Try winding down 1 hour before bed.',
      icon: Zap
    },
    {
      title: 'Mood Patterns',
      description: 'You show consistent positive emotions. Keep maintaining your current routine!',
      icon: Sparkles
    }
  ];

  return (
    <div className="space-y-6">
      {/* Key Insights */}
      <div className="grid lg:grid-cols-3 gap-6">
        {insights.map((insight, index) => {
          const Icon = insight.icon;
          return (
            <Card key={index} className="p-6 bg-slate-800/30 border-violet-500/20 backdrop-blur-xl">
              <div className="flex items-start gap-4 mb-4">
                <div className={`p-3 rounded-lg bg-${insight.color}-500/15`}>
                  <Icon className={`w-6 h-6 text-${insight.color}-400/70`} />
                </div>
                <div className="flex-1">
                  <h3 className="text-white/90 mb-1 font-light">{insight.title}</h3>
                  <p className="text-slate-400 text-sm font-light">{insight.description}</p>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-500 font-light">Score</span>
                  <span className="text-white/90 font-light">{insight.score.toFixed(0)}%</span>
                </div>
                <Progress value={insight.score} className="h-2" />
              </div>
            </Card>
          );
        })}
      </div>

      {/* Time-based Analysis */}
      <Card className="p-6 bg-slate-800/30 border-amber-500/20 backdrop-blur-xl">
        <h3 className="text-white/90 mb-4 font-light">Time-based Patterns</h3>
        <div className="grid md:grid-cols-3 gap-4">
          {timeInsights.map((insight, index) => {
            const Icon = insight.icon;
            return (
              <div key={index} className="p-4 rounded-lg bg-slate-700/30 border border-violet-500/15">
                <div className="flex items-center gap-3 mb-3">
                  <Icon className="w-5 h-5 text-violet-400/70" />
                  <h4 className="text-white/90 font-light">{insight.period}</h4>
                </div>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 text-sm font-light">Dominant mood</span>
                    <Badge className="bg-gradient-to-r from-violet-500/15 to-indigo-500/15 text-white/90 border-violet-400/40 capitalize font-light">
                      {insight.emotion}
                    </Badge>
                  </div>
                  <p className="text-slate-500 text-sm font-light">{insight.count} entries</p>
                </div>
              </div>
            );
          })}
        </div>
      </Card>

      {/* Recommendations */}
      <Card className="p-6 bg-slate-800/30 border-rose-500/20 backdrop-blur-xl">
        <h3 className="text-white/90 mb-4 font-light">Personalized Recommendations</h3>
        <div className="space-y-4">
          {recommendations.map((rec, index) => {
            const Icon = rec.icon;
            return (
              <div key={index} className="flex items-start gap-4 p-4 rounded-lg bg-slate-700/30 border border-violet-500/15">
                <div className="p-2 rounded-lg bg-gradient-to-br from-violet-500/15 to-indigo-500/15 flex-shrink-0">
                  <Icon className="w-5 h-5 text-violet-400/70" />
                </div>
                <div>
                  <h4 className="text-white/90 mb-1 font-light">{rec.title}</h4>
                  <p className="text-slate-400 text-sm font-light">{rec.description}</p>
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
