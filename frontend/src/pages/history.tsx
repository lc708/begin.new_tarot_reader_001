import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowLeft, Calendar, Filter, Eye, Trash2, Search, Clock, Star, TrendingUp } from 'lucide-react';
import { tarotAPI } from '../lib/api';

interface ReadingRecord {
  id: string;
  question: string;
  question_category: string;
  spread_type: string;
  spread_name: string;
  reading_summary: string;
  timestamp: string;
  cards_count: number;
}

// 辅助函数
const getSpreadName = (spreadType: string): string => {
  const names: Record<string, string> = {
    'single': '单张牌占卜',
    'three_card': '三张牌占卜',
    'celtic_cross': '凯尔特十字'
  };
  return names[spreadType] || spreadType;
};

const getCardCount = (spreadType: string): number => {
  const counts: Record<string, number> = {
    'single': 1,
    'three_card': 3,
    'celtic_cross': 10
  };
  return counts[spreadType] || 1;
};

const HistoryPage: React.FC = () => {
  const [readings, setReadings] = useState<ReadingRecord[]>([]);
  const [filteredReadings, setFilteredReadings] = useState<ReadingRecord[]>([]);
  const [currentFilter, setCurrentFilter] = useState<'all' | 'recent' | 'love' | 'career' | 'general'>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedReading, setSelectedReading] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 6;

  // 模拟数据加载
  useEffect(() => {
    const loadReadings = async () => {
      setIsLoading(true);
      try {
        // 尝试从API加载数据
        const response = await tarotAPI.getReadingHistory();
        const historyData = response.data?.readings || [];
        
        // 转换数据格式
        const data: ReadingRecord[] = historyData.map(item => ({
          id: item.id,
          question: item.user_question,
          question_category: item.question_category,
          spread_type: item.spread_type,
          spread_name: getSpreadName(item.spread_type),
          reading_summary: item.reading_summary,
          timestamp: item.timestamp,
          cards_count: getCardCount(item.spread_type)
        }));
        
        setReadings(data);
      } catch (error) {
        // 使用模拟数据
        const mockReadings: ReadingRecord[] = [
          {
            id: '1',
            question: '我的事业发展如何？',
            question_category: 'career',
            spread_type: 'three_card',
            spread_name: '三张牌占卜',
            reading_summary: '事业运势上升，需要把握时机',
            timestamp: '2024-08-13T10:30:00Z',
            cards_count: 3
          },
          {
            id: '2',
            question: '这段感情的未来走向？',
            question_category: 'love',
            spread_type: 'celtic_cross',
            spread_name: '凯尔特十字',
            reading_summary: '感情稳定发展，需要更多沟通',
            timestamp: '2024-08-12T15:45:00Z',
            cards_count: 10
          },
          {
            id: '3',
            question: '今日运势如何？',
            question_category: 'general',
            spread_type: 'single',
            spread_name: '单张牌占卜',
            reading_summary: '保持积极心态，好运将至',
            timestamp: '2024-08-11T08:20:00Z',
            cards_count: 1
          },
          {
            id: '4',
            question: '应该换工作吗？',
            question_category: 'career',
            spread_type: 'three_card',
            spread_name: '三张牌占卜',
            reading_summary: '时机尚未成熟，继续积累经验',
            timestamp: '2024-08-10T14:15:00Z',
            cards_count: 3
          },
          {
            id: '5',
            question: '健康状况需要注意什么？',
            question_category: 'general',
            spread_type: 'single',
            spread_name: '单张牌占卜',
            reading_summary: '注意休息，保持身心平衡',
            timestamp: '2024-08-09T11:30:00Z',
            cards_count: 1
          }
        ];
        setReadings(mockReadings);
      }
      setIsLoading(false);
    };

    loadReadings();
  }, []);

  // 过滤和搜索
  useEffect(() => {
    let filtered = readings;

    // 按类别过滤
    if (currentFilter !== 'all') {
      if (currentFilter === 'recent') {
        const oneWeekAgo = new Date();
        oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
        filtered = filtered.filter(reading => new Date(reading.timestamp) > oneWeekAgo);
      } else {
        filtered = filtered.filter(reading => reading.question_category === currentFilter);
      }
    }

    // 搜索过滤
    if (searchTerm) {
      filtered = filtered.filter(reading => 
        reading.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
        reading.reading_summary.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // 按时间排序
    filtered.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

    setFilteredReadings(filtered);
    setCurrentPage(1);
  }, [readings, currentFilter, searchTerm]);

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'love': return '💖';
      case 'career': return '💼';
      case 'general': return '✨';
      default: return '🔮';
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'love': return 'text-pink-400';
      case 'career': return 'text-blue-400';
      case 'general': return 'text-purple-400';
      default: return 'text-gray-400';
    }
  };

  // 分页
  const totalPages = Math.ceil(filteredReadings.length / itemsPerPage);
  const paginatedReadings = filteredReadings.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  // 统计数据
  const stats = {
    total: readings.length,
    thisWeek: readings.filter(r => {
      const oneWeekAgo = new Date();
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
      return new Date(r.timestamp) > oneWeekAgo;
    }).length,
    byCategory: {
      love: readings.filter(r => r.question_category === 'love').length,
      career: readings.filter(r => r.question_category === 'career').length,
      general: readings.filter(r => r.question_category === 'general').length
    }
  };

  return (
    <>
      <Head>
        <title>占卜历史记录 - 神秘塔罗牌占卜师</title>
        <meta name="description" content="查看您的塔罗占卜历史记录，回顾过往的指引和洞察" />
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
          </div>

          {/* Page Title & Stats */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h1 className="text-responsive-xl font-mystical font-bold mb-6 text-gradient">
              占卜历史记录
            </h1>
            <div className="mystical-divider max-w-32 mx-auto mb-8"></div>
            
            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              <div className="reading-card p-6 text-center">
                <Star className="w-8 h-8 text-amber-400 mx-auto mb-2" />
                <div className="text-2xl font-bold text-white mb-1">{stats.total}</div>
                <div className="text-sm text-gray-400">总占卜次数</div>
              </div>
              
              <div className="reading-card p-6 text-center">
                <Clock className="w-8 h-8 text-blue-400 mx-auto mb-2" />
                <div className="text-2xl font-bold text-white mb-1">{stats.thisWeek}</div>
                <div className="text-sm text-gray-400">本周占卜</div>
              </div>
              
              <div className="reading-card p-6 text-center">
                <TrendingUp className="w-8 h-8 text-green-400 mx-auto mb-2" />
                <div className="text-2xl font-bold text-white mb-1">{stats.byCategory.career}</div>
                <div className="text-sm text-gray-400">事业占卜</div>
              </div>
              
              <div className="reading-card p-6 text-center">
                <div className="text-2xl mb-2">💖</div>
                <div className="text-2xl font-bold text-white mb-1">{stats.byCategory.love}</div>
                <div className="text-sm text-gray-400">感情占卜</div>
              </div>
            </div>
          </motion.div>

          {/* Search and Filter */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mb-12"
          >
            <div className="max-w-4xl mx-auto">
              {/* Search Bar */}
              <div className="relative mb-6">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="搜索占卜记录..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="mystical-input pl-12"
                />
              </div>
              
              {/* Filter Buttons */}
              <div className="flex flex-wrap justify-center gap-3">
                {[
                  { id: 'all', label: '全部', icon: Filter },
                  { id: 'recent', label: '最近一周', icon: Clock },
                  { id: 'love', label: '感情', icon: null },
                  { id: 'career', label: '事业', icon: null },
                  { id: 'general', label: '综合', icon: null }
                ].map((filter) => (
                  <button
                    key={filter.id}
                    onClick={() => setCurrentFilter(filter.id as any)}
                    className={`px-6 py-3 rounded-xl font-semibold transition-all flex items-center gap-2 ${
                      currentFilter === filter.id
                        ? 'bg-gradient-to-r from-purple-500 to-blue-600 text-white shadow-lg'
                        : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50'
                    }`}
                  >
                    {filter.icon && <filter.icon className="w-4 h-4" />}
                    {!filter.icon && <span>{getCategoryIcon(filter.id)}</span>}
                    {filter.label}
                  </button>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Loading State */}
          {isLoading && (
            <div className="text-center py-20">
              <div className="loading-spinner mx-auto mb-4"></div>
              <p className="text-gray-400">加载历史记录中...</p>
            </div>
          )}

          {/* Empty State */}
          {!isLoading && filteredReadings.length === 0 && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center py-20"
            >
              <div className="text-6xl mb-6">🔮</div>
              <h3 className="text-xl font-bold text-white mb-4">暂无占卜记录</h3>
              <p className="text-gray-400 mb-8">
                {searchTerm || currentFilter !== 'all' 
                  ? '没有找到符合条件的记录' 
                  : '开始您的第一次塔罗占卜吧'
                }
              </p>
              <Link href="/reading">
                <motion.button
                  whileHover={{ scale: 1.05, y: -2 }}
                  className="btn-primary flex items-center gap-3 mx-auto"
                >
                  <Star className="w-5 h-5" />
                  开始占卜
                </motion.button>
              </Link>
            </motion.div>
          )}

          {/* Reading Cards Grid */}
          {!isLoading && paginatedReadings.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <div className="grid-responsive">
                {paginatedReadings.map((reading, index) => (
                  <motion.div
                    key={reading.id}
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="history-card group"
                  >
                    <div className="flex items-start gap-3 mb-4">
                      <div className="text-2xl">{getCategoryIcon(reading.question_category)}</div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs text-gray-400">
                            {formatDate(reading.timestamp)}
                          </span>
                          <span className={`text-xs px-2 py-1 rounded-full bg-gray-800/50 ${getCategoryColor(reading.question_category)}`}>
                            {reading.spread_name}
                          </span>
                        </div>
                        <h3 className="font-semibold text-white group-hover:text-amber-300 transition-colors">
                          {reading.question}
                        </h3>
                      </div>
                    </div>
                    
                    <p className="text-gray-300 text-sm leading-relaxed mb-4 line-clamp-2">
                      {reading.reading_summary}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 text-xs text-gray-400">
                        <Calendar className="w-3 h-3" />
                        <span>{reading.cards_count} 张牌</span>
                      </div>
                      
                      <div className="flex gap-2">
                        <button
                          onClick={() => setSelectedReading(selectedReading === reading.id ? null : reading.id)}
                          className="p-2 text-purple-400 hover:text-purple-300 transition-colors"
                          title="查看详情"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          className="p-2 text-red-400 hover:text-red-300 transition-colors"
                          title="删除记录"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    
                    {/* Expanded Details */}
                    {selectedReading === reading.id && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        className="mt-4 pt-4 border-t border-purple-500/30"
                      >
                        <h4 className="text-sm font-semibold text-purple-300 mb-2">完整解读</h4>
                        <p className="text-sm text-gray-300 leading-relaxed">
                          {reading.reading_summary}
                        </p>
                        <div className="mt-3 text-xs text-gray-400">
                          类别: {reading.question_category} • 牌阵: {reading.spread_name}
                        </div>
                      </motion.div>
                    )}
                  </motion.div>
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex justify-center items-center gap-4 mt-12">
                  <button
                    onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                    disabled={currentPage === 1}
                    className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    上一页
                  </button>
                  
                  <div className="flex gap-2">
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                      <button
                        key={page}
                        onClick={() => setCurrentPage(page)}
                        className={`w-10 h-10 rounded-lg font-semibold transition-all ${
                          currentPage === page
                            ? 'bg-gradient-to-r from-purple-500 to-blue-600 text-white'
                            : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50'
                        }`}
                      >
                        {page}
                      </button>
                    ))}
                  </div>
                  
                  <button
                    onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                    disabled={currentPage === totalPages}
                    className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    下一页
                  </button>
                </div>
              )}
            </motion.div>
          )}

          {/* Bottom CTA */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mt-20"
          >
            <div className="reading-card">
              <h2 className="text-responsive-lg font-mystical font-bold mb-6 text-gradient">
                继续您的塔罗之旅
              </h2>
              
              <p className="text-gray-300 mb-8 leading-relaxed max-w-2xl mx-auto">
                每一次占卜都是一次自我探索的旅程，让塔罗继续为您指引前路
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/reading">
                  <motion.button
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className="btn-primary flex items-center gap-3"
                  >
                    <Star className="w-5 h-5" />
                    新的占卜
                  </motion.button>
                </Link>
                
                <Link href="/learn">
                  <motion.button
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className="btn-secondary flex items-center gap-3"
                  >
                    <Eye className="w-5 h-5" />
                    学习塔罗
                  </motion.button>
                </Link>
              </div>
            </div>
          </motion.div>
        </div>
      </main>
    </>
  );
};

export default HistoryPage;
