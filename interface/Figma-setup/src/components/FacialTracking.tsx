import { useState, useEffect, useRef } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Video, VideoOff, Camera, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

interface FacialTrackingProps {
  onEmotionDetected: (emotion: string, confidence: number) => void;
}

const emotions = [
  { id: 'focused', label: 'Focused', color: 'bg-indigo-500', emoji: '🎯' },
  { id: 'happy', label: 'Happy', color: 'bg-amber-500', emoji: '😊' },
  { id: 'tired', label: 'Tired', color: 'bg-violet-500', emoji: '😴' },
  { id: 'stressed', label: 'Stressed', color: 'bg-rose-500', emoji: '😰' },
  { id: 'neutral', label: 'Neutral', color: 'bg-slate-500', emoji: '😐' },
];

export function FacialTracking({ onEmotionDetected }: FacialTrackingProps) {
  const [isTracking, setIsTracking] = useState(false);
  const [currentEmotion, setCurrentEmotion] = useState<string | null>(null);
  const [confidence, setConfidence] = useState(0);
  const videoRef = useRef<HTMLVideoElement>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    return () => {
      stopTracking();
    };
  }, []);

  const startTracking = async () => {
    try {
      // Request camera access
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'user' } 
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      
      setIsTracking(true);
      
      // Simulate emotion detection every 3 seconds
      intervalRef.current = setInterval(() => {
        const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
        const randomConfidence = 0.75 + Math.random() * 0.25;
        
        setCurrentEmotion(randomEmotion.id);
        setConfidence(randomConfidence);
        onEmotionDetected(randomEmotion.id, randomConfidence);
      }, 3000);
      
    } catch (error) {
      console.error('Error accessing camera:', error);
      // Fallback: simulate tracking without camera
      setIsTracking(true);
      intervalRef.current = setInterval(() => {
        const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
        const randomConfidence = 0.75 + Math.random() * 0.25;
        
        setCurrentEmotion(randomEmotion.id);
        setConfidence(randomConfidence);
        onEmotionDetected(randomEmotion.id, randomConfidence);
      }, 3000);
    }
  };

  const stopTracking = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
    }
    
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    
    setIsTracking(false);
    setCurrentEmotion(null);
  };

  const currentEmotionData = emotions.find(e => e.id === currentEmotion);

  return (
    <Card className="bg-slate-800/30 border-violet-500/20 backdrop-blur-xl overflow-hidden">
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <Camera className="w-5 h-5 text-violet-400/80" />
            <h2 className="text-white/90 font-light">Facial Expression Tracking</h2>
          </div>
          
          {isTracking && (
            <Badge className="bg-gradient-to-r from-violet-500/15 to-indigo-500/15 text-violet-300/80 border-violet-400/40 font-light">
              <div className="w-2 h-2 bg-violet-400/70 rounded-full animate-pulse mr-2" />
              Live
            </Badge>
          )}
        </div>

        {/* Video Feed */}
        <div className="relative aspect-video bg-slate-900/50 rounded-lg overflow-hidden mb-4 border border-violet-500/25">
          {isTracking ? (
            <>
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full h-full object-cover"
              />
              
              {/* Overlay scanning effect */}
              <div className="absolute inset-0 pointer-events-none">
                <motion.div
                  className="absolute inset-0 border-2 border-violet-400/40"
                  animate={{
                    scale: [1, 1.05, 1],
                    opacity: [0.3, 0.6, 0.3],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                />
                
                {/* Corner brackets */}
                <div className="absolute top-4 left-4 w-8 h-8 border-l-2 border-t-2 border-amber-400/60" />
                <div className="absolute top-4 right-4 w-8 h-8 border-r-2 border-t-2 border-violet-400/60" />
                <div className="absolute bottom-4 left-4 w-8 h-8 border-l-2 border-b-2 border-rose-400/60" />
                <div className="absolute bottom-4 right-4 w-8 h-8 border-r-2 border-b-2 border-indigo-400/60" />
              </div>

              {/* Current Emotion Display */}
              <AnimatePresence mode="wait">
                {currentEmotionData && (
                  <motion.div
                    key={currentEmotion}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="absolute bottom-4 left-4 right-4"
                  >
                    <div className="bg-slate-900/85 backdrop-blur-md rounded-lg p-4 border border-violet-400/40">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <span className="text-3xl">{currentEmotionData.emoji}</span>
                          <div>
                            <p className="text-white/90 font-light">{currentEmotionData.label}</p>
                            <p className="text-slate-400 text-sm font-light">
                              {(confidence * 100).toFixed(0)}% confidence
                            </p>
                          </div>
                        </div>
                        <Sparkles className="w-5 h-5 text-violet-400/70" />
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </>
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <div className="text-center">
                <VideoOff className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                <p className="text-slate-500">Camera inactive</p>
              </div>
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="flex gap-3">
          {!isTracking ? (
            <Button 
              onClick={startTracking}
              className="flex-1 bg-gradient-to-r from-violet-600/90 to-indigo-600/90 hover:from-violet-500/90 hover:to-indigo-500/90 text-white/90 border-none shadow-lg shadow-violet-500/20 font-light"
            >
              <Video className="w-4 h-4 mr-2" />
              Start Tracking
            </Button>
          ) : (
            <Button 
              onClick={stopTracking}
              variant="outline"
              className="flex-1 border-violet-400/40 text-violet-300/80 hover:bg-violet-900/15 font-light"
            >
              <VideoOff className="w-4 h-4 mr-2" />
              Stop Tracking
            </Button>
          )}
        </div>
      </div>

      {/* Emotion Legend */}
      <div className="px-6 pb-6">
        <p className="text-slate-400 text-sm mb-3 font-light">Detectable Emotions</p>
        <div className="flex flex-wrap gap-2">
          {emotions.map((emotion) => (
            <Badge
              key={emotion.id}
              variant="outline"
              className={`${
                currentEmotion === emotion.id
                  ? 'bg-gradient-to-r from-violet-500/20 to-indigo-500/20 border-violet-400/60 text-white/90'
                  : 'border-slate-600/60 text-slate-400'
              } font-light`}
            >
              <span className="mr-1">{emotion.emoji}</span>
              {emotion.label}
            </Badge>
          ))}
        </div>
      </div>
    </Card>
  );
}
