import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, Sparkles, Shuffle, Play, RotateCcw, Check, Wand2 } from 'lucide-react';
import { tarotAPI, ReadingResult, SpreadInfo } from '../lib/api';

interface Card {
  name: string;
  reversed: boolean;
  position: number;
  orientation: string;
}

// 根据牌阵类型获取预计时间和神秘提示
const getReadingTimeInfo = (spreadType: string) => {
  const timeInfo: Record<string, { duration: string; mysticalText: string[] }> = {
    'single': {
      duration: '约15秒',
      mysticalText: [
        '🔮 单张神谕正在显现...',
        '✨ 宇宙的智慧即将为您揭晓',
        '🌟 命运之轮缓缓转动，答案即将浮现'
      ]
    },
    'three_card': {
      duration: '约45秒',
      mysticalText: [
        '🌙 过去、现在、未来的脉络正在交织...',
        '✨ 时间之河的三重奥秘即将显现',
        '🔮 三重神谕正在汇聚时空的能量'
      ]
    },
    'love_spread': {
      duration: '约1分钟',
      mysticalText: [
        '💕 爱神维纳斯正在为您解读情感密码...',
        '🌹 五重心灵连接正在建立神秘链接',
        '✨ 情感的星辰正在为您重新排列'
      ]
    },
    'career_spread': {
      duration: '约1分钟',
      mysticalText: [
        '⚡ 事业之神墨丘利正在为您指引方向...',
        '🏛️ 六重智慧之门正在为您开启',
        '✨ 成功的星座正在为您重新连线'
      ]
    },
    'decision_spread': {
      duration: '约1分钟',
      mysticalText: [
        '⚖️ 智慧女神雅典娜正在为您权衡选择...',
        '🔮 七重决策之光正在照亮前路',
        '✨ 命运的天平正在为您寻找平衡'
      ]
    },
    'celtic_cross': {
      duration: '约2分钟',
      mysticalText: [
        '🌟 古老的凯尔特智慧正在苏醒...',
        '🔮 十重神圣几何正在构建宇宙真理',
        '✨ 最深层的奥秘即将为您完全展开'
      ]
    }
  };

  return timeInfo[spreadType] || timeInfo['single'];
};

const ReadingPage: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<'question' | 'spread' | 'cards' | 'drawing' | 'result'>('question');
  const [question, setQuestion] = useState('');
  const [selectedSpread, setSelectedSpread] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [readingResult, setReadingResult] = useState<ReadingResult | null>(null);
  const [spreads, setSpreads] = useState<SpreadInfo[]>([]);
  const [apiError, setApiError] = useState<string | null>(null);
  const [drawnCards, setDrawnCards] = useState<Card[]>([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentMysticalText, setCurrentMysticalText] = useState<string>('');
  const [textIndex, setTextIndex] = useState<number>(0);

  // 加载牌阵信息
  useEffect(() => {
    const loadSpreads = async () => {
      try {
        const response = await tarotAPI.getSpreads();
        setSpreads(response.data || []);
      } catch (error) {
        // 使用备用数据
        setSpreads([
          { id: 'single', name: '单张牌占卜', description: '简单快速的日常指引', card_count: 1, difficulty: '简单', usage: '日常问题' },
          { id: 'three_card', name: '三张牌占卜', description: '过去现在未来的时间线分析', card_count: 3, difficulty: '中等', usage: '发展趋势' },
          { id: 'celtic_cross', name: '凯尔特十字', description: '复杂问题的全面解析', card_count: 10, difficulty: '高级', usage: '深度分析' }
        ]);
      }
    };
    loadSpreads();
  }, []);

  // 管理神秘文案的循环显示
  useEffect(() => {
    if (isDrawing || isLoading) {
      const timeInfo = getReadingTimeInfo(selectedSpread || 'single');
      const mysticalTexts = timeInfo.mysticalText;
      
      setCurrentMysticalText(mysticalTexts[0]);
      setTextIndex(0);
      
      const interval = setInterval(() => {
        setTextIndex(prev => {
          const nextIndex = (prev + 1) % mysticalTexts.length;
          setCurrentMysticalText(mysticalTexts[nextIndex]);
          return nextIndex;
        });
      }, 4000); // 每4秒切换一次文案
      
      return () => clearInterval(interval);
    }
  }, [isDrawing, isLoading, selectedSpread]);

  const handleStartReading = async () => {
    setIsLoading(true);
    setIsDrawing(true);
    setApiError(null);
    
    try {
      const selectedSpreadInfo = spreads.find(s => s.id === selectedSpread);
      const cardCount = selectedSpreadInfo?.card_count || 1;
      
      // 模拟抽牌动画
      const mockCards: Card[] = [];
      for (let i = 0; i < cardCount; i++) {
        mockCards.push({
          name: `Card ${i + 1}`,
          reversed: Math.random() > 0.7,
          position: i + 1,
          orientation: Math.random() > 0.7 ? 'reversed' : 'upright'
        });
      }
      setDrawnCards(mockCards);
      
      // 等待动画完成
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      console.log('发送API请求...', { question, spread_type: selectedSpread });
      
      // 添加超时控制
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30秒超时
      
      try {
        const result = await tarotAPI.createReading({
          question,
          spread_type: selectedSpread,
          save_result: true
        });
        
        clearTimeout(timeoutId);
        console.log('API响应:', result);
        
        if (result && result.success) {
          console.log('设置占卜结果，跳转到结果页...');
          setReadingResult(result);
          setCurrentStep('result');
        } else {
          console.error('API返回错误:', result?.error || '未知错误');
          throw new Error(result?.error || '占卜过程中发生错误');
        }
      } catch (apiError) {
        clearTimeout(timeoutId);
        throw apiError;
      }
    } catch (error) {
      console.error('Reading error:', error);
      setApiError(error instanceof Error ? error.message : '占卜失败，请重试');
      
      // 创建备用结果
      const fallbackResult: ReadingResult = {
        success: true,
        question: question,
        question_category: "general",
        spread_type: selectedSpread,
        spread_name: spreads.find(s => s.id === selectedSpread)?.name || '占卜',
        drawn_cards: drawnCards,
        individual_readings: [],
        combined_reading: "🔮 由于AI占卜师暂时无法连接，为您提供了基础的塔罗指引。请静心感受这些牌带给您的直觉启发。",
        reading_summary: "相信直觉，静心感受牌的指引。",
        timestamp: new Date().toISOString()
      };
      setReadingResult(fallbackResult);
      setCurrentStep('result');
    } finally {
      setIsLoading(false);
      setIsDrawing(false);
    }
  };

  const handleQuestionSubmit = () => {
    if (question.trim()) {
      setCurrentStep('spread');
    }
  };



  const handleSpreadSelect = (spreadId: string) => {
    setSelectedSpread(spreadId);
    setCurrentStep('cards');
  };

  const handleNewReading = () => {
    setCurrentStep('question');
    setQuestion('');
    setSelectedSpread('');
    setReadingResult(null);
    setDrawnCards([]);
    setApiError(null);
  };

  const getStepProgress = () => {
    const steps = ['question', 'spread', 'cards', 'result'];
    return steps.indexOf(currentStep) + 1;
  };

  return (
    <>
      <Head>
        <title>塔罗占卜进行中 - 神秘塔罗牌占卜师</title>
        <meta name="description" content="正在进行塔罗牌占卜，探索您内心的答案" />
      </Head>

      <main className="min-h-screen py-8">
        <div className="container-custom">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <Link href="/">
              <motion.button 
                whileHover={{ scale: 1.05, x: -5 }}
                className="btn-secondary flex items-center gap-2"
              >
                <ArrowLeft size={20} />
                返回首页
              </motion.button>
            </Link>
            
            {/* Progress Indicator */}
            <div className="flex items-center gap-4">
              {[1, 2, 3, 4].map((step) => (
                <div
                  key={step}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    step <= getStepProgress() 
                      ? 'bg-gradient-to-r from-amber-400 to-amber-600 shadow-lg shadow-amber-500/50' 
                      : 'bg-gray-600'
                  }`}
                />
              ))}
            </div>
          </div>

          {/* Error Display */}
          {apiError && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-8 p-4 bg-red-900/50 border border-red-500/50 rounded-xl text-red-200"
            >
              {apiError}
            </motion.div>
          )}

          {/* Step Content */}
          <AnimatePresence mode="wait">
            {currentStep === 'question' && (
              <QuestionStep 
                question={question} 
                setQuestion={setQuestion} 
                onSubmit={handleQuestionSubmit} 
              />
            )}
            {currentStep === 'spread' && (
              <SpreadStep 
                spreads={spreads} 
                selectedSpread={selectedSpread} 
                onSelect={handleSpreadSelect} 
              />
            )}
            {currentStep === 'cards' && (
                            <CardsStep 
                selectedSpread={spreads.find(s => s.id === selectedSpread)}
                selectedSpreadId={selectedSpread}
                isLoading={isLoading}
                isDrawing={isDrawing}
                drawnCards={drawnCards}
                currentMysticalText={currentMysticalText}
                onStartReading={handleStartReading}
              />
            )}
            {currentStep === 'result' && readingResult && (
              <ResultStep 
                result={readingResult} 
                onNewReading={handleNewReading} 
              />
            )}
          </AnimatePresence>
        </div>
      </main>
    </>
  );
};

// QuestionForm 组件
const QuestionStep: React.FC<{
  question: string;
  setQuestion: (q: string) => void;
  onSubmit: () => void;
}> = ({ question, setQuestion, onSubmit }) => (
  <motion.div
    initial={{ opacity: 0, y: 50 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -50 }}
    className="container-narrow"
  >
    <div className="reading-card text-center">
      <div className="mb-8">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="w-20 h-20 mx-auto rounded-full bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center shadow-2xl shadow-purple-500/30"
        >
          <Sparkles className="w-10 h-10 text-amber-300" />
        </motion.div>
      </div>

      <h2 className="text-responsive-lg font-mystical font-bold mb-6 text-gradient">
        请输入您的问题
      </h2>
      
      <div className="mystical-divider max-w-24 mx-auto mb-8"></div>
      
      <p className="text-gray-300 mb-8 leading-relaxed max-w-2xl mx-auto">
        静下心来，想一想您最想了解的问题。可以是关于爱情、事业、健康或人生方向的任何问题。
        问题越具体，占卜结果越准确。
      </p>
      
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="mystical-input h-32 resize-none mb-8 text-lg"
        placeholder="例如：我该如何提升我的事业运势？"
      />
      
      <motion.button
        whileHover={{ scale: 1.05, y: -2 }}
        whileTap={{ scale: 0.95 }}
        onClick={onSubmit}
        disabled={!question.trim()}
        className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-3 mx-auto"
      >
        <Play className="w-5 h-5" />
        下一步：选择牌阵
      </motion.button>
    </div>
  </motion.div>
);

// SpreadVisualization 组件
const SpreadStep: React.FC<{
  spreads: SpreadInfo[];
  selectedSpread: string;
  onSelect: (id: string) => void;
}> = ({ spreads, selectedSpread, onSelect }) => (
  <motion.div
    initial={{ opacity: 0, y: 50 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -50 }}
    className="container-custom"
  >
    <div className="text-center mb-12">
      <h2 className="text-responsive-lg font-mystical font-bold mb-6 text-gradient">
        选择占卜牌阵
      </h2>
      <div className="mystical-divider max-w-24 mx-auto mb-6"></div>
      <p className="text-gray-300 max-w-3xl mx-auto">
        每种牌阵都有其独特的能量和解读方式，请选择最适合您问题的牌阵
      </p>
    </div>

    <div className="grid-responsive">
      {spreads.map((spread, index) => (
        <motion.div
          key={spread.id}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: index * 0.1 }}
          whileHover={{ y: -8 }}
          onClick={() => onSelect(spread.id)}
          className={`spread-card cursor-pointer transition-all ${
            selectedSpread === spread.id 
              ? 'ring-2 ring-amber-400 shadow-2xl shadow-amber-500/30' 
              : ''
          }`}
        >
          <div className="text-center">
            <h3 className="text-xl font-mystical font-bold mb-4 text-white">
              {spread.name}
            </h3>
            
            <div className="mystical-divider mb-4"></div>
            
            <p className="text-gray-300 mb-6 leading-relaxed text-sm">
              {spread.description}
            </p>
            
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-purple-300">牌数:</span>
                <span className="font-semibold text-amber-300">{spread.card_count} 张</span>
              </div>
              <div className="flex justify-between">
                <span className="text-purple-300">难度:</span>
                <span className="font-semibold text-white">{spread.difficulty}</span>
              </div>
              <div className="text-xs text-gray-400 mt-3">
                {spread.usage}
              </div>
            </div>
            
            {selectedSpread === spread.id && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                className="mt-4 flex items-center justify-center gap-2 text-amber-300"
              >
                <Check className="w-4 h-4" />
                <span className="text-sm font-semibold">已选择</span>
              </motion.div>
            )}
          </div>
        </motion.div>
      ))}
    </div>
    
    {selectedSpread && (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mt-12"
      >
        <motion.button
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => {}}
          className="btn-primary flex items-center gap-3 mx-auto"
        >
          <Shuffle className="w-5 h-5" />
          继续抽牌
        </motion.button>
      </motion.div>
    )}
  </motion.div>
);

// CardDeck 组件
const CardsStep: React.FC<{
  selectedSpread?: SpreadInfo;
  selectedSpreadId: string;
  isLoading: boolean;
  isDrawing: boolean;
  drawnCards: Card[];
  currentMysticalText: string;
  onStartReading: () => void;
}> = ({ selectedSpread, selectedSpreadId, isLoading, isDrawing, drawnCards, currentMysticalText, onStartReading }) => (
  <motion.div
    initial={{ opacity: 0, y: 50 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -50 }}
    className="container-narrow"
  >
    <div className="reading-card text-center">
      <div className="mb-8">
        <motion.div
          animate={{ 
            rotate: isLoading ? 360 : 0,
            scale: isLoading ? [1, 1.1, 1] : 1
          }}
          transition={{ 
            rotate: { duration: 2, repeat: isLoading ? Infinity : 0, ease: "linear" },
            scale: { duration: 1, repeat: isLoading ? Infinity : 0 }
          }}
          className="w-24 h-24 mx-auto rounded-full bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center shadow-2xl shadow-purple-500/30"
        >
          <Shuffle className="w-12 h-12 text-amber-300" />
        </motion.div>
      </div>

      <h2 className="text-responsive-lg font-mystical font-bold mb-6 text-gradient">
        {isDrawing ? '正在抽取塔罗牌...' : '准备抽取塔罗牌'}
      </h2>
      
      <div className="mystical-divider max-w-24 mx-auto mb-8"></div>
      
      {selectedSpread && (
        <div className="mb-8 p-6 bg-purple-900/30 rounded-xl border border-purple-500/30">
          <p className="text-gray-300 mb-2">
            您选择的牌阵：<span className="text-amber-300 font-semibold">{selectedSpread.name}</span>
          </p>
          <p className="text-sm text-gray-400">
            将为您抽取 {selectedSpread.card_count} 张神谕之牌
          </p>
        </div>
      )}

      {/* Card Drawing Animation */}
      {isDrawing && drawnCards.length > 0 && (
        <div className="mb-8">
          <div className="flex justify-center gap-4 flex-wrap">
            {drawnCards.map((card, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0, rotateY: 180 }}
                animate={{ opacity: 1, scale: 1, rotateY: 0 }}
                transition={{ delay: index * 0.5, duration: 0.8 }}
                className="tarot-card"
              >
                <div className="tarot-card-back">
                  <Sparkles className="text-amber-300" />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* 动态神秘提示 */}
      {isDrawing || isLoading ? (
        <div className="mb-8 text-center">
          {/* 预计时间提示 */}
          <div className="mb-6 p-4 bg-purple-900/40 rounded-xl border border-purple-400/30 backdrop-blur-sm">
            <div className="text-amber-300 font-mystical text-lg mb-2">
              ⏳ 预计占卜时间：{getReadingTimeInfo(selectedSpreadId).duration}
            </div>
            <div className="text-gray-400 text-sm">
              占卜复杂度越高，所需时间越长，请耐心等待
            </div>
          </div>
          
          {/* 循环神秘文案 */}
          <motion.div
            key={currentMysticalText}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.8 }}
            className="text-gray-300 leading-relaxed font-mystical text-lg"
          >
            {currentMysticalText}
          </motion.div>
          
          {/* 呼吸动画的点点 */}
          <div className="flex justify-center gap-2 mt-6">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                animate={{
                  scale: [1, 1.5, 1],
                  opacity: [0.5, 1, 0.5],
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: i * 0.5,
                }}
                className="w-2 h-2 bg-amber-400 rounded-full"
              />
            ))}
          </div>
          
          {/* 进度指示 */}
          <div className="mt-6 text-center">
            <div className="inline-flex items-center gap-2 text-purple-300 text-sm">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full"
              />
              神谕解读中...
            </div>
          </div>
        </div>
      ) : (
        <p className="text-gray-300 mb-8 leading-relaxed">
          静心凝神，专注于您的问题，然后点击下方按钮开始抽牌
        </p>
      )}
      
      {!isDrawing && (
        <motion.button
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.95 }}
          onClick={onStartReading}
          disabled={isLoading}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-3 mx-auto text-lg px-8 py-4"
        >
          {isLoading ? (
            <>
              <div className="loading-spinner" />
              占卜中...
            </>
          ) : (
            <>
              <Wand2 className="w-6 h-6" />
              开始抽牌
            </>
          )}
        </motion.button>
      )}
    </div>
  </motion.div>
);

// ReadingDisplay 组件
const ResultStep: React.FC<{
  result: ReadingResult;
  onNewReading: () => void;
}> = ({ result, onNewReading }) => (
  <motion.div
    initial={{ opacity: 0, y: 50 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -50 }}
    className="container-custom"
  >
    <div className="text-center mb-12">
      <h2 className="text-responsive-lg font-mystical font-bold mb-6 text-gradient">
        您的塔罗解读
      </h2>
      <div className="mystical-divider max-w-24 mx-auto mb-6"></div>
      <p className="text-amber-300 font-semibold text-lg">
        {result.reading_summary}
      </p>
    </div>

    {/* 抽到的牌 */}
    {result.drawn_cards && result.drawn_cards.length > 0 && (
      <div className="reading-card mb-8">
        <h3 className="text-xl font-mystical font-bold mb-6 text-center text-white">抽到的牌</h3>
        <div className="flex justify-center gap-6 flex-wrap">
          {result.drawn_cards.map((card, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, rotateY: 180 }}
              animate={{ opacity: 1, rotateY: 0 }}
              transition={{ delay: index * 0.3, duration: 0.8 }}
              className="drawn-card text-center p-4"
            >
              <div className="text-2xl mb-2">🎴</div>
              <h4 className="font-semibold text-gray-800 mb-1">{card.name}</h4>
              <p className="text-xs text-gray-600">
                {card.orientation === 'reversed' ? '逆位' : '正位'}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    )}

    {/* 综合解读 */}
    <div className="reading-card mb-8">
      <h3 className="text-xl font-mystical font-bold mb-6 text-white">占卜解读</h3>
      <div className="prose prose-invert max-w-none">
        <p className="text-gray-300 leading-relaxed whitespace-pre-line">
          {result.combined_reading}
        </p>
      </div>
    </div>

    {/* 操作按钮 */}
    <div className="flex flex-col sm:flex-row gap-4 justify-center">
      <motion.button
        whileHover={{ scale: 1.05, y: -2 }}
        whileTap={{ scale: 0.95 }}
        onClick={onNewReading}
        className="btn-primary flex items-center gap-3"
      >
        <RotateCcw className="w-5 h-5" />
        重新占卜
      </motion.button>
      
      <Link href="/">
        <motion.button
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.95 }}
          className="btn-secondary flex items-center gap-3"
        >
          <ArrowLeft className="w-5 h-5" />
          返回首页
        </motion.button>
      </Link>
    </div>
  </motion.div>
);

export default ReadingPage;