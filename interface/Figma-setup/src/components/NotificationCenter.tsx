import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Bell, MessageSquare, TrendingUp, Heart } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { ScrollArea } from './ui/scroll-area';

interface NotificationCenterProps {
  currentEmotion: string | null;
}

const emotionMessages: Record<string, string[]> = {
  focused: [
    "🎯 You're in the zone! Keep this momentum going.",
    "💜 Deep work mode activated. You're crushing it!",
    "✨ Your concentration is impressive right now.",
  ],
  happy: [
    "😊 Your positive energy is contagious!",
    "🌟 Great vibes detected. Keep smiling!",
    "💖 Your happiness is radiating through.",
  ],
  tired: [
    "😴 Energy levels low. Time for a quick break?",
    "🌙 Rest is productive too. Don't forget to recharge.",
    "☕ A short walk might help refresh your mind.",
  ],
  stressed: [
    "🫧 Deep breath. You're doing better than you think.",
    "🌿 Detected stress. Try a 5-minute meditation.",
    "💆 Remember: breaks are part of productivity.",
  ],
  neutral: [
    "🎯 Steady as she goes. You're doing great.",
    "💭 Neutral state detected. Ready for your next task?",
    "⚖️ Balanced and composed. Nice!",
  ],
};

export function NotificationCenter({ currentEmotion }: NotificationCenterProps) {
  const getRecentMessages = () => {
    const messages = [];
    const now = Date.now();
    
    // Add current emotion message
    if (currentEmotion) {
      const emotionMsgs = emotionMessages[currentEmotion] || [];
      const randomMsg = emotionMsgs[Math.floor(Math.random() * emotionMsgs.length)];
      messages.push({
        id: 1,
        message: randomMsg,
        time: 'Just now',
        emotion: currentEmotion,
        type: 'emotion'
      });
    }
    
    // Add some system messages
    messages.push(
      {
        id: 2,
        message: 'Daily insight ready: Your productivity peaked at 2 PM',
        time: '30 min ago',
        emotion: null,
        type: 'insight'
      },
      {
        id: 3,
        message: 'Reminder: You\'ve been focused for 45 minutes. Great job!',
        time: '1 hour ago',
        emotion: null,
        type: 'reminder'
      },
      {
        id: 4,
        message: 'Stress levels decreased by 15% this week 📉',
        time: '2 hours ago',
        emotion: null,
        type: 'trend'
      }
    );
    
    return messages;
  };

  const messages = getRecentMessages();

  const getIcon = (type: string) => {
    switch (type) {
      case 'emotion':
        return Heart;
      case 'insight':
        return MessageSquare;
      case 'trend':
        return TrendingUp;
      default:
        return Bell;
    }
  };

  return (
    <Card className="bg-slate-800/30 border-violet-500/20 backdrop-blur-xl h-full">
      <div className="p-6 border-b border-violet-500/20">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Bell className="w-5 h-5 text-violet-400/80" />
            <h3 className="text-white/90 font-light">Notifications</h3>
          </div>
          <Badge className="bg-gradient-to-r from-violet-500/15 to-indigo-500/15 text-violet-200/80 border-violet-400/40 font-light">
            {messages.length}
          </Badge>
        </div>
      </div>

      <ScrollArea className="h-[600px]">
        <div className="p-4 space-y-3">
          <AnimatePresence mode="popLayout">
            {messages.map((msg, index) => {
              const Icon = getIcon(msg.type);
              return (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ delay: index * 0.1 }}
                  className="p-4 rounded-lg bg-purple-950/40 border border-purple-700/20 hover:bg-purple-950/60 transition-colors"
                >
                  <div className="flex items-start gap-3">
                    <div className="p-2 rounded-lg bg-purple-600/20 flex-shrink-0">
                      <Icon className="w-4 h-4 text-purple-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-purple-100 text-sm mb-1">{msg.message}</p>
                      <p className="text-purple-400 text-xs">{msg.time}</p>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      </ScrollArea>

      <div className="p-4 border-t border-violet-500/20">
        <p className="text-slate-500 text-xs text-center font-light">
          Notifications update in real-time based on your mood
        </p>
      </div>
    </Card>
  );
}
