import { useState, useEffect } from 'react';
import { FacialTracking } from './components/FacialTracking';
import { MoodAnalytics } from './components/MoodAnalytics';
import { InsightsPanel } from './components/InsightsPanel';
import { NotificationCenter } from './components/NotificationCenter';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Toaster } from './components/ui/sonner';
import { Scan, TrendingUp, Lightbulb } from 'lucide-react';
import { toast } from 'sonner@2.0.3';

export interface MoodEntry {
  timestamp: number;
  emotion: string;
  confidence: number;
}

export default function App() {
  const [moodHistory, setMoodHistory] = useState<MoodEntry[]>([]);
  const [currentEmotion, setCurrentEmotion] = useState<string | null>(null);

  useEffect(() => {
    // Generate some mock historical data for demonstration
    const now = Date.now();
    const mockData: MoodEntry[] = [];
    
    for (let i = 0; i < 48; i++) {
      const emotions = ['focused', 'happy', 'tired', 'stressed', 'neutral'];
      mockData.push({
        timestamp: now - (48 - i) * 3600000, // hourly data for last 48 hours
        emotion: emotions[Math.floor(Math.random() * emotions.length)],
        confidence: 0.7 + Math.random() * 0.3
      });
    }
    
    setMoodHistory(mockData);
  }, []);

  const handleEmotionDetected = (emotion: string, confidence: number) => {
    const newEntry: MoodEntry = {
      timestamp: Date.now(),
      emotion,
      confidence
    };
    
    setMoodHistory(prev => [...prev, newEntry]);
    setCurrentEmotion(emotion);
    
    // Show notification based on emotion
    const messages: Record<string, string> = {
      focused: "Great focus! Keep up the momentum 💜",
      happy: "Your positive energy is contagious! ✨",
      tired: "Time for a break? Rest recharges creativity 🌙",
      stressed: "Deep breath. You're doing better than you think 🫧",
      neutral: "Steady as she goes 🎯"
    };
    
    toast(messages[emotion] || "Mood detected", {
      description: `Confidence: ${(confidence * 100).toFixed(0)}%`,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900">
      {/* Ambient gradient overlays */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-1/2 h-1/2 bg-gradient-to-br from-amber-500/10 via-rose-500/8 to-transparent blur-3xl" />
        <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-gradient-to-bl from-violet-500/12 via-purple-500/8 to-transparent blur-3xl" />
        <div className="absolute bottom-0 left-1/3 w-1/2 h-1/2 bg-gradient-to-t from-orange-500/10 via-amber-500/6 to-transparent blur-3xl" />
        <div className="absolute bottom-0 right-1/3 w-1/2 h-1/2 bg-gradient-to-t from-indigo-500/10 via-transparent to-transparent blur-3xl" />
      </div>
      
      <div className="container mx-auto px-4 py-8 max-w-7xl relative z-10">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-3 mb-3">
            <div className="w-1.5 h-1.5 bg-gradient-to-r from-amber-400/60 to-rose-400/60 rounded-full animate-pulse" />
            <h1 className="text-white/90 tracking-tight bg-gradient-to-r from-slate-200 via-violet-200 to-slate-300 bg-clip-text text-transparent">Lumora</h1>
            <div className="w-1.5 h-1.5 bg-gradient-to-r from-violet-400/60 to-indigo-400/60 rounded-full animate-pulse" />
          </div>
          <p className="text-slate-400 font-light">AI-powered facial expression analysis</p>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="tracking" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 bg-slate-800/40 border border-violet-500/20 backdrop-blur-xl">
            <TabsTrigger 
              value="tracking"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-violet-600/80 data-[state=active]:to-indigo-600/80 data-[state=active]:text-white/90 font-light"
            >
              <Scan className="w-4 h-4 mr-2" />
              Live Tracking
            </TabsTrigger>
            <TabsTrigger 
              value="analytics"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-violet-600/80 data-[state=active]:to-indigo-600/80 data-[state=active]:text-white/90 font-light"
            >
              <TrendingUp className="w-4 h-4 mr-2" />
              Analytics
            </TabsTrigger>
            <TabsTrigger 
              value="insights"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-violet-600/80 data-[state=active]:to-indigo-600/80 data-[state=active]:text-white/90 font-light"
            >
              <Lightbulb className="w-4 h-4 mr-2" />
              Insights
            </TabsTrigger>
          </TabsList>

          <TabsContent value="tracking" className="space-y-6">
            <div className="grid lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <FacialTracking onEmotionDetected={handleEmotionDetected} />
              </div>
              <div>
                <NotificationCenter currentEmotion={currentEmotion} />
              </div>
            </div>
          </TabsContent>

          <TabsContent value="analytics">
            <MoodAnalytics moodHistory={moodHistory} />
          </TabsContent>

          <TabsContent value="insights">
            <InsightsPanel moodHistory={moodHistory} />
          </TabsContent>
        </Tabs>
      </div>
      
      <Toaster theme="dark" />
    </div>
  );
}

